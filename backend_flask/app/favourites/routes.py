from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from ..extensions import db
from ..models import User, SavedProject, ProjectTopic


favourites_bp = Blueprint("favourites", __name__)


@favourites_bp.get("/")
@jwt_required()
def get_favourites():
    """Get all saved projects (favourites) for the current user"""
    user_id = get_jwt_identity()
    
    saved_projects = SavedProject.query.filter_by(user_id=user_id).all()
    
    favourites = []
    for saved_project in saved_projects:
        project_topic = ProjectTopic.query.get(saved_project.project_topic_id)
        favourite_data = {
            "id": saved_project.id,
            "user_notes": saved_project.user_notes,
            "custom_title": saved_project.custom_title,
            "is_favorite": saved_project.is_favorite,
            "status": saved_project.status,
            "progress_percentage": saved_project.progress_percentage,
            "saved_at": saved_project.saved_at.isoformat(),
            "project_topic": {
                "id": project_topic.id,
                "title": project_topic.title,
                "description": project_topic.description,
                "difficulty": project_topic.difficulty,
                "duration": project_topic.duration,
                "tags": project_topic.tags or []
            } if project_topic else None
        }
        favourites.append(favourite_data)
    
    return jsonify({"favourites": favourites})


@favourites_bp.post("/")
@jwt_required()
def save_favourite():
    """Save a project topic as favourite"""
    print("=== SAVE FAVOURITE ROUTE CALLED ===")
    user_id = get_jwt_identity()
    print(f"User ID: {user_id}")
    data = request.get_json(silent=True) or {}
    print(f"Request data: {data}")
    
    topic_data = data.get("topicData")
    notes = data.get("notes", "")
    
    if not topic_data:
        print("ERROR: topicData is required")
        return jsonify({"message": "topicData is required"}), 400
    
    # Create or get project topic
    project_topic = ProjectTopic.query.filter_by(title=topic_data.get("title")).first()
    
    if not project_topic:
        # Create new project topic
        project_topic = ProjectTopic(
            title=topic_data.get("title", ""),
            description=topic_data.get("description", ""),
            difficulty=topic_data.get("difficulty", "Medium"),
            duration=topic_data.get("timeline", "3-6 months"),
            tags=topic_data.get("tags", []),
            created_at=datetime.utcnow()
        )
        db.session.add(project_topic)
        db.session.flush()  # Get the ID without committing
        
        # Add resources if provided
        resources = topic_data.get("resources", [])
        for resource in resources:
            # Resources are stored separately in ProjectResource table
            # For now, we'll skip this as it requires more complex handling
            pass
    
    # Check if already saved by user
    existing_save = SavedProject.query.filter_by(
        user_id=user_id, 
        project_topic_id=project_topic.id
    ).first()
    
    if existing_save:
        return jsonify({"message": "Project already saved"}), 409
    
    # Create saved project entry
    saved_project = SavedProject(
        user_id=user_id,
        project_topic_id=project_topic.id,
        user_notes=notes,
        is_favorite=True,  # Mark as favourite when saving
        status="saved"
    )
    
    db.session.add(saved_project)
    db.session.commit()
    
    return jsonify({
        "id": saved_project.id,
        "message": "Project saved as favourite successfully"
    }), 201


@favourites_bp.delete("/<int:favourite_id>")
@jwt_required()
def remove_favourite(favourite_id):
    """Remove a favourite project"""
    user_id = get_jwt_identity()
    
    saved_project = SavedProject.query.filter_by(
        id=favourite_id,
        user_id=user_id
    ).first()
    
    if not saved_project:
        return jsonify({"message": "Favourite not found"}), 404
    
    db.session.delete(saved_project)
    db.session.commit()
    
    return jsonify({"message": "Favourite removed successfully"})


@favourites_bp.put("/<int:favourite_id>/notes")
@jwt_required()
def update_favourite_notes(favourite_id):
    """Update notes and progress for a favourite project"""
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    
    saved_project = SavedProject.query.filter_by(
        id=favourite_id,
        user_id=user_id
    ).first()
    
    if not saved_project:
        return jsonify({"message": "Favourite not found"}), 404
    
    # Update fields if provided
    if "notes" in data:
        saved_project.user_notes = data["notes"]
    
    if "progress_status" in data:
        valid_statuses = ["saved", "in_progress", "completed", "abandoned"]
        if data["progress_status"] in valid_statuses:
            saved_project.status = data["progress_status"]
    
    if "progress_percentage" in data:
        progress = data["progress_percentage"]
        if isinstance(progress, int) and 0 <= progress <= 100:
            saved_project.progress_percentage = progress
    
    if "custom_title" in data:
        saved_project.custom_title = data["custom_title"]
    
    if "is_favorite" in data:
        saved_project.is_favorite = bool(data["is_favorite"])
    
    db.session.commit()
    
    return jsonify({
        "message": "Favourite updated successfully",
        "favourite": {
            "id": saved_project.id,
            "user_notes": saved_project.user_notes,
            "custom_title": saved_project.custom_title,
            "is_favorite": saved_project.is_favorite,
            "status": saved_project.status,
            "progress_percentage": saved_project.progress_percentage
        }
    })


@favourites_bp.get("/check/<project_title>")
@jwt_required()
def check_favourite_status(project_title):
    """Check if a project is saved as favourite by current user"""
    user_id = get_jwt_identity()
    
    # Find project topic by title
    project_topic = ProjectTopic.query.filter_by(title=project_title).first()
    if not project_topic:
        return jsonify({"is_favourite": False})
    
    # Check if saved by user
    saved_project = SavedProject.query.filter_by(
        user_id=user_id,
        project_topic_id=project_topic.id
    ).first()
    
    return jsonify({
        "is_favourite": saved_project is not None,
        "favourite_id": saved_project.id if saved_project else None
    })