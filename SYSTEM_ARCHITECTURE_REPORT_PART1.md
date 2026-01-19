# FYP Guidance System - Comprehensive Technical Report (Part 1)

## Table of Contents - Part 1
1. [Executive Summary](#executive-summary)
2. [System Overview](#system-overview)
3. [Architecture & Design Patterns](#architecture--design-patterns)
4. [Technology Stack](#technology-stack)
5. [Backend Architecture](#backend-architecture)
6. [Database Design & Models](#database-design--models)
7. [Authentication & Security](#authentication--security)

---

## Executive Summary

The **Final Year Project (FYP) Guidance System** is a comprehensive, full-stack web application designed to assist university students in discovering, planning, and managing their final year projects. The system leverages artificial intelligence for personalized project recommendations, provides collaborative workspaces for team projects, and includes robust project management tools.

### Key Statistics
- **Frontend**: Vue 3 SPA with 19+ components
- **Backend**: Dual implementation (Express.js + Flask)
- **Database Models**: 20+ tables with complex relationships
- **AI Providers**: 3 (Gemini, OpenAI, HuggingFace)
- **Real-time Features**: WebSocket support via Socket.IO
- **Authentication**: JWT + OAuth 2.0 (Google)

### Core Capabilities
✅ AI-powered project topic generation  
✅ Multi-provider AI integration with graceful fallbacks  
✅ Google OAuth 2.0 authentication  
✅ Collaborative team workspaces  
✅ Real-time chat and file sharing  
✅ Project progress tracking with phases and tasks  
✅ Proposal builder with PDF export  
✅ Favourites management system  
✅ Admin dashboard for system oversight  
✅ Activity tracking and analytics  

---

## System Overview

### Purpose & Use Case
The FYP Guidance System addresses the common challenge students face when selecting and managing their final year projects. It provides:

1. **Discovery Phase**: AI-generated project suggestions based on student profiles
2. **Planning Phase**: Proposal builder with structured templates
3. **Execution Phase**: Progress tracking, collaboration tools, and resource management
4. **Monitoring Phase**: Activity logs, analytics, and admin oversight

### System Architecture Model
**Architecture Pattern**: Hybrid Multi-Backend Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                            │
│  Vue 3 SPA (Port 3000) - Vite Dev Server                    │
│  - Components: 19 Vue components                             │
│  - Services: 10 service modules                              │
│  - State: Reactive composition API                           │
└──────────────────┬──────────────────────────────────────────┘
                   │
    ┌──────────────┴──────────────┐
    │                             │
┌───▼─────────────┐    ┌──────────▼──────────┐
│ EXPRESS BACKEND │    │   FLASK BACKEND      │
│  (Port 3001)    │    │    (Port 5000)       │
│                 │    │                      │
│ - AI Proxy      │    │ - REST API           │
│ - CORS Handler  │    │ - Authentication     │
│ - Content       │    │ - Database ORM       │
│   Filtering     │    │ - WebSocket (Socket.IO)│
└─────────────────┘    └──────────┬───────────┘
                                  │
                       ┌──────────▼───────────┐
                       │  DATABASE LAYER      │
                       │  SQLite (Dev)        │
                       │  PostgreSQL (Prod)   │
                       │  - 20+ Tables        │
                       │  - Migrations        │
                       └──────────────────────┘
```

### Deployment Architecture

**Development Environment**:
- Frontend: Vite dev server (http://localhost:3000)
- Express Backend: Nodemon (http://localhost:3001)
- Flask Backend: Flask dev server (http://localhost:5000)
- Database: SQLite (instance/app.db)

**Production Recommendations**:
- Frontend: Static build served via Nginx/Apache or CDN
- Express Backend: PM2 process manager
- Flask Backend: Gunicorn + Nginx reverse proxy
- Database: PostgreSQL with connection pooling
- WebSocket: Socket.IO with Redis adapter for scaling

---

## Architecture & Design Patterns

### 1. Dual Backend Strategy

**Why Two Backends?**

The system implements a unique dual-backend architecture for specific reasons:

#### Express Backend (`backend/server.js`)
**Purpose**: Lightweight AI proxy and content filtering

**Responsibilities**:
- Proxy Gemini API requests (CORS bypass)
- Content safety filtering
- Rate limiting for AI requests
- Response transformation

**Why Needed**:
- Gemini API has CORS restrictions
- Client-side API keys are security risks
- Centralized content moderation
- API key rotation without client updates

```javascript
// Express Backend Structure
backend/
├── server.js           # Main server file (599 lines)
├── package.json        # Node dependencies
└── .env               # API keys (GEMINI_API_KEY)
```

**Key Features**:
```javascript
// Content filtering with prohibited keywords
const PROHIBITED_KEYWORDS = [
  'terrorism', 'violence', 'hate speech', 
  'illegal activities', 'adult content'
];

// Gemini proxy endpoint
app.post('/api/generate-topics', async (req, res) => {
  // 1. Validate content
  // 2. Forward to Gemini API
  // 3. Parse and return JSON
});
```

#### Flask Backend (`backend_flask/`)
**Purpose**: Full-featured REST API with database persistence

**Responsibilities**:
- User authentication (JWT + OAuth)
- Database operations (SQLAlchemy ORM)
- Business logic and validation
- Real-time features (Socket.IO)
- File storage and management

**Why Flask**:
- Python's rich ecosystem for AI/ML
- SQLAlchemy for complex ORM relationships
- Flask-Migrate for database versioning
- Easy integration with AI libraries

```python
# Flask Backend Structure
backend_flask/
├── wsgi.py                    # Application entry point
├── app/
│   ├── __init__.py           # App factory pattern
│   ├── models.py             # 20+ database models (623 lines)
│   ├── extensions.py         # Shared extensions
│   ├── config.py             # Configuration
│   ├── sockets.py            # Socket.IO events
│   ├── auth/                 # Authentication blueprint
│   ├── admin/                # Admin blueprint
│   ├── favourites/           # Favourites blueprint
│   ├── workspaces/           # Workspaces blueprint
│   ├── chat/                 # Chat blueprint
│   ├── files/                # File management blueprint
│   ├── progress/             # Progress tracking blueprint
│   ├── projects/             # Project management blueprint
│   └── activity/             # Activity logging blueprint
├── migrations/               # Alembic migrations
└── instance/                # SQLite database (dev)
```

### 2. Frontend Architecture Patterns

#### Component Organization Strategy

**Hierarchical Component Structure**:
```
App.vue (Root)
├── Layout Components
│   ├── Header (Conditional: Student/Admin)
│   ├── Navigation
│   └── Footer
├── Page Components
│   ├── FYPForm.vue          # Main form (1000+ lines)
│   ├── FYPResults.vue       # Results display
│   ├── FavouritesPage.vue   # Favourites management
│   ├── WorkspacesPage.vue   # Workspace list
│   ├── AdminDashboard.vue   # Admin interface
│   └── FYPResources.vue     # Resource library
├── Modal Components
│   ├── AuthModal.vue        # Login/Register
│   ├── ProfileModal.vue     # User profile
│   ├── OnboardingModal.vue  # First-time setup
│   ├── ProposalBuilderModal.vue  # Multi-step proposal
│   ├── ProposalModal.vue    # Proposal viewer
│   ├── WorkspaceDetailsModal.vue
│   ├── CreateWorkspaceModal.vue
│   └── ProfileCompletionModal.vue
├── Feature Components
│   ├── ProjectProgressTracker.vue
│   ├── WorkspaceChat.vue
│   ├── WorkspaceFiles.vue
│   └── WorkspaceActivity.vue
└── Utility Components
    └── AISetupGuide.vue
```

#### Service Layer Pattern

All API communication is abstracted into service modules:

```javascript
src/services/
├── aiService.js          # AI provider abstraction
├── authService.js        # Authentication & JWT
├── favouriteService.js   # Favourites CRUD
├── workspaceService.js   # Workspace operations
├── chatService.js        # Chat messaging
├── fileService.js        # File upload/download
├── progressService.js    # Progress tracking
├── proposalService.js    # Proposal & PDF generation
├── activityService.js    # Activity logging
└── scholarService.js     # External scholarly resources
```

**Service Pattern Benefits**:
- ✅ Separation of concerns
- ✅ Reusability across components
- ✅ Centralized API configuration
- ✅ Easy testing and mocking
- ✅ Consistent error handling

#### Composition API Pattern

All components use Vue 3's Composition API for better code organization:

```javascript
// Example: FYPForm.vue
<script setup>
import { ref, computed, watch, onMounted } from 'vue'

// Reactive state
const formData = ref({ /*...*/ })
const loading = ref(false)
const error = ref('')

// Computed properties
const isFormValid = computed(() => {
  // validation logic
})

// Lifecycle hooks
onMounted(() => {
  // initialization
})

// Methods
const handleSubmit = async () => {
  // submission logic
}
</script>
```

### 3. State Management Approach

**No Centralized Store**: The application uses a distributed state management approach instead of Vuex/Pinia:

**Rationale**:
- Component-level state with Composition API
- Service modules maintain shared state
- Props/Emits for parent-child communication
- Local storage for persistence

**Auth State Example**:
```javascript
// authService.js maintains global auth state
let currentUser = null;
let isAuthenticated = false;

export const authService = {
  get currentUser() { return currentUser; },
  get isAuthenticated() { return isAuthenticated; },
  // Methods to update state
};
```

### 4. Graceful Degradation Pattern

**AI Fallback System**: The application works fully without AI API keys:

```javascript
// AI Service with fallback
class AIService {
  async generateTopics(formData) {
    try {
      if (this.isConfigured()) {
        return await this.generateWithGemini(prompt);
      } else {
        return this.getMockTopics(formData); // Intelligent mocks
      }
    } catch (error) {
      console.warn('AI failed, using mock data');
      return this.getMockTopics(formData);
    }
  }
  
  getMockTopics(formData) {
    // Generate contextually relevant mock data
    // based on student's program and interests
  }
}
```

**Benefits**:
- ✅ Development without API keys
- ✅ Demo/testing environments
- ✅ Cost control during development
- ✅ Offline capability

---

## Technology Stack

### Frontend Stack

#### Core Framework
- **Vue.js 3.5.22** (Composition API)
  - Reactive data binding
  - Component-based architecture
  - Virtual DOM for performance
  - Single File Components (SFC)

#### Build Tools
- **Vite 4.4.9**
  - Lightning-fast HMR (Hot Module Replacement)
  - ES modules-based dev server
  - Optimized production builds
  - Plugin ecosystem

#### Styling
- **Tailwind CSS 3.3.3**
  - Utility-first CSS framework
  - Custom color system (primary/secondary/accent)
  - Responsive design utilities
  - Custom components (btn-primary, card, etc.)
  - JIT (Just-In-Time) compiler

#### UI Components & Icons
- **Lucide Vue Next 0.279.0**
  - 1000+ consistent icons
  - Tree-shakeable
  - TypeScript support

#### HTTP Client
- **Axios 1.13.2**
  - Promise-based HTTP client
  - Request/response interceptors
  - Automatic JSON transformation
  - CSRF protection

#### WebSocket
- **Socket.IO Client 4.8.2**
  - Real-time bidirectional communication
  - Automatic reconnection
  - Room/namespace support

#### PDF Generation
- **jsPDF 3.0.4**
  - Client-side PDF generation
  - Custom fonts and styling
  - Multi-page support

#### Utilities
- **@vueuse/core 10.4.1**
  - Vue composition utilities
  - Browser API wrappers

### Backend Stack (Flask)

#### Core Framework
- **Flask 3.x**
  - Micro web framework
  - Werkzeug WSGI toolkit
  - Jinja2 templating (for emails)

#### Database ORM
- **SQLAlchemy 2.x**
  - Python SQL toolkit
  - ORM with relationship management
  - Query builder
  - Connection pooling

- **Flask-SQLAlchemy**
  - Flask integration for SQLAlchemy
  - Application context management

- **Flask-Migrate**
  - Alembic-based migrations
  - Version control for schema changes

#### Authentication
- **Flask-JWT-Extended**
  - JWT token generation/validation
  - Token refresh mechanism
  - Role-based access control

- **Flask-Bcrypt**
  - Password hashing (bcrypt algorithm)
  - Salt generation
  - Secure password verification

- **Authlib**
  - OAuth 2.0 client
  - Google authentication
  - Token management

#### Real-time
- **Flask-SocketIO**
  - WebSocket support
  - Room-based messaging
  - Event broadcasting

#### CORS
- **Flask-CORS**
  - Cross-Origin Resource Sharing
  - Configurable origins
  - Pre-flight request handling

### Backend Stack (Express)

#### Core Framework
- **Express.js 5.1.0**
  - Fast, minimalist web framework
  - Middleware architecture
  - Routing system

#### Utilities
- **node-fetch 3.3.2**
  - Fetch API for Node.js
  - Promise-based HTTP requests

- **dotenv 17.2.3**
  - Environment variable management

- **cors 2.8.5**
  - CORS middleware

### Database

#### Development
- **SQLite**
  - Serverless database
  - File-based storage
  - Zero configuration
  - Perfect for development

#### Production (Recommended)
- **PostgreSQL**
  - ACID compliance
  - Advanced indexing
  - JSON support
  - Full-text search
  - Scalability

### Development Tools

#### Package Management
- **npm** (Node.js)
- **pip** (Python)

#### Process Management
- **Concurrently 9.2.1**
  - Run multiple commands simultaneously
  - Colored output per process

#### Code Quality
- **Autoprefixer 10.4.15**
  - Automatic CSS vendor prefixes

- **PostCSS 8.4.29**
  - CSS transformation pipeline

---

## Backend Architecture

### Flask Application Structure

#### Application Factory Pattern

```python
# app/__init__.py
def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config())
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    init_oauth(app)
    cors.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(favourites_bp, url_prefix="/api/favourites")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")
    app.register_blueprint(workspaces_bp, url_prefix="/api/workspaces")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(files_bp, url_prefix="/api/files")
    app.register_blueprint(activity_bp, url_prefix="/api/activity")
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    
    # Register Socket.IO events
    register_socket_events(socketio)
    
    return app
```

**Benefits**:
- ✅ Multiple app instances (testing, production)
- ✅ Clean configuration management
- ✅ Extension initialization order control
- ✅ Easy blueprint registration

#### Blueprint Architecture

Blueprints organize the application into modular components:

**Auth Blueprint** (`app/auth/routes.py`):
```python
auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")      # User registration
@auth_bp.post("/login")          # Email/password login
@auth_bp.get("/google/login")    # Google OAuth initiation
@auth_bp.get("/google/callback") # Google OAuth callback
@auth_bp.get("/me")              # Get current user
@auth_bp.put("/profile")         # Update profile
@auth_bp.post("/onboarding")     # Complete onboarding
```

**Favourites Blueprint** (`app/favourites/routes.py`):
```python
favourites_bp = Blueprint("favourites", __name__)

@favourites_bp.get("/")                    # List favourites
@favourites_bp.post("/")                   # Add favourite
@favourites_bp.get("/<int:id>")            # Get favourite details
@favourites_bp.put("/<int:id>")            # Update favourite
@favourites_bp.delete("/<int:id>")         # Delete favourite
@favourites_bp.post("/<int:id>/progress")  # Enable progress tracking
```

**Workspaces Blueprint** (`app/workspaces/routes.py`):
```python
workspaces_bp = Blueprint("workspaces", __name__)

@workspaces_bp.get("/")                          # List workspaces
@workspaces_bp.post("/")                         # Create workspace
@workspaces_bp.get("/<int:id>")                  # Get workspace details
@workspaces_bp.put("/<int:id>")                  # Update workspace
@workspaces_bp.delete("/<int:id>")               # Delete workspace
@workspaces_bp.get("/discover")                  # Discover public workspaces
@workspaces_bp.post("/<int:id>/join")            # Join public workspace
@workspaces_bp.post("/<int:id>/leave")           # Leave workspace
@workspaces_bp.post("/<int:id>/invite")          # Invite member
@workspaces_bp.post("/<int:id>/members/<int:mid>/role")  # Update member role
@workspaces_bp.delete("/<int:id>/members/<int:mid>")     # Remove member
```

**Admin Blueprint** (`app/admin/routes.py`):
```python
admin_bp = Blueprint("admin", __name__)

# Requires @admin_required decorator
@admin_bp.get("/users")                   # List all users
@admin_bp.get("/stats")                   # System statistics
@admin_bp.put("/users/<int:id>/role")     # Change user role
@admin_bp.delete("/users/<int:id>")       # Delete user
```

#### Middleware & Decorators

**JWT Authentication**:
```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@favourites_bp.get("/")
@jwt_required()  # Validates JWT token
def get_favourites():
    user_id = int(get_jwt_identity())
    # ... route logic
```

**Admin Authorization**:
```python
# app/admin/__init__.py
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user or not user.is_admin():
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper
```

#### Error Handling

**Global Error Handlers**:
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "Internal server error"}), 500
```

**JWT Error Handlers**:
```python
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Invalid token"}), 401
```

---

## Database Design & Models

### Entity Relationship Overview

The database consists of 20+ interconnected tables organized into logical domains:

#### 1. User & Authentication Domain

**User Model** (Core):
```python
class User(db.Model):
    # Identity
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)  # OAuth users: null
    
    # OAuth
    google_id = db.Column(db.String(255), unique=True, nullable=True)
    auth_provider = db.Column(db.String(20), default='email')  # 'email' | 'google'
    
    # Profile
    full_name = db.Column(db.String(255))
    university = db.Column(db.String(255))
    program = db.Column(db.String(100))
    academic_year = db.Column(db.String(10))
    interests = db.Column(JSON)  # Array of strings
    skills = db.Column(JSON)     # Array of strings
    
    # Preferences
    project_preference = db.Column(db.String(50))  # Research/Development/Both
    expected_duration = db.Column(db.String(20))
    
    # Status
    onboarding_completed = db.Column(db.Boolean, default=False)
    role = db.Column(db.String(20), default='student')  # 'student' | 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    saved_projects = db.relationship('SavedProject', backref='user', cascade='all, delete-orphan')
    owned_workspaces = db.relationship('Workspace', foreign_keys='Workspace.owner_id')
    workspace_memberships = db.relationship('WorkspaceMember', backref='user')
```

**StudentProfile Model** (Extended Profile):
```python
class StudentProfile(db.Model):
    """Detailed student information from forms"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Academic info
    student_id = db.Column(db.String(50))
    program = db.Column(db.String(100))
    academic_year = db.Column(db.String(10))
    
    # Skills & Interests
    skills_text = db.Column(Text)
    interests_text = db.Column(Text)
    
    # Project preferences
    difficulty_preference = db.Column(db.String(20))
    duration_preference = db.Column(db.String(20))
    project_type = db.Column(db.String(50))
    supervisor_name = db.Column(db.String(255))
    budget_range = db.Column(db.String(20))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
```

#### 2. Project Domain

**ProjectTopic Model** (Master Projects Table):
```python
class ProjectTopic(db.Model):
    """Master table for all project topics"""
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Info
    title = db.Column(db.String(500), nullable=False, index=True)
    description = db.Column(Text, nullable=False)
    difficulty = db.Column(db.String(20))  # Beginner/Intermediate/Advanced
    duration = db.Column(db.String(20))    # e.g., "6-8 months"
    
    # Extended Details
    objectives = db.Column(JSON)           # Array of objectives
    methodology = db.Column(Text)
    expected_outcomes = db.Column(Text)
    
    # Categorization
    program_area = db.Column(db.String(100), index=True)
    tags = db.Column(JSON)                 # Array of tags
    
    # Source Tracking
    source_type = db.Column(db.String(20), default='generated')
    # 'generated' | 'predefined' | 'template'
    ai_provider = db.Column(db.String(20))  # 'gemini' | 'openai' | 'huggingface'
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    skills = db.relationship('ProjectSkill', cascade='all, delete-orphan')
    resources = db.relationship('ProjectResource', cascade='all, delete-orphan')
```

**ProjectSkill Model**:
```python
class ProjectSkill(db.Model):
    """Skills required for each project"""
    id = db.Column(db.Integer, primary_key=True)
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'))
    
    skill_name = db.Column(db.String(100), index=True)
    skill_level = db.Column(db.String(20))  # basic/intermediate/advanced
    is_required = db.Column(db.Boolean, default=True)
```

**ProjectResource Model**:
```python
class ProjectResource(db.Model):
    """Resources for projects"""
    id = db.Column(db.Integer, primary_key=True)
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'))
    
    resource_type = db.Column(db.String(20))  # Paper/Tutorial/Tool/Book/Course
    title = db.Column(db.String(300))
    description = db.Column(Text)
    url = db.Column(db.String(500))
    author = db.Column(db.String(200))
    publication_year = db.Column(db.Integer)
```

**SavedProject Model** (User's Projects):
```python
class SavedProject(db.Model):
    """Projects saved/bookmarked by users"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_topic_id = db.Column(db.Integer, db.ForeignKey('project_topic.id'))
    
    # Customization
    user_notes = db.Column(Text)
    custom_title = db.Column(db.String(500))
    is_favorite = db.Column(db.Boolean, default=False)
    
    # Progress Tracking
    status = db.Column(db.String(20), default='saved')
    # 'saved' | 'not_started' | 'in_progress' | 'completed' | 'abandoned'
    progress_percentage = db.Column(db.Integer, default=0)
    progress_tracking_enabled = db.Column(db.Boolean, default=False)
    
    # Timeline
    start_date = db.Column(db.DateTime)
    expected_completion_date = db.Column(db.DateTime)
    actual_completion_date = db.Column(db.DateTime)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    phases = db.relationship('ProjectPhase', back_populates='saved_project', 
                            cascade='all, delete-orphan')
    project_topic = db.relationship('ProjectTopic')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'project_topic_id'),
    )
```

#### 3. Progress Tracking Domain

**ProjectPhase Model**:
```python
class ProjectPhase(db.Model):
    """Phases/milestones within a project"""
    id = db.Column(db.Integer, primary_key=True)
    saved_project_id = db.Column(db.Integer, db.ForeignKey('saved_project.id'))
    
    # Phase Details
    phase_name = db.Column(db.String(100))
    phase_order = db.Column(db.Integer)  # 1, 2, 3...
    description = db.Column(Text)
    
    # Timeline
    estimated_duration_weeks = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    actual_completion_date = db.Column(db.DateTime)
    
    # Status
    status = db.Column(db.String(20), default='not_started')
    # 'not_started' | 'in_progress' | 'completed' | 'blocked'
    progress_percentage = db.Column(db.Integer, default=0)
    notes = db.Column(Text)
    
    # Relationships
    saved_project = db.relationship('SavedProject', back_populates='phases')
    tasks = db.relationship('PhaseTask', cascade='all, delete-orphan')
```

**PhaseTask Model**:
```python
class PhaseTask(db.Model):
    """Individual tasks within phases"""
    id = db.Column(db.Integer, primary_key=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('project_phase.id'))
    
    task_name = db.Column(db.String(300))
    description = db.Column(Text)
    task_order = db.Column(db.Integer)
    
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    due_date = db.Column(db.DateTime)
    
    phase = db.relationship('ProjectPhase', back_populates='tasks')
```

#### 4. Collaboration Domain

**Workspace Model**:
```python
class Workspace(db.Model):
    """Collaborative workspace for teams"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(Text)
    
    # Ownership
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Project Link
    saved_project_id = db.Column(db.Integer, db.ForeignKey('saved_project.id'))
    
    # Settings
    is_public = db.Column(db.Boolean, default=False)  # Discoverable
    max_members = db.Column(db.Integer, default=10)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    owner = db.relationship('User', foreign_keys=[owner_id])
    members = db.relationship('WorkspaceMember', cascade='all, delete-orphan')
    messages = db.relationship('WorkspaceMessage', backref='workspace')
    files = db.relationship('WorkspaceFile', backref='workspace')
    activities = db.relationship('WorkspaceActivity', backref='workspace')
```

**WorkspaceMember Model**:
```python
class WorkspaceMember(db.Model):
    """Members in a workspace"""
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Permissions
    role = db.Column(db.String(20), default='member')
    # 'owner' | 'admin' | 'member' | 'viewer'
    can_edit = db.Column(db.Boolean, default=True)
    can_invite = db.Column(db.Boolean, default=False)
    
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('workspace_id', 'user_id'),
    )
```

**WorkspaceMessage Model**:
```python
class WorkspaceMessage(db.Model):
    """Chat messages in workspace"""
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    message = db.Column(Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text/file/system
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**WorkspaceFile Model**:
```python
class WorkspaceFile(db.Model):
    """Files shared in workspace"""
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    filename = db.Column(db.String(255))
    original_filename = db.Column(db.String(255))
    file_size = db.Column(db.Integer)  # bytes
    file_type = db.Column(db.String(100))  # MIME type
    file_path = db.Column(db.String(500))  # storage path
    description = db.Column(Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**WorkspaceActivity Model**:
```python
class WorkspaceActivity(db.Model):
    """Activity feed for workspace"""
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    activity_type = db.Column(db.String(50), index=True)
    # member_joined, file_uploaded, message_sent, etc.
    description = db.Column(Text)
    activity_data = db.Column(JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
```

### Database Relationships Diagram

```
User (1) ──────< (N) SavedProject (N) ────── (1) ProjectTopic
  │                      │                            │
  │                      │                            ├──< ProjectSkill
  │                      │                            └──< ProjectResource
  │                      │
  │                      └──< ProjectPhase
  │                              └──< PhaseTask
  │
  ├──< Workspace (as owner)
  │       │
  │       ├──< WorkspaceMember
  │       ├──< WorkspaceMessage
  │       ├──< WorkspaceFile
  │       └──< WorkspaceActivity
  │
  └──< WorkspaceMember (as member)
```

### Database Indexing Strategy

**Primary Indexes**:
- All `id` columns (auto-indexed as primary keys)
- `user.email` (unique index for fast lookups)
- `user.google_id` (unique index for OAuth)

**Performance Indexes**:
- `project_topic.title` (for search)
- `project_topic.program_area` (for filtering)
- `workspace_activity.created_at` (for timeline queries)
- `user_activity.user_id + activity_type + created_at` (composite)

### Database Migration System

**Alembic Migrations** (via Flask-Migrate):

```bash
# Create migration
flask --app wsgi db migrate -m "Description"

# Apply migration
flask --app wsgi db upgrade

# Rollback
flask --app wsgi db downgrade
```

**Migration Files Location**:
```
migrations/
├── alembic.ini
├── env.py
├── script.py.mako
└── versions/
    ├── xxxx_initial_schema.py
    ├── xxxx_add_workspaces.py
    └── xxxx_add_progress_tracking.py
```

---

## Authentication & Security

### Authentication Mechanisms

#### 1. Email/Password Authentication

**Registration Flow**:
```python
@auth_bp.post("/register")
def register():
    # 1. Validate email and password
    # 2. Check if email exists
    # 3. Hash password with bcrypt
    user = User(email=email, auth_provider='email')
    user.set_password(password)  # bcrypt hashing
    # 4. Save to database
    # 5. Return user data (no auto-login)
```

**Login Flow**:
```python
@auth_bp.post("/login")
def login():
    # 1. Find user by email
    # 2. Verify password with bcrypt
    if not user.check_password(password):
        return error
    # 3. Generate JWT token
    token = create_access_token(identity=str(user.id))
    # 4. Return token + user data
```

**Password Security**:
- **Bcrypt hashing** with automatic salt generation
- **Work factor**: 12 rounds (configurable)
- **No plain-text storage** ever
- **Password validation**: Minimum length enforced client-side

#### 2. Google OAuth 2.0

**OAuth Flow**:
```
1. User clicks "Sign in with Google"
   ↓
2. Frontend redirects to /api/auth/google/login
   ↓
3. Backend redirects to Google OAuth consent page
   ↓
4. User approves access
   ↓
5. Google redirects to /api/auth/google/callback
   ↓
6. Backend exchanges code for access token
   ↓
7. Backend fetches user info from Google
   ↓
8. Backend creates/updates user in database
   ↓
9. Backend generates JWT token
   ↓
10. Frontend receives token via URL parameter
```

**Implementation**:
```python
@auth_bp.get("/google/login")
def google_login():
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.get("/google/callback")
def google_callback():
    # Get access token
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')
    
    # Extract user data
    google_id = user_info.get('sub')
    email = user_info.get('email')
    full_name = user_info.get('name')
    
    # Find or create user
    user = User.query.filter_by(google_id=google_id).first()
    if not user:
        user = User(
            email=email,
            full_name=full_name,
            google_id=google_id,
            auth_provider='google'
        )
        db.session.add(user)
    
    db.session.commit()
    
    # Generate JWT
    jwt_token = create_access_token(identity=str(user.id))
    
    # Redirect to frontend with token
    return redirect(f"{FRONTEND_URL}?token={jwt_token}")
```

### JWT Token System

#### Token Structure

**Claims**:
```json
{
  "sub": "123",           // User ID
  "iat": 1703620800,      // Issued at
  "exp": 1703707200,      // Expiration (24 hours)
  "type": "access",       // Token type
  "fresh": false,         // Fresh login flag
  "jti": "unique-id"      // JWT ID
}
```

**Token Lifecycle**:
1. **Generation**: After successful login/OAuth
2. **Storage**: Frontend stores in localStorage
3. **Usage**: Sent in `Authorization: Bearer <token>` header
4. **Validation**: Backend validates on each protected request
5. **Expiration**: 24 hours (configurable)
6. **Refresh**: Re-login required (refresh tokens not implemented)

#### Protected Routes

**Decorator Usage**:
```python
from flask_jwt_extended import jwt_required, get_jwt_identity

@favourites_bp.get("/")
@jwt_required()  # Validates JWT token
def get_favourites():
    user_id = int(get_jwt_identity())  # Extract user ID from token
    # ... business logic
```

**Frontend Integration**:
```javascript
// authService.js
class AuthService {
  getAuthHeader() {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
  
  async fetchProtectedResource() {
    const response = await axios.get('/api/favourites', {
      headers: this.getAuthHeader()
    });
    return response.data;
  }
}
```

### Authorization & Roles

#### Role-Based Access Control (RBAC)

**User Roles**:
- **student** (default): Regular user access
- **admin**: Full system access + admin panel

**Admin Decorator**:
```python
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user or user.role != 'admin':
            return jsonify({"error": "Admin access required"}), 403
        
        return fn(*args, **kwargs)
    return wrapper

# Usage
@admin_bp.get("/users")
@admin_required
def list_users():
    # Only admins can access
```

**Workspace Permissions**:
```python
class WorkspaceMember(db.Model):
    role = db.Column(db.String(20))  # owner/admin/member/viewer
    can_edit = db.Column(db.Boolean, default=True)
    can_invite = db.Column(db.Boolean, default=False)
```

**Permission Checks**:
```python
def check_workspace_permission(workspace_id, user_id, required_permission):
    workspace = Workspace.query.get(workspace_id)
    
    # Owner has all permissions
    if workspace.owner_id == user_id:
        return True
    
    # Check member permissions
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id,
        user_id=user_id
    ).first()
    
    if not member:
        return False
    
    if required_permission == 'edit':
        return member.can_edit
    elif required_permission == 'invite':
        return member.can_invite
    
    return True  # viewer access
```

### Security Best Practices Implemented

✅ **Password Security**:
- Bcrypt hashing with salt
- No plain-text passwords
- Minimum length requirements

✅ **Token Security**:
- JWT with expiration
- Secure token generation
- HttpOnly cookies (recommended for production)

✅ **CORS Configuration**:
```python
cors.init_app(app, resources={
    r"/api/*": {
        "origins": "*",  # Configure for production
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
```

✅ **SQL Injection Prevention**:
- SQLAlchemy ORM (parameterized queries)
- No raw SQL execution

✅ **XSS Protection**:
- Vue.js automatic escaping
- Content-Type headers

✅ **CSRF Protection**:
- JWT tokens (stateless)
- SameSite cookie attribute (recommended)

✅ **Content Filtering**:
- Prohibited keyword list (Express backend)
- AI content validation

### Security Recommendations for Production

🔒 **Environment Variables**:
```bash
# Use strong, random secrets
SECRET_KEY=<64-char-random-string>
JWT_SECRET_KEY=<64-char-random-string>

# Secure database URL
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# API keys in environment
GEMINI_API_KEY=<key>
GOOGLE_CLIENT_ID=<id>
GOOGLE_CLIENT_SECRET=<secret>
```

🔒 **HTTPS**:
- SSL/TLS certificates (Let's Encrypt)
- Redirect HTTP to HTTPS
- HSTS headers

🔒 **Rate Limiting**:
```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@auth_bp.post("/login")
@limiter.limit("5 per minute")  # Prevent brute force
def login():
    # ...
```

🔒 **Token Storage**:
- Use HttpOnly cookies instead of localStorage
- Implement refresh token rotation

🔒 **Database Security**:
- Use prepared statements (SQLAlchemy ORM)
- Principle of least privilege for DB user
- Regular backups

---

## End of Part 1

Continue to [SYSTEM_ARCHITECTURE_REPORT_PART2.md](./SYSTEM_ARCHITECTURE_REPORT_PART2.md) for:
- Frontend Architecture Details
- AI Integration & Services
- Real-time Features (WebSockets)
- API Endpoints Reference
- Deployment Guide
- Performance Optimization
- Testing Strategies
- Troubleshooting Guide

---

**Document Version**: 1.0  
**Last Updated**: December 26, 2025  
**Author**: FYP Guidance System Development Team
