from datetime import datetime
from .extensions import db, bcrypt
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Text


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Additional user profile fields
    full_name = db.Column(db.String(255), nullable=True)
    student_id = db.Column(db.String(50), nullable=True, index=True)
    program = db.Column(db.String(100), nullable=True)
    academic_year = db.Column(db.String(10), nullable=True)
    
    # Relationships
    student_profiles = db.relationship('StudentProfile', backref='user', lazy=True, cascade='all, delete-orphan')
    generated_projects = db.relationship('GeneratedProject', backref='user', lazy=True, cascade='all, delete-orphan')
    saved_projects = db.relationship('SavedProject', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # User notes and customization
    user_notes = db.Column(Text, nullable=True)
    custom_title = db.Column(db.String(500), nullable=True)
    is_favorite = db.Column(db.Boolean, default=False, nullable=False)
    
    # Progress tracking
    status = db.Column(db.String(20), default='saved', nullable=False)  # saved, in_progress, completed, abandoned
    progress_percentage = db.Column(db.Integer, default=0, nullable=False)
    
    # Unique constraint to prevent duplicate saves
    __table_args__ = (db.UniqueConstraint('user_id', 'project_topic_id', name='unique_user_project_save'),)


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


# Junction table for many-to-many relationships if needed
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