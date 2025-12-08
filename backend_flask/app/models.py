from datetime import datetime
from .extensions import db, bcrypt
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Text


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for OAuth users
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # OAuth fields
    google_id = db.Column(db.String(255), unique=True, nullable=True, index=True)
    auth_provider = db.Column(db.String(20), default='email', nullable=False)  # 'email' or 'google'
    
    # Onboarding
    onboarding_completed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Additional user profile fields
    full_name = db.Column(db.String(255), nullable=True)
    university = db.Column(db.String(255), nullable=True)
    program = db.Column(db.String(100), nullable=True)
    academic_year = db.Column(db.String(10), nullable=True)
    
    # Relationships
    student_profiles = db.relationship('StudentProfile', backref='user', lazy=True, cascade='all, delete-orphan')
    generated_projects = db.relationship('GeneratedProject', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_projects = db.relationship('SavedProject', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return bcrypt.check_password_hash(self.password_hash, password)


class StudentProfile(db.Model):
    """Store detailed student profile information from the form"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Form fields
    full_name = db.Column(db.String(255), nullable=True)
    student_id = db.Column(db.String(50), nullable=True)
    program = db.Column(db.String(100), nullable=True)
    academic_year = db.Column(db.String(10), nullable=True)
    
    # Skills and interests (stored as text, parsed by frontend)
    skills_text = db.Column(Text, nullable=True)
    interests_text = db.Column(Text, nullable=True)
    
    # Project preferences
    difficulty_preference = db.Column(db.String(20), nullable=True)  # beginner, intermediate, advanced
    duration_preference = db.Column(db.String(20), nullable=True)   # 3-4, 4-6, 6-8, 8-12 months
    project_type = db.Column(db.String(50), nullable=True)          # research, application, analysis, innovation
    additional_requirements = db.Column(Text, nullable=True)
    supervisor_name = db.Column(db.String(255), nullable=True)
    budget_range = db.Column(db.String(20), nullable=True)


class ProjectTopic(db.Model):
    """Master table for project topics (both generated and pre-defined)"""
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Basic project information
    title = db.Column(db.String(500), nullable=False, index=True)
    description = db.Column(Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # Beginner, Intermediate, Advanced
    duration = db.Column(db.String(20), nullable=False)    # e.g., "6-8 months"
    
    # Extended project details
    objectives = db.Column(JSON, nullable=True)            # Array of objective strings
    methodology = db.Column(Text, nullable=True)
    expected_outcomes = db.Column(Text, nullable=True)
    
    # Categories and tags
    program_area = db.Column(db.String(100), nullable=True, index=True)  # e.g., computer-science, business
    tags = db.Column(JSON, nullable=True)                 # Array of tag strings
    
    # Source tracking
    source_type = db.Column(db.String(20), nullable=False, default='generated')  # generated, predefined, template
    ai_provider = db.Column(db.String(20), nullable=True)  # gemini, openai, huggingface (if AI-generated)
    
    # Relationships
    skills = db.relationship('ProjectSkill', backref='project_topic', lazy=True, cascade='all, delete-orphan')
    resources = db.relationship('ProjectResource', backref='project_topic', lazy=True, cascade='all, delete-orphan')
    generated_projects = db.relationship('GeneratedProject', backref='project_topic', lazy=True)


class ProjectSkill(db.Model):
    """Skills required for each project"""
    id = db.Column(db.Integer, primary_key=True)
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False, index=True)
    skill_level = db.Column(db.String(20), nullable=True)  # basic, intermediate, advanced
    is_required = db.Column(db.Boolean, default=True, nullable=False)


class ProjectResource(db.Model):
    """Resources associated with each project"""
    id = db.Column(db.Integer, primary_key=True)
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'), nullable=False)
    
    resource_type = db.Column(db.String(20), nullable=False)  # Paper, Tutorial, Tool, Book, Course
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(Text, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    author = db.Column(db.String(200), nullable=True)
    publication_year = db.Column(db.Integer, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class GeneratedProject(db.Model):
    """Track AI-generated projects for specific users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Generation context
    form_data_snapshot = db.Column(JSON, nullable=True)    # Store the form data used for generation
    ai_prompt = db.Column(Text, nullable=True)             # Store the prompt sent to AI
    ai_provider = db.Column(db.String(20), nullable=True)  # gemini, openai, huggingface
    generation_session_id = db.Column(db.String(100), nullable=True, index=True)  # Group projects from same session
    
    # User interaction
    viewed_at = db.Column(db.DateTime, nullable=True)
    last_interaction_at = db.Column(db.DateTime, nullable=True)


class SavedProject(db.Model):
    """Projects bookmarked/saved by users"""
    __tablename__ = 'saved_project'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # User notes and customization
    user_notes = db.Column(Text, nullable=True)
    custom_title = db.Column(db.String(500), nullable=True)
    is_favorite = db.Column(db.Boolean, default=False, nullable=False)
    
    # Progress tracking
    status = db.Column(db.String(20), default='saved', nullable=False)  # saved, not_started, in_progress, completed, abandoned
    progress_percentage = db.Column(db.Integer, default=0, nullable=False)
    
    # Timeline tracking
    progress_tracking_enabled = db.Column(db.Boolean, default=False, nullable=False)
    start_date = db.Column(db.DateTime, nullable=True)
    expected_completion_date = db.Column(db.DateTime, nullable=True)
    actual_completion_date = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    phases = db.relationship('ProjectPhase', back_populates='saved_project', cascade='all, delete-orphan', lazy='dynamic')
    
    # Unique constraint to prevent duplicate saves
    __table_args__ = (db.UniqueConstraint('user_id', 'project_topic_id', name='unique_user_project_save'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_topic_id': self.project_topic_id,
            'saved_at': self.saved_at.isoformat() if self.saved_at else None,
            'user_notes': self.user_notes,
            'custom_title': self.custom_title,
            'is_favorite': self.is_favorite,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'progress_tracking_enabled': self.progress_tracking_enabled,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'expected_completion_date': self.expected_completion_date.isoformat() if self.expected_completion_date else None,
            'actual_completion_date': self.actual_completion_date.isoformat() if self.actual_completion_date else None
        }


class ResourceCategory(db.Model):
    """Categories for organizing resources"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)  # Icon name for frontend
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class GlobalResource(db.Model):
    """Global resources available to all users (from FYPResources component)"""
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('resource_category.id'), nullable=True)
    
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(Text, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    resource_type = db.Column(db.String(50), nullable=False)  # database, journal, tutorial, tool, guide
    
    # Metadata
    author = db.Column(db.String(200), nullable=True)
    publication_year = db.Column(db.Integer, nullable=True)
    tags = db.Column(JSON, nullable=True)
    
    # Display properties
    icon = db.Column(db.String(50), nullable=True)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class UserActivity(db.Model):
    """Track user activity and interactions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    activity_type = db.Column(db.String(50), nullable=False, index=True)  # form_submit, project_view, project_save, etc.
    activity_data = db.Column(JSON, nullable=True)
    session_id = db.Column(db.String(100), nullable=True, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign key relationships (nullable for different activity types)
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'), nullable=True)
    
    # Index for analytics queries
    __table_args__ = (
        db.Index('ix_user_activity_user_type_date', 'user_id', 'activity_type', 'created_at'),
    )


class UserSkill(db.Model):
    """Track user's declared skills with proficiency levels"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    skill_name = db.Column(db.String(100), nullable=False, index=True)
    proficiency_level = db.Column(db.String(20), nullable=True)  # beginner, intermediate, advanced, expert
    years_experience = db.Column(db.Integer, nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)  # For future verification system
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Unique constraint to prevent duplicate skills per user
    __table_args__ = (db.UniqueConstraint('user_id', 'skill_name', name='unique_user_skill'),)


class ProjectPhase(db.Model):
    """Individual phases/milestones within a saved project"""
    __tablename__ = 'project_phase'
    
    id = db.Column(db.Integer, primary_key=True)
    saved_project_id = db.Column(db.Integer, db.ForeignKey('saved_project.id'), nullable=False)
    
    # Phase details
    phase_name = db.Column(db.String(100), nullable=False)
    phase_order = db.Column(db.Integer, nullable=False)  # 1, 2, 3...
    description = db.Column(Text, nullable=True)
    
    # Timeline
    estimated_duration_weeks = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    actual_completion_date = db.Column(db.DateTime, nullable=True)
    
    # Status
    status = db.Column(db.String(20), default='not_started', nullable=False)  # not_started, in_progress, completed, blocked
    progress_percentage = db.Column(db.Integer, default=0, nullable=False)
    notes = db.Column(Text, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    saved_project = db.relationship('SavedProject', back_populates='phases')
    tasks = db.relationship('PhaseTask', back_populates='phase', cascade='all, delete-orphan', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'saved_project_id': self.saved_project_id,
            'phase_name': self.phase_name,
            'phase_order': self.phase_order,
            'description': self.description,
            'estimated_duration_weeks': self.estimated_duration_weeks,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'actual_completion_date': self.actual_completion_date.isoformat() if self.actual_completion_date else None,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'notes': self.notes,
            'tasks': [task.to_dict() for task in self.tasks.all()] if self.tasks else []
        }


class PhaseTask(db.Model):
    """Specific tasks within each project phase"""
    __tablename__ = 'phase_task'
    
    id = db.Column(db.Integer, primary_key=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('project_phase.id'), nullable=False)
    
    # Task details
    task_name = db.Column(db.String(300), nullable=False)
    description = db.Column(Text, nullable=True)
    task_order = db.Column(db.Integer, nullable=True)
    
    # Status
    is_completed = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Optional deadline
    due_date = db.Column(db.DateTime, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    phase = db.relationship('ProjectPhase', back_populates='tasks')
    
    def to_dict(self):
        return {
            'id': self.id,
            'phase_id': self.phase_id,
            'task_name': self.task_name,
            'description': self.description,
            'task_order': self.task_order,
            'is_completed': self.is_completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None
        }


