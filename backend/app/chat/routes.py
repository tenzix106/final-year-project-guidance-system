from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..extensions import db, socketio
from ..models import WorkspaceMessage, Workspace, WorkspaceMember, User

chat_bp = Blueprint("chat", __name__)


@chat_bp.get("/<int:workspace_id>/messages")
@jwt_required()
def get_messages(workspace_id):
    """Get all messages for a workspace"""
    user_id = int(get_jwt_identity())
    
    # Check if user is a member of the workspace
    workspace = Workspace.query.get_or_404(workspace_id)
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member and workspace.owner_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Get messages, ordered by creation time
    limit = request.args.get('limit', 50, type=int)
    before_id = request.args.get('before', type=int)
    
    query = WorkspaceMessage.query.filter_by(workspace_id=workspace_id)
    
    if before_id:
        query = query.filter(WorkspaceMessage.id < before_id)
    
    messages = query.order_by(WorkspaceMessage.created_at.desc()).limit(limit).all()
    
    # Reverse to show oldest first
    messages.reverse()
    
    return jsonify({
        "messages": [msg.to_dict() for msg in messages],
        "has_more": len(messages) == limit
    })


@chat_bp.post("/<int:workspace_id>/messages")
@jwt_required()
def send_message(workspace_id):
    """Send a message to workspace chat"""
    user_id = int(get_jwt_identity())
    
    # Check if user is a member of the workspace
    workspace = Workspace.query.get_or_404(workspace_id)
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member and workspace.owner_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    data = request.get_json()
    message_text = data.get('message', '').strip()
    
    if not message_text:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    # Create message
    message = WorkspaceMessage(
        workspace_id=workspace_id,
        user_id=user_id,
        message=message_text,
        message_type=data.get('message_type', 'text')
    )
    
    db.session.add(message)
    db.session.commit()
    
    # Emit WebSocket event to all workspace members
    message_dict = message.to_dict()
    socketio.emit('new_message', message_dict, room=f'workspace_{workspace_id}')
    
    return jsonify(message_dict), 201


@chat_bp.delete("/messages/<int:message_id>")
@jwt_required()
def delete_message(message_id):
    """Delete a message (only by author or workspace owner)"""
    user_id = int(get_jwt_identity())
    
    message = WorkspaceMessage.query.get_or_404(message_id)
    workspace = message.workspace
    
    # Only message author or workspace owner can delete
    if message.user_id != user_id and workspace.owner_id != user_id:
        return jsonify({"error": "Permission denied"}), 403
    
    db.session.delete(message)
    db.session.commit()
    
    return jsonify({"message": "Message deleted"}), 200
