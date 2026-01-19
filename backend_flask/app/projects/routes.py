from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models import GeneratedProject, ProjectTopic, User
from datetime import datetime

projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@projects_bp.post("/track-generation")
@jwt_required()
def track_generation():
    """Track that a user generated projects"""
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid token"}), 401
    
    data = request.get_json(silent=True) or {}
    project_topics = data.get('project_topics', [])
    form_data = data.get('form_data', {})
    ai_provider = data.get('ai_provider', 'gemini')
    session_id = data.get('session_id')
    
    if not project_topics:
        return jsonify({"message": "No project topics provided"}), 400
    
    tracked_count = 0
    
    for topic_data in project_topics:
        # Create or get ProjectTopic
        topic = ProjectTopic(
            title=topic_data.get('title', ''),
            description=topic_data.get('description', ''),
            difficulty=topic_data.get('difficulty', 'Intermediate'),
            duration=topic_data.get('duration', '6-8 months'),
            objectives=topic_data.get('objectives', []),
            methodology=topic_data.get('methodology'),
            expected_outcomes=topic_data.get('expectedOutcomes'),
            program_area=form_data.get('program'),
            tags=topic_data.get('tags', []),
            source_type='generated',
            ai_provider=ai_provider
        )
        
        db.session.add(topic)
        db.session.flush()  # Get the ID
        
        # Create GeneratedProject record
        gen_project = GeneratedProject(
            user_id=user_id,
            project_topic_id=topic.id,
            form_data_snapshot=form_data,
            ai_provider=ai_provider,
            generation_session_id=session_id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(gen_project)
        tracked_count += 1
    
    db.session.commit()
    
    return jsonify({
        "message": f"Successfully tracked {tracked_count} generated projects",
        "tracked_count": tracked_count
    }), 201
