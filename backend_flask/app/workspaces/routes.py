from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy import or_
import secrets
from ..extensions import db
from ..models import User, Workspace, WorkspaceMember, WorkspaceInvite, SavedProject
from ..utils.activity import log_activity

workspaces_bp = Blueprint("workspaces", __name__)


@workspaces_bp.get("/")
@jwt_required()
def get_workspaces():
    """Get all workspaces for the current user (owned + member of)"""
    user_id = int(get_jwt_identity())
    
    # Get workspaces where user is owner
    owned_workspaces = Workspace.query.filter_by(owner_id=user_id).all()
    
    # Get workspaces where user is a member
    memberships = WorkspaceMember.query.filter_by(user_id=user_id).all()
    member_workspace_ids = [m.workspace_id for m in memberships]
    member_workspaces = Workspace.query.filter(Workspace.id.in_(member_workspace_ids)).all() if member_workspace_ids else []
    
    # Combine and deduplicate
    all_workspaces = {w.id: w for w in owned_workspaces + member_workspaces}.values()
    
    workspaces_data = []
    for workspace in all_workspaces:
        data = workspace.to_dict(include_members=True)
        # Add user's role in this workspace
        if workspace.owner_id == user_id:
            data['user_role'] = 'owner'
        else:
            member = next((m for m in workspace.members if m.user_id == user_id), None)
            data['user_role'] = member.role if member else 'viewer'
        workspaces_data.append(data)
    
    return jsonify({"workspaces": workspaces_data})


@workspaces_bp.post("/")
@jwt_required()
def create_workspace():
    """Create a new workspace"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    name = data.get("name")
    description = data.get("description", "")
    saved_project_id = data.get("saved_project_id")
    is_public = data.get("is_public", False)
    max_members = data.get("max_members", 10)
    
    if not name:
        return jsonify({"error": "Workspace name is required"}), 400
    
    # Validate saved_project if provided
    if saved_project_id:
        project = SavedProject.query.get(saved_project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        if project.user_id != user_id:
            return jsonify({"error": "You don't have access to this project"}), 403
    
    # Create workspace
    workspace = Workspace(
        name=name,
        description=description,
        owner_id=user_id,
        saved_project_id=saved_project_id,
        is_public=is_public,
        max_members=max_members
    )
    
    db.session.add(workspace)
    db.session.commit()
    
    # Add owner as a member with full permissions
    owner_member = WorkspaceMember(
        workspace_id=workspace.id,
        user_id=user_id,
        role='owner',
        can_edit=True,
        can_invite=True
    )
    
    db.session.add(owner_member)
    db.session.commit()
    
    # Log activity
    user = User.query.get(user_id)
    log_activity(
        workspace_id=workspace.id,
        user_id=user_id,
        activity_type='workspace_created',
        description=f"{user.full_name or user.email} created the workspace",
        metadata={'workspace_name': workspace.name}
    )
    
    return jsonify(workspace.to_dict(include_members=True)), 201


@workspaces_bp.get("/<int:workspace_id>")
@jwt_required()
def get_workspace(workspace_id):
    """Get a specific workspace"""
    user_id = int(get_jwt_identity())
    
    workspace = Workspace.query.get_or_404(workspace_id)
    
    # Check if user has access
    is_member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not is_member and workspace.owner_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    data = workspace.to_dict(include_members=True)
    data['user_role'] = is_member.role if is_member else 'owner'
    
    return jsonify(data)


@workspaces_bp.patch("/<int:workspace_id>")
@jwt_required()
def update_workspace(workspace_id):
    """Update workspace details"""
    user_id = int(get_jwt_identity())
    
    workspace = Workspace.query.get_or_404(workspace_id)
    
    # Only owner or admins can update
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if workspace.owner_id != user_id and (not member or member.role not in ['owner', 'admin']):
        return jsonify({"error": "Permission denied"}), 403
    
    data = request.get_json()
    
    if "name" in data:
        workspace.name = data["name"]
    if "description" in data:
        workspace.description = data["description"]
    if "is_public" in data:
        workspace.is_public = data["is_public"]
    if "max_members" in data:
        workspace.max_members = data["max_members"]
    
    workspace.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify(workspace.to_dict(include_members=True))


@workspaces_bp.delete("/<int:workspace_id>")
@jwt_required()
def delete_workspace(workspace_id):
    """Delete a workspace (owner only)"""
    user_id = int(get_jwt_identity())
    
    workspace = Workspace.query.get_or_404(workspace_id)
    
    if workspace.owner_id != user_id:
        return jsonify({"error": "Only the owner can delete this workspace"}), 403
    
    db.session.delete(workspace)
    db.session.commit()
    
    return jsonify({"message": "Workspace deleted successfully"})


@workspaces_bp.post("/<int:workspace_id>/invite")
@jwt_required()
def invite_to_workspace(workspace_id):
    """Invite someone to join the workspace"""
    user_id = int(get_jwt_identity())
    
    workspace = Workspace.query.get_or_404(workspace_id)
    
    # Check if user can invite
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member or not member.can_invite:
        return jsonify({"error": "You don't have permission to invite members"}), 403
    
    data = request.get_json()
    email = data.get("email")
    role = data.get("role", "member")
    
    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    # Check if already a member
    invitee = User.query.filter_by(email=email).first()
    if invitee:
        existing_member = WorkspaceMember.query.filter_by(
            workspace_id=workspace_id,
            user_id=invitee.id
        ).first()
        if existing_member:
            return jsonify({"error": "User is already a member"}), 400
    
    # Check for pending invite
    existing_invite = WorkspaceInvite.query.filter_by(
        workspace_id=workspace_id,
        email=email,
        status='pending'
    ).first()
    
    if existing_invite:
        return jsonify({"error": "Invitation already sent"}), 400
    
    # Create invite
    invite_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=7)
    
    invite = WorkspaceInvite(
        workspace_id=workspace_id,
        email=email,
        invited_by_id=user_id,
        invite_token=invite_token,
        role=role,
        expires_at=expires_at
    )
    
    db.session.add(invite)
    db.session.commit()
    
    # TODO: Send email notification
    
    return jsonify(invite.to_dict()), 201


@workspaces_bp.post("/invites/<string:invite_token>/accept")
@jwt_required()
def accept_invite(invite_token):
    """Accept a workspace invitation"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    
    invite = WorkspaceInvite.query.filter_by(invite_token=invite_token).first_or_404()
    
    # Validate invite
    if invite.status != 'pending':
        return jsonify({"error": "Invitation is no longer valid"}), 400
    
    if invite.expires_at and invite.expires_at < datetime.utcnow():
        invite.status = 'expired'
        db.session.commit()
        return jsonify({"error": "Invitation has expired"}), 400
    
    if user.email != invite.email:
        return jsonify({"error": "This invitation is for a different email"}), 403
    
    # Check workspace capacity
    workspace = invite.workspace
    if len(workspace.members) >= workspace.max_members:
        return jsonify({"error": "Workspace is at full capacity"}), 400
    
    # Add as member
    member = WorkspaceMember(
        workspace_id=invite.workspace_id,
        user_id=user_id,
        role=invite.role,
        can_edit=True if invite.role in ['admin', 'member'] else False,
        can_invite=True if invite.role == 'admin' else False
    )
    
    db.session.add(member)
    
    # Update invite status
    invite.status = 'accepted'
    invite.responded_at = datetime.utcnow()
    
    db.session.commit()
    
    # Log activity
    log_activity(
        workspace_id=workspace.id,
        user_id=user_id,
        activity_type='member_joined',
        description=f"{user.full_name or user.email} joined the workspace",
        metadata={'role': invite.role}
    )
    
    return jsonify(workspace.to_dict(include_members=True))


@workspaces_bp.delete("/<int:workspace_id>/members/<int:member_id>")
@jwt_required()
def remove_member(workspace_id, member_id):
    """Remove a member from workspace"""
    user_id = int(get_jwt_identity())
    
    workspace = Workspace.query.get_or_404(workspace_id)
    member_to_remove = WorkspaceMember.query.get_or_404(member_id)
    
    # Check permissions
    if workspace.owner_id != user_id and member_to_remove.user_id != user_id:
        # Only owner can remove others, or members can remove themselves
        return jsonify({"error": "Permission denied"}), 403
    
    if member_to_remove.role == 'owner' and member_to_remove.user_id != user_id:
        return jsonify({"error": "Cannot remove workspace owner"}), 403
    
    # Get member user info before deleting
    removed_user = User.query.get(member_to_remove.user_id)
    current_user = User.query.get(user_id)
    
    db.session.delete(member_to_remove)
    db.session.commit()
    
    # Log activity
    if member_to_remove.user_id == user_id:
        description = f"{current_user.full_name or current_user.email} left the workspace"
        activity_type = 'member_left'
    else:
        description = f"{removed_user.full_name or removed_user.email} was removed from the workspace"
        activity_type = 'member_removed'
    
    log_activity(
        workspace_id=workspace_id,
        user_id=user_id,
        activity_type=activity_type,
        description=description,
        metadata={'removed_user_id': member_to_remove.user_id}
    )
    
    return jsonify({"message": "Member removed successfully"})


@workspaces_bp.get("/discover")
@jwt_required()
def discover_workspaces():
    """Discover public workspaces"""
    user_id = int(get_jwt_identity())
    
    # Get public workspaces that user is not already a member of
    user_workspace_ids = [m.workspace_id for m in WorkspaceMember.query.filter_by(user_id=user_id).all()]
    
    public_workspaces = Workspace.query.filter(
        Workspace.is_public == True,
        ~Workspace.id.in_(user_workspace_ids) if user_workspace_ids else True
    ).all()
    
    return jsonify({"workspaces": [w.to_dict(include_members=False) for w in public_workspaces]})


@workspaces_bp.post("/<int:workspace_id>/join")
@jwt_required()
def join_workspace(workspace_id):
    """Join a public workspace"""
    user_id = int(get_jwt_identity())
    
    workspace = Workspace.query.get_or_404(workspace_id)
    
    # Check if workspace is public
    if not workspace.is_public:
        return jsonify({"error": "This workspace is private"}), 403
    
    # Check if already a member
    existing_member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if existing_member:
        return jsonify({"error": "You are already a member of this workspace"}), 400
    
    # Check workspace capacity
    if len(workspace.members) >= workspace.max_members:
        return jsonify({"error": "Workspace is at full capacity"}), 400
    
    # Add as member
    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=user_id,
        role='member',
        can_edit=True,
        can_invite=False
    )
    
    db.session.add(member)
    db.session.commit()
    
    # Log activity
    user = User.query.get(user_id)
    log_activity(
        workspace_id=workspace_id,
        user_id=user_id,
        activity_type='member_joined',
        description=f"{user.full_name or user.email} joined the workspace",
        metadata={'role': 'member', 'via': 'public_join'}
    )
    
    return jsonify(workspace.to_dict(include_members=True)), 201
