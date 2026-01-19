from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from sqlalchemy import func

from . import progress_bp
from ..extensions import db
from ..models import SavedProject, ProjectPhase, PhaseTask, ProjectTopic


# Default project phases template
DEFAULT_PHASES = [
    {
        'phase_name': 'Research & Planning',
        'phase_order': 1,
        'description': 'Literature review, requirements gathering, project planning',
        'estimated_duration_weeks': 3,
        'default_tasks': [
            'Conduct literature review',
            'Define project scope and objectives',
            'Identify stakeholders and requirements',
            'Create project proposal',
            'Get supervisor approval'
        ]
    },
    {
        'phase_name': 'Design & Architecture',
        'phase_order': 2,
        'description': 'System design, architecture planning, technology selection',
        'estimated_duration_weeks': 2,
        'default_tasks': [
            'Design system architecture',
            'Create data models/schemas',
            'Select technologies and frameworks',
            'Design user interface mockups',
            'Document design decisions'
        ]
    },
    {
        'phase_name': 'Development',
        'phase_order': 3,
        'description': 'Implementation of core functionality',
        'estimated_duration_weeks': 6,
        'default_tasks': [
            'Set up development environment',
            'Implement core features',
            'Develop user interface',
            'Integrate components',
            'Code review and refactoring'
        ]
    },
    {
        'phase_name': 'Testing & Quality Assurance',
        'phase_order': 4,
        'description': 'Testing, bug fixing, and quality improvements',
        'estimated_duration_weeks': 2,
        'default_tasks': [
            'Write unit tests',
            'Perform integration testing',
            'Conduct user acceptance testing',
            'Fix identified bugs',
            'Performance optimization'
        ]
    },
    {
        'phase_name': 'Documentation & Deployment',
        'phase_order': 5,
        'description': 'Final documentation and project delivery',
        'estimated_duration_weeks': 2,
        'default_tasks': [
            'Write technical documentation',
            'Create user manual',
            'Prepare final report',
            'Deploy application',
            'Prepare presentation'
        ]
    }
]


@progress_bp.route('/initialize/<int:saved_project_id>', methods=['POST'])
@jwt_required()
def initialize_progress_tracking(saved_project_id):
    """Initialize progress tracking for a saved project"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        # Get the saved project
        saved_project = SavedProject.query.filter_by(
            id=saved_project_id,
            user_id=user_id
        ).first()
        
        if not saved_project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Check if already initialized
        if saved_project.progress_tracking_enabled:
            return jsonify({'message': 'Progress tracking already enabled'}), 200
        
        # Enable progress tracking
        saved_project.progress_tracking_enabled = True
        saved_project.status = 'not_started'
        
        # Set start date
        if data.get('start_date'):
            saved_project.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        else:
            saved_project.start_date = datetime.utcnow()
        
        # Calculate expected completion based on project duration
        project_topic = ProjectTopic.query.get(saved_project.project_topic_id)
        duration_weeks = 15  # Default
        if project_topic and hasattr(project_topic, 'estimated_duration'):
            duration_str = project_topic.estimated_duration or ''
            duration_map = {
                '1-2 months': 8,
                '3-4 months': 16,
                '5-6 months': 24,
                '6+ months': 30
            }
            duration_weeks = duration_map.get(duration_str, 15)
        
        saved_project.expected_completion_date = saved_project.start_date + timedelta(weeks=duration_weeks)
        
        # Create default phases
        current_date = saved_project.start_date
        for phase_template in DEFAULT_PHASES:
            phase = ProjectPhase(
                saved_project_id=saved_project.id,
                phase_name=phase_template['phase_name'],
                phase_order=phase_template['phase_order'],
                description=phase_template['description'],
                estimated_duration_weeks=phase_template['estimated_duration_weeks'],
                start_date=current_date,
                end_date=current_date + timedelta(weeks=phase_template['estimated_duration_weeks']),
                status='not_started'
            )
            db.session.add(phase)
            db.session.flush()
            
            # Create default tasks for this phase
            for idx, task_name in enumerate(phase_template['default_tasks'], 1):
                task = PhaseTask(
                    phase_id=phase.id,
                    task_name=task_name,
                    task_order=idx
                )
                db.session.add(task)
            
            current_date = phase.end_date
        
        db.session.commit()
        
        # Reload phases for response
        phases = ProjectPhase.query.filter_by(saved_project_id=saved_project.id).order_by(ProjectPhase.phase_order).all()
        
        return jsonify({
            'message': 'Progress tracking initialized',
            'project': saved_project.to_dict(),
            'phases': [phase.to_dict() for phase in phases]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@progress_bp.route('/<int:saved_project_id>', methods=['GET'])
@jwt_required()
def get_progress(saved_project_id):
    """Get full progress tracking data for a project"""
    try:
        user_id = get_jwt_identity()
        
        saved_project = SavedProject.query.filter_by(
            id=saved_project_id,
            user_id=user_id
        ).first()
        
        if not saved_project:
            return jsonify({'error': 'Project not found'}), 404
        
        # Get project topic
        project_topic = ProjectTopic.query.get(saved_project.project_topic_id)
        
        # Get all phases ordered
        phases = ProjectPhase.query.filter_by(
            saved_project_id=saved_project_id
        ).order_by(ProjectPhase.phase_order).all()
        
        # Calculate overall progress
        if phases:
            total_tasks = sum(phase.tasks.count() for phase in phases)
            completed_tasks = sum(
                phase.tasks.filter_by(is_completed=True).count()
                for phase in phases
            )
            saved_project.progress_percentage = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
            db.session.commit()
        
        # Build topic dict
        topic_dict = {}
        if project_topic:
            topic_dict = {
                'id': project_topic.id,
                'title': project_topic.title,
                'description': project_topic.description,
                'difficulty_level': getattr(project_topic, 'difficulty_level', None),
                'estimated_duration': getattr(project_topic, 'estimated_duration', None)
            }
        
        return jsonify({
            'project': saved_project.to_dict(),
            'topic': topic_dict,
            'phases': [phase.to_dict() for phase in phases]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@progress_bp.route('/phase/<int:phase_id>', methods=['PUT'])
@jwt_required()
def update_phase(phase_id):
    """Update a project phase"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        phase = ProjectPhase.query.join(SavedProject).filter(
            ProjectPhase.id == phase_id,
            SavedProject.user_id == user_id
        ).first()
        
        if not phase:
            return jsonify({'error': 'Phase not found'}), 404
        
        # Update phase fields
        if 'status' in data:
            phase.status = data['status']
            if data['status'] == 'completed':
                if not phase.actual_completion_date:
                    phase.actual_completion_date = datetime.utcnow()
                # Mark all tasks as completed and set progress to 100%
                phase.progress_percentage = 100
                for task in phase.tasks.all():
                    if not task.is_completed:
                        task.is_completed = True
                        task.completed_at = datetime.utcnow()
            elif data['status'] == 'not_started':
                # Reset all tasks when resetting phase
                for task in phase.tasks.all():
                    task.is_completed = False
                    task.completed_at = None
                phase.progress_percentage = 0
        
        if 'notes' in data:
            phase.notes = data['notes']
        
        if 'start_date' in data:
            phase.start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
        
        if 'end_date' in data:
            phase.end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        
        # Calculate phase progress from tasks (only if status wasn't explicitly set to completed/not_started)
        if 'status' not in data or data['status'] not in ['completed', 'not_started']:
            total_tasks = phase.tasks.count()
            if total_tasks > 0:
                completed = phase.tasks.filter_by(is_completed=True).count()
                phase.progress_percentage = int((completed / total_tasks * 100))
        
        db.session.commit()
        
        # Recalculate overall project progress
        saved_project = phase.saved_project
        all_phases = ProjectPhase.query.filter_by(saved_project_id=saved_project.id).all()
        
        if all_phases:
            total_tasks = sum(p.tasks.count() for p in all_phases)
            completed_tasks = sum(
                p.tasks.filter_by(is_completed=True).count()
                for p in all_phases
            )
            saved_project.progress_percentage = int((completed_tasks / total_tasks * 100)) if total_tasks > 0 else 0
            
            # Update project status based on phases
            if all(p.status == 'completed' for p in all_phases):
                saved_project.status = 'completed'
                saved_project.actual_completion_date = datetime.utcnow()
            elif any(p.status == 'in_progress' for p in all_phases):
                saved_project.status = 'in_progress'
            
            db.session.commit()
        
        return jsonify({'message': 'Phase updated', 'phase': phase.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@progress_bp.route('/task/<int:task_id>/toggle', methods=['PUT'])
@jwt_required()
def toggle_task(task_id):
    """Toggle task completion status"""
    try:
        user_id = get_jwt_identity()
        
        task = PhaseTask.query.join(ProjectPhase).join(SavedProject).filter(
            PhaseTask.id == task_id,
            SavedProject.user_id == user_id
        ).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Toggle completion
        task.is_completed = not task.is_completed
        task.completed_at = datetime.utcnow() if task.is_completed else None
        
        # Update phase progress
        phase = task.phase
        total_tasks = phase.tasks.count()
        completed = phase.tasks.filter_by(is_completed=True).count()
        phase.progress_percentage = int((completed / total_tasks * 100)) if total_tasks > 0 else 0
        
        # Auto-update phase status
        if phase.progress_percentage == 100:
            phase.status = 'completed'
            phase.actual_completion_date = datetime.utcnow()
        elif phase.progress_percentage > 0 and phase.status == 'not_started':
            phase.status = 'in_progress'
        
        db.session.commit()
        
        # Recalculate overall progress
        saved_project = phase.saved_project
        all_phases = ProjectPhase.query.filter_by(saved_project_id=saved_project.id).all()
        total_all_tasks = sum(p.tasks.count() for p in all_phases)
        completed_all_tasks = sum(
            p.tasks.filter_by(is_completed=True).count()
            for p in all_phases
        )
        saved_project.progress_percentage = int((completed_all_tasks / total_all_tasks * 100)) if total_all_tasks > 0 else 0
        db.session.commit()
        
        return jsonify({
            'message': 'Task updated',
            'task': task.to_dict(),
            'phase_progress': phase.progress_percentage,
            'project_progress': saved_project.progress_percentage
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@progress_bp.route('/task', methods=['POST'])
@jwt_required()
def add_task():
    """Add a custom task to a phase"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        phase_id = data.get('phase_id')
        
        # Verify user owns this phase
        phase = ProjectPhase.query.join(SavedProject).filter(
            ProjectPhase.id == phase_id,
            SavedProject.user_id == user_id
        ).first()
        
        if not phase:
            return jsonify({'error': 'Phase not found'}), 404
        
        # Get next task order
        max_order = db.session.query(func.max(PhaseTask.task_order)).filter_by(phase_id=phase_id).scalar() or 0
        
        task = PhaseTask(
            phase_id=phase_id,
            task_name=data['task_name'],
            description=data.get('description'),
            task_order=max_order + 1,
            due_date=datetime.fromisoformat(data['due_date'].replace('Z', '+00:00')) if data.get('due_date') else None
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify({'message': 'Task added', 'task': task.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@progress_bp.route('/task/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a custom task"""
    try:
        user_id = get_jwt_identity()
        
        task = PhaseTask.query.join(ProjectPhase).join(SavedProject).filter(
            PhaseTask.id == task_id,
            SavedProject.user_id == user_id
        ).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        phase = task.phase
        db.session.delete(task)
        db.session.commit()
        
        # Recalculate phase progress
        total_tasks = phase.tasks.count()
        if total_tasks > 0:
            completed = phase.tasks.filter_by(is_completed=True).count()
            phase.progress_percentage = int((completed / total_tasks * 100))
            db.session.commit()
        
        return jsonify({'message': 'Task deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@progress_bp.route('/customize/<int:saved_project_id>', methods=['POST'])
@jwt_required()
def customize_timeline(saved_project_id):
    """Replace default phases with AI-generated custom timeline"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Verify user owns this project
        saved_project = SavedProject.query.filter_by(
            id=saved_project_id,
            user_id=user_id
        ).first()
        
        if not saved_project:
            return jsonify({'error': 'Project not found'}), 404
        
        phases_data = data.get('phases', [])
        if not phases_data:
            return jsonify({'error': 'No phases provided'}), 400
        
        # Delete existing phases and tasks
        ProjectPhase.query.filter_by(saved_project_id=saved_project_id).delete()
        db.session.commit()
        
        # Create new custom phases
        start_date = datetime.utcnow()
        current_date = start_date
        created_phases = []
        
        for idx, phase_data in enumerate(phases_data):
            # Calculate dates
            duration_weeks = phase_data.get('duration_weeks', 2)
            end_date = current_date + timedelta(weeks=duration_weeks)
            
            # Create phase
            phase = ProjectPhase(
                saved_project_id=saved_project_id,
                phase_name=phase_data['name'],
                phase_order=idx + 1,
                description=phase_data.get('description', ''),
                estimated_duration_weeks=duration_weeks,
                start_date=current_date,
                end_date=end_date,
                status='not_started'
            )
            
            db.session.add(phase)
            db.session.flush()  # Get phase ID
            
            # Add tasks for this phase
            tasks = phase_data.get('tasks', [])
            for task_idx, task_name in enumerate(tasks):
                task = PhaseTask(
                    phase_id=phase.id,
                    task_name=task_name,
                    task_order=task_idx + 1,
                    is_completed=False
                )
                db.session.add(task)
            
            created_phases.append(phase)
            current_date = end_date
        
        # Update project status
        saved_project.status = 'not_started'
        
        db.session.commit()
        
        # Return the new phases
        return jsonify({
            'message': 'Custom timeline created',
            'phases': [phase.to_dict() for phase in created_phases]
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
