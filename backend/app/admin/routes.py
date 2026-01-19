from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from ..models import User, ProjectTopic, GeneratedProject, SavedProject, UserActivity
from ..extensions import db
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


def admin_required(fn):
    """Decorator to require admin role"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        # Convert to int since JWT identity is stored as string
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return jsonify({"message": "Invalid token"}), 401
        
        user = User.query.get(user_id)
        if not user or not user.is_admin():
            return jsonify({"message": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


@admin_bp.get("/stats/overview")
@admin_required
def get_overview_stats():
    """Get system overview statistics"""
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_admins = User.query.filter_by(role='admin').count()
    total_topics = ProjectTopic.query.count()
    total_generated = GeneratedProject.query.count()
    total_saved = SavedProject.query.count()
    
    # Users registered in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users_30d = User.query.filter(User.created_at >= thirty_days_ago).count()
    
    # Active users (users who generated/saved projects in last 30 days)
    active_users_30d = db.session.query(User.id).join(
        GeneratedProject
    ).filter(
        GeneratedProject.created_at >= thirty_days_ago
    ).distinct().count()
    
    return jsonify({
        "total_users": total_users,
        "total_students": total_students,
        "total_admins": total_admins,
        "total_topics": total_topics,
        "total_generated_projects": total_generated,
        "total_saved_projects": total_saved,
        "new_users_30d": new_users_30d,
        "active_users_30d": active_users_30d
    })


@admin_bp.get("/stats/usage")
@admin_required
def get_usage_stats():
    """Get detailed usage statistics"""
    # Projects generated per day for last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    daily_generations = db.session.query(
        func.date(GeneratedProject.created_at).label('date'),
        func.count(GeneratedProject.id).label('count')
    ).filter(
        GeneratedProject.created_at >= thirty_days_ago
    ).group_by(
        func.date(GeneratedProject.created_at)
    ).order_by('date').all()
    
    # Top programs by number of users
    top_programs = db.session.query(
        User.program,
        func.count(User.id).label('count')
    ).filter(
        User.program.isnot(None)
    ).group_by(
        User.program
    ).order_by(desc('count')).limit(10).all()
    
    # AI provider usage
    ai_usage = db.session.query(
        ProjectTopic.ai_provider,
        func.count(ProjectTopic.id).label('count')
    ).filter(
        ProjectTopic.ai_provider.isnot(None)
    ).group_by(
        ProjectTopic.ai_provider
    ).all()
    
    return jsonify({
        "daily_generations": [
            {"date": str(row.date), "count": row.count}
            for row in daily_generations
        ],
        "top_programs": [
            {"program": row.program, "count": row.count}
            for row in top_programs
        ],
        "ai_provider_usage": [
            {"provider": row.ai_provider, "count": row.count}
            for row in ai_usage
        ]
    })


@admin_bp.get("/users")
@admin_required
def get_all_users():
    """Get list of all users with pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    role_filter = request.args.get('role', '', type=str)
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.email.ilike(f'%{search}%')) |
            (User.full_name.ilike(f'%{search}%'))
        )
    
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        "users": [
            {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "university": user.university,
                "program": user.program,
                "academic_year": user.academic_year,
                "role": user.role,
                "auth_provider": user.auth_provider,
                "created_at": user.created_at.isoformat(),
                "onboarding_completed": user.onboarding_completed
            }
            for user in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    })


@admin_bp.patch("/users/<int:user_id>/role")
@admin_required
def update_user_role(user_id):
    """Update a user's role"""
    current_user_id = get_jwt_identity()
    if str(user_id) == str(current_user_id):
        return jsonify({"message": "Cannot change your own role"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.get_json()
    new_role = data.get('role')
    
    if new_role not in ['student', 'admin']:
        return jsonify({"message": "Invalid role. Must be 'student' or 'admin'"}), 400
    
    user.role = new_role
    db.session.commit()
    
    return jsonify({
        "message": "User role updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    })


@admin_bp.delete("/users/<int:user_id>")
@admin_required
def delete_user(user_id):
    """Delete a user and all their associated data"""
    current_user_id = get_jwt_identity()
    
    # Prevent admins from deleting themselves
    if str(user_id) == str(current_user_id):
        return jsonify({"message": "Cannot delete your own account"}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    user_email = user.email
    
    # Delete the user (cascade will handle related records)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        "message": f"User {user_email} deleted successfully"
    })


@admin_bp.get("/topics")
@admin_required
def get_all_topics():
    """Get list of all project topics"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)
    source_type = request.args.get('source_type', '', type=str)
    
    query = ProjectTopic.query
    
    if search:
        query = query.filter(
            (ProjectTopic.title.ilike(f'%{search}%')) |
            (ProjectTopic.description.ilike(f'%{search}%'))
        )
    
    if source_type:
        query = query.filter_by(source_type=source_type)
    
    pagination = query.order_by(ProjectTopic.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        "topics": [
            {
                "id": topic.id,
                "title": topic.title,
                "description": topic.description,
                "difficulty": topic.difficulty,
                "duration": topic.duration,
                "program_area": topic.program_area,
                "tags": topic.tags,
                "source_type": topic.source_type,
                "ai_provider": topic.ai_provider,
                "created_at": topic.created_at.isoformat()
            }
            for topic in pagination.items
        ],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    })


@admin_bp.delete("/topics/<int:topic_id>")
@admin_required
def delete_topic(topic_id):
    """Delete a project topic"""
    topic = ProjectTopic.query.get(topic_id)
    if not topic:
        return jsonify({"message": "Topic not found"}), 404
    
    # Check if topic is referenced by saved or generated projects
    saved_count = SavedProject.query.filter_by(project_topic_id=topic_id).count()
    generated_count = GeneratedProject.query.filter_by(project_topic_id=topic_id).count()
    
    if saved_count > 0 or generated_count > 0:
        return jsonify({
            "message": f"Cannot delete topic. It is referenced by {saved_count} saved projects and {generated_count} generated projects"
        }), 400
    
    db.session.delete(topic)
    db.session.commit()
    
    return jsonify({"message": "Topic deleted successfully"})


@admin_bp.get("/settings/ai")
@admin_required
def get_ai_settings():
    """Get current AI configuration (from environment/config)"""
    from ..config import Config
    import os
    
    return jsonify({
        "providers": {
            "gemini": {
                "configured": bool(os.getenv('GEMINI_API_KEY')),
                "key_length": len(os.getenv('GEMINI_API_KEY', ''))
            },
            "openai": {
                "configured": bool(os.getenv('OPENAI_API_KEY')),
                "key_length": len(os.getenv('OPENAI_API_KEY', ''))
            },
            "huggingface": {
                "configured": bool(os.getenv('HUGGINGFACE_API_KEY')),
                "key_length": len(os.getenv('HUGGINGFACE_API_KEY', ''))
            }
        },
        "default_provider": os.getenv('DEFAULT_AI_PROVIDER', 'gemini')
    })
