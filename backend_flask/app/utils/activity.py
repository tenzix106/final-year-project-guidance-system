from ..extensions import db, socketio
from ..models import WorkspaceActivity


def log_activity(workspace_id, user_id, activity_type, description, metadata=None):
    """Helper function to log workspace activities"""
    activity = WorkspaceActivity(
        workspace_id=workspace_id,
        user_id=user_id,
        activity_type=activity_type,
        description=description,
        activity_data=metadata or {}
    )
    db.session.add(activity)
    db.session.commit()
    
    # Emit WebSocket event for real-time updates
    activity_dict = activity.to_dict()
    socketio.emit('new_activity', activity_dict, room=f'workspace_{workspace_id}')
    
    return activity
