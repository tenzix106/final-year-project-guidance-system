from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import WorkspaceActivity, Workspace, WorkspaceMember

activity_bp = Blueprint("activity", __name__)


@activity_bp.get("/<int:workspace_id>/activity")
@jwt_required()
def get_activities(workspace_id):
    """Get activity feed for a workspace"""
    user_id = int(get_jwt_identity())
    
    # Check if user is a member of the workspace
    workspace = Workspace.query.get_or_404(workspace_id)
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member and workspace.owner_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Get activities, ordered by creation time (newest first)
    limit = request.args.get('limit', 50, type=int)
    before_id = request.args.get('before', type=int)
    
    query = WorkspaceActivity.query.filter_by(workspace_id=workspace_id)
    
    if before_id:
        query = query.filter(WorkspaceActivity.id < before_id)
    
    activities = query.order_by(WorkspaceActivity.created_at.desc()).limit(limit).all()
    
    return jsonify({
        "activities": [activity.to_dict() for activity in activities],
        "has_more": len(activities) == limit
    })
