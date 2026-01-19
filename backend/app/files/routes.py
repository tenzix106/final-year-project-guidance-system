from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from ..extensions import db, socketio
from ..models import WorkspaceFile, Workspace, WorkspaceMember, User
from ..utils.activity import log_activity

files_bp = Blueprint("files", __name__)

# Configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'png', 'jpg', 'jpeg', 'gif', 'svg',
    'zip', 'rar', '7z',
    'mp4', 'avi', 'mov',
    'py', 'js', 'html', 'css', 'json', 'xml',
    'md', 'csv'
}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_icon(file_type):
    """Get icon name based on file type"""
    if not file_type:
        return 'File'
    
    if file_type.startswith('image/'):
        return 'Image'
    elif file_type.startswith('video/'):
        return 'Video'
    elif file_type in ['application/pdf']:
        return 'FileText'
    elif file_type in ['application/zip', 'application/x-rar', 'application/x-7z-compressed']:
        return 'Archive'
    elif 'word' in file_type or 'document' in file_type:
        return 'FileText'
    elif 'excel' in file_type or 'spreadsheet' in file_type:
        return 'Table'
    elif 'powerpoint' in file_type or 'presentation' in file_type:
        return 'Presentation'
    else:
        return 'File'


@files_bp.get("/<int:workspace_id>/files")
@jwt_required()
def get_files(workspace_id):
    """Get all files for a workspace"""
    user_id = int(get_jwt_identity())
    
    # Check if user is a member of the workspace
    workspace = Workspace.query.get_or_404(workspace_id)
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member and workspace.owner_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Get files, ordered by upload time (newest first)
    files = WorkspaceFile.query.filter_by(
        workspace_id=workspace_id
    ).order_by(WorkspaceFile.created_at.desc()).all()
    
    return jsonify({
        "files": [f.to_dict() for f in files]
    })


@files_bp.post("/<int:workspace_id>/files")
@jwt_required()
def upload_file(workspace_id):
    """Upload a file to workspace"""
    user_id = int(get_jwt_identity())
    
    # Check if user is a member of the workspace
    workspace = Workspace.query.get_or_404(workspace_id)
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member and workspace.owner_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Check if member has permission to upload
    if member and not member.can_edit:
        return jsonify({"error": "You don't have permission to upload files"}), 403
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400
    
    # Get file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({"error": f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"}), 400
    
    # Generate unique filename
    original_filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"{workspace_id}_{timestamp}_{original_filename}"
    
    # Create workspace-specific directory
    workspace_dir = os.path.join(UPLOAD_FOLDER, f'workspace_{workspace_id}')
    os.makedirs(workspace_dir, exist_ok=True)
    
    file_path = os.path.join(workspace_dir, filename)
    
    # Save file
    file.save(file_path)
    
    # Get description from form data
    description = request.form.get('description', '')
    
    # Create database record
    workspace_file = WorkspaceFile(
        workspace_id=workspace_id,
        uploaded_by=user_id,
        filename=filename,
        original_filename=original_filename,
        file_size=file_size,
        file_type=file.content_type,
        file_path=file_path,
        description=description
    )
    
    db.session.add(workspace_file)
    db.session.commit()
    
    # Log activity
    user = User.query.get(user_id)
    log_activity(
        workspace_id=workspace_id,
        user_id=user_id,
        activity_type='file_uploaded',
        description=f"{user.full_name or user.email} uploaded {original_filename}",
        metadata={
            'file_id': workspace_file.id,
            'filename': original_filename,
            'file_size': file_size
        }
    )
    
    # Emit WebSocket event
    file_dict = workspace_file.to_dict()
    socketio.emit('new_file', file_dict, room=f'workspace_{workspace_id}')
    
    return jsonify(file_dict), 201


@files_bp.get("/<int:workspace_id>/files/<int:file_id>/download")
@jwt_required()
def download_file(workspace_id, file_id):
    """Download a file"""
    user_id = int(get_jwt_identity())
    
    # Check if user is a member of the workspace
    workspace = Workspace.query.get_or_404(workspace_id)
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member and workspace.owner_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Get file
    workspace_file = WorkspaceFile.query.get_or_404(file_id)
    
    if workspace_file.workspace_id != workspace_id:
        return jsonify({"error": "File not found in this workspace"}), 404
    
    if not os.path.exists(workspace_file.file_path):
        return jsonify({"error": "File not found on server"}), 404
    
    return send_file(
        workspace_file.file_path,
        as_attachment=True,
        download_name=workspace_file.original_filename
    )


@files_bp.delete("/<int:workspace_id>/files/<int:file_id>")
@jwt_required()
def delete_file(workspace_id, file_id):
    """Delete a file"""
    user_id = int(get_jwt_identity())
    
    # Check if user is a member of the workspace
    workspace = Workspace.query.get_or_404(workspace_id)
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member and workspace.owner_id != user_id:
        return jsonify({"error": "Access denied"}), 403
    
    # Get file
    workspace_file = WorkspaceFile.query.get_or_404(file_id)
    
    if workspace_file.workspace_id != workspace_id:
        return jsonify({"error": "File not found in this workspace"}), 404
    
    # Check if user has permission to delete (owner, admin, or file uploader)
    is_owner = workspace.owner_id == user_id
    is_admin = member and member.role in ['admin', 'owner']
    is_uploader = workspace_file.uploaded_by == user_id
    
    if not (is_owner or is_admin or is_uploader):
        return jsonify({"error": "You don't have permission to delete this file"}), 403
    
    # Delete physical file
    if os.path.exists(workspace_file.file_path):
        os.remove(workspace_file.file_path)
    
    # Get info before deleting from DB
    filename = workspace_file.original_filename
    
    # Delete database record
    db.session.delete(workspace_file)
    db.session.commit()
    
    # Log activity
    user = User.query.get(user_id)
    log_activity(
        workspace_id=workspace_id,
        user_id=user_id,
        activity_type='file_deleted',
        description=f"{user.full_name or user.email} deleted {filename}",
        metadata={'filename': filename}
    )
    
    return jsonify({"message": "File deleted successfully"})
