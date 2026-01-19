from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import decode_token
from .extensions import db
from .models import WorkspaceMember, Workspace


def register_socket_events(socketio):
    """Register all Socket.IO event handlers"""
    
    @socketio.on('connect')
    def handle_connect(auth):
        """Handle client connection"""
        try:
            # Verify JWT token from auth
            if auth and 'token' in auth:
                token = auth['token']
                decoded = decode_token(token)
                user_id = int(decoded['sub'])
                print(f"User {user_id} connected via WebSocket")
                return True
            else:
                print("Connection rejected: No token provided")
                return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        print("Client disconnected")
    
    @socketio.on('join_workspace')
    def handle_join_workspace(data):
        """Join a workspace room for real-time updates"""
        workspace_id = data.get('workspace_id')
        token = data.get('token')
        
        try:
            # Verify user has access to workspace
            decoded = decode_token(token)
            user_id = int(decoded['sub'])
            
            workspace = Workspace.query.get(workspace_id)
            if not workspace:
                emit('error', {'message': 'Workspace not found'})
                return
            
            # Check membership
            member = WorkspaceMember.query.filter_by(
                workspace_id=workspace_id,
                user_id=user_id
            ).first()
            
            if not member and workspace.owner_id != user_id:
                emit('error', {'message': 'Access denied'})
                return
            
            # Join the room
            room = f'workspace_{workspace_id}'
            join_room(room)
            emit('joined_workspace', {'workspace_id': workspace_id})
            print(f"User {user_id} joined workspace {workspace_id}")
            
        except Exception as e:
            print(f"Error joining workspace: {e}")
            emit('error', {'message': str(e)})
    
    @socketio.on('leave_workspace')
    def handle_leave_workspace(data):
        """Leave a workspace room"""
        workspace_id = data.get('workspace_id')
        room = f'workspace_{workspace_id}'
        leave_room(room)
        emit('left_workspace', {'workspace_id': workspace_id})
    
    @socketio.on('send_message')
    def handle_send_message(data):
        """Handle real-time chat message"""
        workspace_id = data.get('workspace_id')
        message_data = data.get('message')
        
        # Broadcast to all users in the workspace room
        room = f'workspace_{workspace_id}'
        emit('new_message', message_data, room=room, include_self=False)
    
    @socketio.on('file_uploaded')
    def handle_file_uploaded(data):
        """Handle file upload notification"""
        workspace_id = data.get('workspace_id')
        file_data = data.get('file')
        
        # Broadcast to all users in the workspace room
        room = f'workspace_{workspace_id}'
        emit('new_file', file_data, room=room, include_self=False)
    
    @socketio.on('activity_logged')
    def handle_activity_logged(data):
        """Handle activity feed update"""
        workspace_id = data.get('workspace_id')
        activity_data = data.get('activity')
        
        # Broadcast to all users in the workspace room
        room = f'workspace_{workspace_id}'
        emit('new_activity', activity_data, room=room, include_self=False)
