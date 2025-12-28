# FYP Guidance System - Use Cases and Activity Diagrams
## Core Functionality Documentation

---

## 1. Use Case Diagram

### System Actors
- **Student**: Primary user who uses the system for FYP guidance
- **Admin**: System administrator who manages users and analytics
- **AI Service**: External AI provider (Google Gemini/OpenAI/HuggingFace)
- **Database**: Backend database (SQLite with Flask-SQLAlchemy)
- **Google OAuth**: Third-party authentication provider

### How to Draw the Use Case Diagram

#### Step 1: Draw the Actors (Stick Figures)

**On the LEFT side of your diagram:**
- Draw a stick figure labeled **"Student"**

**On the RIGHT side of your diagram:**
- Draw a stick figure labeled **"AI Service"**
- Below it, draw another stick figure labeled **"Database"**

#### Step 2: Draw the System Boundary

In the center, draw a **large rectangle** that will contain all use cases. Label it at the top: **"FYP Guidance System"**

#### Step 3: Draw the Use Cases (Ovals)

Inside the system boundary rectangle, draw **ovals** for each use case. Arrange them in groups:

**Top Section (Authentication):**
- Oval: "UC1: Register Account"
- Oval: "UC2: Login to System"
- Oval: "UC2A: Login with Google OAuth"

**Second Section (User Onboarding):**
- Oval: "UC3: Complete Onboarding"
- Oval: "UC4: Complete Student Profile"

**Third Section (Topic Discovery):**
- Oval: "UC5: Discover Research Topics"
- Oval: "UC6: Generate AI Topic Recommendations" (place to the right of UC5)
- Oval: "UC7: Save Favorite Projects"

**Fourth Section (Proposal Building):**
- Oval: "UC8: Build Project Proposal"
- Oval: "UC9: Generate Proposal Sections (AI)" (place to the right of UC8)
- Oval: "UC10: Download Proposal as PDF"

**Fifth Section (Project Management):**
- Oval: "UC11: Track Project Progress"
- Oval: "UC12: Manage Favourites"

**Sixth Section (Collaboration):**
- Oval: "UC13: Create Workspace"
- Oval: "UC14: Collaborate on Project"
- Oval: "UC15: Real-time Chat"
- Oval: "UC16: Share Files"

**Bottom Section (Admin):**
- Oval: "UC17: Admin Dashboard"
- Oval: "UC18: Manage Users"
- Oval: "UC19: View Analytics"

#### Step 4: Draw Associations (Solid Lines)

Draw **solid lines** from the Student actor to these use cases:
- Student → UC1 (Register Account)
- Student → UC2 (Login to System)
- Student → UC2A (Login with Google OAuth)
- Student → UC3 (Complete Onboarding)
- Student → UC4 (Complete Student Profile)
- Student → UC5 (Discover Research Topics)
- Student → UC7 (Save Favorite Projects)
- Student → UC8 (Build Project Proposal)
- Student → UC10 (Download Proposal as PDF)
- Student → UC11 (Track Project Progress)
- Student → UC12 (Manage Favourites)
- Student → UC13 (Create Workspace)
- Student → UC14 (Collaborate on Project)
- Student → UC15 (Real-time Chat)
- Student → UC16 (Share Files)

Draw **solid lines** from the Admin actor to these use cases:
- Admin → UC17 (Admin Dashboard)
- Admin → UC18 (Manage Users)
- Admin → UC19 (View Analytics)

#### Step 5: Draw Include Relationships (Dashed Arrows)

Draw **dashed arrows** with **<<includes>>** label:
- UC2 → UC2A (arrow from "Login to System" to "Login with Google OAuth")
- UC5 → UC6 (arrow from "Discover Research Topics" to "Generate AI Topic Recommendations")
- UC8 → UC9 (arrow from "Build Project Proposal" to "Generate Proposal Sections")
- UC14 → UC15 (arrow from "Collaborate on Project" to "Real-time Chat")
- UC14 → UC16 (arrow from "Collaborate on Project" to "Share Files")
- UC17 → UC18 (arrow from "Admin Dashboard" to "Manage Users")
- UC17 → UC19 (arrow from "Admin Dashboard" to "View Analytics")

**Note**: These arrows should be dashed/dotted, not solid, and point from the main use case to the included functionality.

#### Step 6: Draw Extend Relationship (Dashed Arrow)

Draw **dashed arrow** with **<<extends>>** label:
- UC10 → UC8 (arrow from "Download Proposal as PDF" to "Build Project Proposal")
- UC2A → UC2 (arrow from "Login with Google OAuth" to "Login to System")
- UC11 → UC12 (arrow from "Track Project Progress" to "Manage Favourites")

#### Step 7: Draw External System Interactions (Solid Lines to Actors)

Draw **solid lines** from use cases to external actors:

**To Database:**
- UC1 → Database (label: "creates user")
- UC2 → Database (label: "authenticates")
- UC2A → Database (label: "creates/retrieves OAuth user")
- UC4 → Database (label: "updates profile")
- UC6 → Database (label: "retrieves profile data")
- UC7 → Database (label: "persists favourites")
- UC9 → Database (label: "saves proposal sections")
- UC11 → Database (label: "tracks progress")
- UC12 → Database (label: "queries favourites")
- UC13 → Database (label: "creates workspace")
- UC14 → Database (label: "stores collaboration data")
- UC18 → Database (label: "manages user records")
- UC19 → Database (label: "queries analytics")

**To AI Service:**
- UC6 → AI Service (label: "generates topics")
- UC9 → AI Service (label: "generates proposal content")

**To Google OAuth:**
- UC2A → Google OAuth (label: "authenticates")

### Diagram Legend

**Line Types:**
- **Solid line**: Direct association (actor uses use case)
- **Dashed arrow with <<includes>>**: Required functionality included in main use case
- **Dashed arrow with <<extends>>**: Optional additional behavior
- **Solid line to external actor**: External system dependency

**Arrow Directions:**
- Associations: No arrowheads or simple lines
- Include: Arrow points from main use case to included use case
- Extend: Arrow points from extending use case to base use case
- External systems: Arrow points from use case to external actor

---

## 2. Core Use Case Specifications

### UC1: Register Account

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants quick, secure account creation
- System: Needs to validate and store user data securely

**Preconditions:** None  
**Postconditions:**
- New user account created in database
- Password stored as bcrypt hash (if email registration)
- User can authenticate with credentials
- User marked for onboarding

**Main Success Scenario:**
1. Student navigates to registration page
2. System displays registration form (Email, Password, Confirm Password)
3. Student enters registration details
4. Student submits form
5. System validates input data client-side
6. System sends POST request to `/api/auth/register`
7. Backend validates data server-side
8. Backend checks email uniqueness in database
9. Backend hashes password using bcrypt (cost factor 12)
10. Backend creates User record in SQLite database with role='student'
11. Backend returns 201 Created with user data (id, email)
12. System displays success notification
13. System redirects to login page

**Alternative Flows:**
- **5a. Validation fails:**
  - System displays inline error messages
  - System highlights invalid fields
  - User corrects errors and resubmits
  
- **8a. Email already registered:**
  - Backend returns 409 Conflict error
  - System displays "Email already in use" error
  - User can try different email or login instead

**Special Requirements:**
- Password must be minimum 8 characters
- Email must be valid format and lowercase
- Bcrypt cost factor: 12 for security
- Response time: < 2 seconds
- Auth provider field set to 'email'

**Technology/Data Variations:**
- Frontend: Vue 3 Composition API (AuthModal.vue)
- Backend: Flask with Flask-SQLAlchemy
- Database: SQLite (User model)
- Password hashing: bcrypt library

---

### UC2: Login to System

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants secure, fast access to account
- System: Needs to verify identity and maintain session

**Preconditions:** Student has registered account  
**Postconditions:**
- JWT access token generated and stored
- User session established
- User can access protected routes
- Onboarding modal shown if not completed

**Main Success Scenario:**
1. Student navigates to login page
2. System displays login form (Email, Password) or Google OAuth button
3. Student enters credentials
4. Student clicks "Login" button
5. System sends POST to `/api/auth/login`
6. Backend queries User by email from database
7. Backend verifies password using `bcrypt.check_password_hash()`
8. Backend generates JWT access token:
   - Identity: user_id (as string)
   - No explicit expiration (uses Flask-JWT-Extended defaults)
   - Signed with JWT_SECRET_KEY
9. Backend returns token and user data (id, email, role, onboarding_completed)
10. Frontend stores token in authService
11. Frontend stores user data in application state
12. System checks onboarding_completed flag
13. If not completed: Show OnboardingModal
14. System redirects to dashboard
15. Dashboard displays personalized content

**Alternative Flows:**
- **6a. Email not found:**
  - Backend returns 401 Unauthorized
  - System displays "Invalid credentials" (no user enumeration)
  - User can retry or register
  
- **7a. Password incorrect:**
  - Backend returns 401 Unauthorized
  - System displays "Invalid credentials"
  - Failed attempt logged for security monitoring
  
- **OAuth Login Flow** (UC2A):
  - Student clicks "Sign in with Google"
  - System redirects to `/api/auth/google/login`
  - Google authenticates user
  - System redirects to `/api/auth/google/callback`
  - Backend creates/retrieves user with google_id and auth_provider='google'
  - Backend generates JWT token
  - Frontend redirects to success page with token in URL
  - System extracts token and completes login

**Special Requirements:**
- JWT token handled by Flask-JWT-Extended
- Secure password comparison (constant time)
- No user enumeration in error messages
- Support both email and Google OAuth authentication
- Token must be sent in Authorization: Bearer header

**Frequency of Use:** Multiple times per day per user

---

### UC2A: Login with Google OAuth

**Primary Actor:** Student, Google OAuth Service  
**Stakeholders and Interests:**
- Student: Wants quick login without password
- Google: Authenticates user identity
- System: Securely creates/retrieves user account

**Preconditions:** 
- Google OAuth configured (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
- User has Google account

**Postconditions:**
- User authenticated via Google
- User record created or retrieved in database
- JWT token generated
- User logged in

**Main Success Scenario:**
1. Student clicks "Sign in with Google" button
2. System sends GET to `/api/auth/google/login`
3. Backend initiates OAuth flow with Google
4. User redirected to Google login page
5. User authenticates with Google credentials
6. User grants permission to app
7. Google redirects to `/api/auth/google/callback` with auth code
8. Backend exchanges code for user info (email, google_id, name)
9. Backend checks if user exists by google_id or email
10. **IF user exists:**
    - Backend retrieves existing user
11. **IF user doesn't exist:**
    - Backend creates new User with:
      - email (from Google)
      - google_id (from Google)
      - auth_provider='google'
      - password_hash=None (no password needed)
      - role='student'
      - onboarding_completed=False
12. Backend generates JWT access token
13. Backend redirects to frontend with token in URL
14. Frontend extracts token from URL
15. Frontend stores token and completes login flow

**Alternative Flows:**
- **3a. OAuth not configured:**
  - Backend returns 500 error: "Google OAuth not configured"
  - System displays error to user
  
- **6a. User denies permission:**
  - Google redirects with error
  - System displays "Login cancelled"
  
- **7a. Callback error:**
  - Backend catches OAuth error
  - System logs error
  - System redirects to login with error message

**Special Requirements:**
- Requires GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in .env
- Uses Authlib library for OAuth
- No password stored for OAuth users
- Users can have both email and Google auth on same email

**Technology/Data Variations:**
- OAuth Library: Authlib
- Google API: OpenID Connect
- Redirect URIs must be configured in Google Console

---

### UC3: Complete Onboarding

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants guided introduction to system features
- System: Wants to educate new users and improve retention

**Preconditions:** 
- Student is authenticated
- onboarding_completed = False

**Postconditions:**
- User understands core features
- onboarding_completed flag set to True in database
- User can proceed to use system

**Main Success Scenario:**
1. System detects new user (onboarding_completed = False)
2. System displays OnboardingModal full-screen overlay
3. System shows welcome screen with:
   - Step 1/4 indicator
   - Progress bar
   - "Welcome to FYP Guidance!" message
4. Student reads introduction
5. Student clicks "Next" button
6. System advances to Step 2: "Generate Project Topics"
   - Explains AI-powered topic generation
   - Shows example topic cards
7. Student clicks "Next"
8. System advances to Step 3: "Build Your Proposal"
   - Explains proposal builder feature
   - Shows step-by-step preview
9. Student clicks "Next"
10. System advances to Step 4: "Track Your Progress"
    - Explains favourites and progress tracking
    - Shows workspace collaboration preview
11. Student clicks "Get Started" button
12. System sends PUT to `/api/user/onboarding-complete`
13. Backend updates User.onboarding_completed = True
14. System closes modal
15. System shows dashboard

**Alternative Flows:**
- **Any step: Student clicks "Skip":**
  - System shows confirmation: "Skip onboarding?"
  - If confirmed:
    - System calls onboarding complete endpoint
    - System closes modal
  
- **Student closes modal without completing:**
  - System remembers incomplete state
  - Onboarding shown again on next login

**Special Requirements:**
- Non-blocking: User can skip anytime
- Animated transitions between steps
- Progress indicator shows completion percentage
- Icons change per step (Sparkles, FileText, BookOpen, Target)

**Technology/Data Variations:**
- Component: OnboardingModal.vue
- State management: Local ref + backend persistence
- Animations: Tailwind transitions

---

### UC4: Complete Student Profile

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants personalized recommendations
- AI Service: Needs context for generating relevant content
- System: Needs profile data for matching algorithms

**Preconditions:** Student is authenticated  
**Postconditions:**
- User profile fields updated in database
- Profile data available for AI context
- Enhanced personalization enabled

**Main Success Scenario:**
1. Student navigates to Profile page or clicks "Edit Profile" from dropdown
2. System displays profile modal/form with sections:
   - **Basic Info**: Full Name, University, Program, Academic Year
   - **Interests**: Comma-separated interest areas (stored as JSON array)
   - **Skills**: Comma-separated skills (stored as JSON array)
   - **Project Preferences**: Project type, Expected duration
3. Student fills in fields
4. System validates each field on input (real-time validation)
5. Student clicks "Save Profile"
6. System validates entire form
7. System sends PUT to `/api/user/profile` with profile data
8. Backend updates User record fields:
   - full_name, university, program, academic_year
   - interests (JSON array)
   - skills (JSON array)
   - project_preference, expected_duration
9. Backend returns 200 OK with updated user data
10. System displays "Profile updated successfully" notification
11. System updates global user state
12. System closes profile modal

**Alternative Flows:**
- **6a. Validation errors:**
  - System highlights invalid fields
  - System displays error messages
  - Student corrects fields
  
- **8a. Database update fails:**
  - Backend returns 500 error
  - System displays "Failed to save. Please try again."
  - Form data remains populated for retry

**Special Requirements:**
- Profile is not required to be complete to use system
- Interests and skills stored as JSON arrays in database
- Form accessible from user dropdown menu
- Mobile-responsive form layout

**Business Rules:**
- Profile completion enhances AI recommendations
- All fields optional (system works without profile)
- Interests/skills can be comma or newline separated

---

### UC5: Discover Research Topics

**Primary Actor:** Student, AI Service  
**Stakeholders and Interests:**
- Student: Wants relevant, innovative project ideas
- AI Service: Generates contextual recommendations
- System: Provides graceful degradation if AI unavailable

**Preconditions:** 
- Student is authenticated

**Postconditions:**
- Topics displayed to student (AI-generated or mock data)
- Topics can be saved as favorites
- Student can proceed to build proposal from topic
- Generation tracked in GeneratedProject table

**Main Success Scenario:**
1. Student navigates to home page
2. System displays FYPForm interface:
   - Student Name, Student ID, Program, Academic Year
   - Skills (comma-separated text)
   - Interests (comma-separated text)
   - Difficulty preference dropdown
   - Duration preference dropdown
   - Project type selection
   - Additional requirements (optional text)
   - Supervisor name (optional)
   - Budget range (optional)
3. Student fills form fields
4. Student clicks "Generate Project Topics" button
5. System shows loading state (spinner animation)
6. **System executes UC6 (Generate AI Topic Recommendations)**
7. System receives AI-generated topics array (typically 3 topics)
8. System sends POST to `/api/projects/track-generation` to persist:
   - project_topics array
   - form_data snapshot
   - ai_provider used
   - session_id
9. Backend creates ProjectTopic and GeneratedProject records
10. System displays topics in FYPResults component:
    - Each topic card showing:
      - Title (bold heading)
      - Description (2-3 paragraphs)
      - Difficulty badge (color-coded)
      - Duration estimate
      - Objectives (bullet points)
      - Methodology (paragraph)
      - Expected Outcomes (paragraph)
      - Skills required (tags)
      - Resources (expandable list with links)
      - Tags (category badges)
    - Action buttons per card:
      - "Save to Favourites" (heart icon)
      - "Build Proposal" button
11. Student reviews generated topics
12. Student can:
    - Save topic to favourites (UC7)
    - Build proposal from topic (UC8)
    - Regenerate with different form inputs

**Alternative Flows:**
- **6a. AI service unavailable or fails:**
  - System automatically falls back to intelligent mock data
  - Mock topics filtered by selected difficulty/project type
  - Mock topics incorporate student's program in descriptions
  - Subtle notification: "Using sample topics (AI unavailable)"
  - No tracking sent to backend (mock data)
  
- **8a. Generation tracking fails:**
  - System logs error but doesn't block display
  - Topics still shown to user
  - Student can proceed with all actions
  
- **7a. No topics generated (empty response):**
  - System displays error state
  - System provides helpful message: "Failed to generate topics"
  - System suggests: "Please try again or adjust your inputs"

**Special Requirements:**
- **Performance**: Display topics within 10-15 seconds
- **Graceful degradation**: System fully functional without AI
- **Responsive design**: Cards stack vertically on mobile
- **Animations**: Results fade in smoothly

**Technology Variations:**
- **AI Provider Options**: Gemini (via backend), OpenAI (direct), HuggingFace
- **Fallback Strategy**: AI → Intelligent Mock Data
- **Form Component**: FYPForm.vue
- **Results Component**: FYPResults.vue

---

### UC6: Generate AI Topic Recommendations

**Primary Actor:** AI Service  
**Stakeholders and Interests:**
- Student: Wants contextually relevant, innovative topics
- AI Service: Generates based on student form data
- System: Manages API calls, timeouts, error handling

**Preconditions:**
- Student has filled form with skills and interests
- AI service may or may not be configured
- Network connectivity available (for AI calls)

**Postconditions:**
- AI-generated topics returned to UC5 (or mock data)
- Topics contextually relevant to student
- Each topic has required fields

**Main Success Scenario:**
1. System retrieves form data from FYPForm:
   - name, student_id, program, academicYear
   - skillsText, interestsText
   - difficulty, duration, projectType
   - additionalRequirements, supervisorName, budgetRange
2. System builds structured AI prompt via aiService.buildPrompt():
   ```
   You are an expert academic advisor helping students find their perfect 
   Final Year Project (FYP) topic.
   
   STUDENT PROFILE:
   - Name: [name]
   - Program: [program]
   - Academic Year: [academicYear]
   - Skills & Knowledge: [parsed skills array]
   - Areas of Interest: [parsed interests array]
   - Difficulty Preference: [difficulty]
   - Project Duration: [duration]
   - Project Type: [projectType]
   - Additional Requirements: [additionalRequirements or 'None specified']
   
   TASK: Generate 3 personalized, innovative, and feasible FYP project topics
   
   REQUIREMENTS:
   1. Relevant to program and interests
   2. Match specified difficulty and duration
   3. Innovative but feasible for final year student
   4. Include practical applications and real-world impact
   5. Consider current trends in their field
   
   OUTPUT FORMAT: Return JSON array with exactly 3 objects:
   {
     "id": number,
     "title": "Project Title",
     "description": "Detailed description (2-3 sentences)",
     "difficulty": "Beginner/Intermediate/Advanced",
     "duration": "X-Y months",
     "skills": ["skill1", "skill2", ...],
     "resources": [
       {"type": "Paper/Tutorial/Tool", "title": "...", "url": "#"}
     ],
     "tags": ["tag1", "tag2", ...],
     "objectives": ["objective1", "objective2", ...],
     "methodology": "Brief methodology",
     "expectedOutcomes": "What student will achieve"
   }
   ```
3. System determines AI provider from aiService.provider
4. System sets 30-second timeout using Promise.race()
5. **IF provider === 'gemini':**
   - System sends POST to backend `/api/ai/generate-topics`
   - Backend calls Gemini API (avoids CORS)
   - Backend returns formatted response
6. **IF provider === 'openai':**
   - System calls OpenAI API directly from frontend
7. **IF provider === 'huggingface':**
   - System calls HuggingFace Inference API
8. AI processes prompt and generates response
9. System receives raw response text
10. System extracts JSON using regex: `/\[[\s\S]*\]/`
11. System parses JSON array
12. System validates each topic object has required fields
13. System returns topics array to UC5

**Alternative Flows:**
- **5a. API key not configured:**
  - aiService.isConfigured() returns false
  - System skips AI call
  - System generates intelligent mock data:
    - Filters predefined topics by difficulty and project type
    - Incorporates program name in descriptions
    - Returns 3 mock topics matching form criteria
  - No error shown (seamless fallback)
  
- **5b. Request timeout (30 seconds):**
  - System cancels API request
  - System logs timeout event
  - System falls back to mock data
  - System displays subtle toast: "Using sample topics"
  
- **5c. Network error:**
  - System catches exception
  - System logs error
  - System falls back to mock data
  
- **10a. Invalid JSON in response:**
  - System tries to extract objects individually
  - If still fails: Use mock data
  - System logs parsing error
  
- **12a. Topics missing required fields:**
  - System filters out invalid topics
  - If valid count < 3: Supplement with mock topics
  - System logs validation errors

**Special Requirements:**
- **Timeout**: Must not hang (30s max)
- **Graceful degradation**: Always return usable topics
- **Mock data quality**: Realistic and relevant
- **Provider flexibility**: Easy to switch between Gemini/OpenAI/HuggingFace

**Mock Data Intelligence:**
The mock fallback:
- Contains 50+ predefined realistic topics
- Filters by difficulty (Beginner/Intermediate/Advanced)
- Filters by project type (Research/Development/etc.)
- Adjusts descriptions to mention student's program
- Includes realistic resources, objectives, methodology
- Randomizes selection to provide variety

**Provider-Specific Details:**
- **Gemini**: POST /api/ai/generate-topics (backend proxy)
- **OpenAI**: Direct fetch to api.openai.com
- **HuggingFace**: Direct fetch to api-inference.huggingface.co

**Frequency of Use:** 2-5 times per student session

---

### UC7: Save Favorite Projects

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants to bookmark interesting topics for later
- System: Needs to persist favourites to backend database

**Preconditions:** 
- Student is authenticated
- Student has generated or viewed topics

**Postconditions:**
- Project saved to backend database (SavedProject table)
- ProjectTopic created if doesn't exist
- Favourite accessible from Favourites page
- Visual confirmation shown

**Main Success Scenario:**
1. Student views generated topic in FYPResults
2. Student clicks "Save to Favourites" button (heart icon)
3. System shows loading spinner on button
4. System sends POST to `/api/favourites/` with:
   - topicData: {title, description, difficulty, duration, tags, resources, objectives, methodology, expectedOutcomes}
   - notes: "" (optional user notes)
5. Backend checks if ProjectTopic exists by title
6. **IF ProjectTopic doesn't exist:**
   - Backend creates new ProjectTopic record
7. Backend checks if already saved by user (unique constraint check)
8. **IF not already saved:**
   - Backend creates SavedProject record:
     - user_id
     - project_topic_id
     - status = 'saved'
     - is_favorite = True
     - progress_percentage = 0
9. Backend returns 201 Created with saved project data
10. System updates button state:
    - Heart icon filled
    - Text: "Saved ✓"
    - Green color
11. System displays success toast: "Project saved to favourites!"
12. System updates favourites count (if displayed)

**Alternative Flows:**
- **7a. Project already saved:**
  - Backend returns 409 Conflict: "Project already saved"
  - System displays info message: "Already in your favourites"
  - Button shows "Saved ✓" state
  
- **5a. Network error:**
  - System displays error toast: "Failed to save. Check connection."
  - Button returns to normal state
  - Student can retry
  
- **5b. Unauthorized (token expired):**
  - Backend returns 401
  - System redirects to login
  - System preserves topic data for retry after login

**Special Requirements:**
- **Immediate feedback**: Button state changes instantly (optimistic UI)
- **Duplicate prevention**: Backend enforces unique constraint
- **Full topic data**: All fields saved for later access
- **Rollback**: If backend fails, UI reverts button state

**Technology/Data Variations:**
- Frontend: FYPResults.vue
- Service: favouriteService.js
- Backend: /api/favourites/ (POST)
- Models: SavedProject, ProjectTopic

**Frequency of Use:** 1-5 times per generation session

---

### UC8: Build Project Proposal

**Primary Actor:** Student, AI Service  
**Stakeholders and Interests:**
- Student: Wants structured, professional proposal document
- AI Service: Assists with content generation
- System: Manages multi-step workflow, auto-save, PDF export

**Preconditions:** Student is authenticated  
**Postconditions:**
- Complete proposal created (all sections filled)
- Draft saved in localStorage
- PDF document available for download
- Student can edit and re-download anytime

**Main Success Scenario:**
1. Student clicks "Build Proposal" from:
   - Topic card in FYPResults
   - Favourites page
   - Dashboard quick action
   - Navigation menu
2. System opens ProposalBuilderModal full-screen
3. System checks localStorage for existing draft
4. **IF draft exists:**
   - System displays prompt: "Load previous draft or start fresh?"
   - Student chooses "Load Draft" or "Start Fresh"
5. **IF user has favourites:**
   - System fetches favourites via GET `/api/favourites/`
   - System displays dropdown: "Start from a Saved Favourite"
   - Student can select favourite to auto-fill fields
6. **IF favourite selected:**
   - System auto-fills:
     - Project Title (from favourite title)
     - Background (from description)
     - Objectives (from objectives array)
     - Methodology (from methodology)
7. **IF no draft OR "Start Fresh":**
   - System initializes empty proposal with 6-step structure
8. System displays modal with step navigation (1-6):
   - **Step 1**: Project Basics
   - **Step 2**: Background & Motivation
   - **Step 3**: Project Objectives
   - **Step 4**: Scope & Limitations
   - **Step 5**: Methodology
   - **Step 6**: Timeline & Milestones
9. Student fills Step 1 - Project Basics:
   - Project Title (required, text input)
   - Student Name (pre-filled from user.email)
   - Student ID (text input)
   - Program/Department (text input)
   - Academic Year (text input)
   - Supervisor Name (text input, optional)
10. Student clicks "Next" to advance to Step 2
11. For each content step (2-6), student can:
    - **Option A**: Click "Generate with AI" → Execute UC9
    - **Option B**: Type manually in textarea
    - **Option C**: Use template (pre-filled example)
12. System auto-saves to localStorage every 30 seconds:
    - Key: `proposalDraft`
    - Value: Complete proposal object
    - Toast: "Draft saved" (subtle, bottom-right)
13. Student completes all 6 steps
14. Student reviews completed proposal
15. Student clicks "Download as PDF" button
16. **System executes UC10 (Download Proposal as PDF)**
17. System displays success: "Proposal downloaded!"
18. Modal remains open for edits or can be closed

**Alternative Flows:**
- **3a. Draft corrupted:**
  - System catches JSON parse error
  - System clears localStorage.proposalDraft
  - System initializes empty proposal
  
- **9a. Required field validation:**
  - Student clicks "Next" with empty title
  - System shows error: "Project title is required"
  - System prevents navigation to step 2
  - Student fills title and retries
  
- **11a. AI generation disabled:**
  - System hides "Generate with AI" button
  - Only "Type Manually" and "Use Template" available
  
- **Student closes modal mid-edit:**
  - System detects unsaved changes
  - System shows confirmation: "Save draft before closing?"
  - Options: "Save & Close", "Discard", "Cancel"
  - If "Save & Close": Saves to localStorage then closes

**Special Requirements:**
- **Auto-save**: Every 30s to prevent data loss
- **Progress indicator**: Shows step X of 6
- **Validation**: Real-time + on next/submit
- **Responsive**: Full-screen modal on mobile
- **Draft persistence**: Survives browser refresh

**Step-Specific Details:**

| Step | Section | Word Target | AI Capable | Template Available |
|------|---------|-------------|------------|-------------------|
| 1 | Project Basics | N/A (form fields) | No | No |
| 2 | Background | 200-400 | Yes | Yes |
| 3 | Objectives | 3-5 points | Yes | Yes |
| 4 | Scope | 150-300 | Yes | Yes |
| 5 | Methodology | 300-500 | Yes | Yes |
| 6 | Timeline | 4-6 phases | Yes | Yes |

**Technology/Data Variations:**
- Component: ProposalBuilderModal.vue
- Storage: Browser localStorage (client-side only)
- State: Local reactive refs (step, proposal object)
- No backend persistence (proposals not saved to database)

---

### UC9: Generate Proposal Sections (AI)

**Primary Actor:** AI Service  
**Stakeholders and Interests:**
- Student: Wants professional, relevant content
- AI Service: Generates section-specific content
- System: Manages prompts, validation, fallback

**Preconditions:**
- UC7 in progress (proposal modal open)
- Project title filled in
- AI service configured

**Postconditions:**
- Section populated with AI-generated content
- Content is editable by student
- Draft auto-saved to localStorage
- Section marked as complete

**Main Success Scenario:**
1. Student navigates to section tab (e.g., "Background")
2. Student clicks "Generate with AI" button
3. System validates prerequisites:
   - Project title is non-empty
   - Section type identified
4. System updates button state:
   - Text: "Generating..."
   - Shows spinner
   - Disables button
5. System builds section-specific AI prompt:

   **Background Section Prompt:**
   ```
   Generate a professional Background & Motivation section for a 
   final year project proposal.
   
   Project: [projectTitle]
   Student: [level] in [program]
   Skills: [studentSkills]
   Category: [inferredCategory]
   
   Requirements:
   - Length: 200-400 words
   - Include: problem statement, current limitations, significance
   - Tone: Academic, professional
   - Structure: 3-4 paragraphs
   
   Return only the background text, no additional formatting.
   ```

   **Objectives Section Prompt:**
   ```
   Generate 4-5 specific, measurable objectives for this FYP:
   
   Project: [projectTitle]
   Level: [level]
   
   Requirements:
   - Start with action verbs (Develop, Design, Implement, Evaluate)
   - Achievable in 3-6 months
   - Specific and measurable
   - Format as numbered list
   
   Return only the numbered objectives.
   ```

   *(Similar prompts for Scope, Methodology, Timeline)*

6. System calls AI API with prompt
7. System sets 30-second timeout
8. AI generates section-specific content
9. System receives response text
10. System validates generated content:
    - Word count meets section requirements
    - Structure matches expected format
    - Content mentions project title
    - No inappropriate content
11. System inserts content into editor:
    ```javascript
    proposal.sections[sectionType] = generatedContent
    ```
12. System updates button state:
    - Text: "Generated ✓"
    - Green checkmark icon
    - Re-enables button
13. System triggers auto-save
14. System displays toast: "[Section] generated successfully!"
15. Student can now edit content or move to next section

**Alternative Flows:**
- **3a. Project title empty:**
  - System shows validation error
  - System highlights "Project Information" tab
  - System does not call AI
  - Student must fill title first
  
- **6a. AI API call fails:**
  - System loads predefined template for section type
  - Templates are professionally written examples
  - System shows toast: "Using template (AI unavailable)"
  - Content is editable
  
- **6b. Request timeout (30s):**
  - System cancels API request
  - System loads template as fallback
  - System logs timeout event
  
- **10a. Generated content too short (<50% minimum):**
  - System retries with stricter prompt
  - Prompt addition: "Provide more detail and expand on..."
  - If retry fails: Use template
  
- **10b. Content appears off-topic:**
  - System checks if project title appears in response
  - System checks for domain keywords
  - If validation fails:
    - System shows warning: "Review content carefully"
    - System still inserts (allows student editing)
  
- **Student clicks "Regenerate":**
  - System shows confirmation: "Replace existing content?"
  - If Yes: Repeat generation process
  - If No: Keep existing content

**Special Requirements:**
- **Speed**: Target 10-15 seconds per section
- **Quality**: Content must be coherent and relevant
- **Editability**: Always allow manual editing post-generation
- **Consistency**: Sections should reference each other

**Template Fallback Content Examples:**

**Background Template:**
```
This project aims to address challenges in [domain] by developing [title]. 
Currently, existing solutions face limitations such as [common limitation]. 
This project will contribute by implementing [general approach].

The proposed system will provide [core functionality]. This addresses 
key gaps in current approaches including [limitation 1] and [limitation 2].

This research is motivated by the increasing need for [domain benefit]. 
The expected outcome is a functional system that demonstrates [value proposition].
```

**Objectives Template:**
```
1. Design and develop [core system component]
2. Implement [key feature 1] to address [problem]
3. Implement [key feature 2] for [purpose]
4. Test and evaluate system performance and usability
5. Document the development process and user guidelines
```

**Quality Validation Checklist:**
- [ ] Mentions project title at least once
- [ ] Meets minimum word count for section
- [ ] Uses appropriate academic tone
- [ ] Contains no hallucinated facts/references
- [ ] Structured according to section requirements
- [ ] No inappropriate or offensive content

**Frequency of Use:** 5 times per proposal (one per section)

---

### UC10: Download Proposal as PDF

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants professional, formatted PDF document
- System: Generates well-structured PDF with proper formatting

**Preconditions:**
- UC7 in progress (proposal modal open)
- At least project information filled

**Postconditions:**
- PDF file downloaded to student's device
- Filename is descriptive and professional
- PDF contains all proposal sections
- Formatting is clean and university-appropriate
- Modal remains open for further edits

**Main Success Scenario:**
1. Student clicks "Download as PDF" button in proposal modal (Step 6)
2. System validates proposal:
   - Project title is filled
   - At least 2 content sections have text
3. System initializes jsPDF library
4. System generates PDF document structure:
   
   **PAGE 1: Title Page**
   - University/System logo (if configured)
   - Document title: "Final Year Project Proposal" (centered, 24pt, bold)
   - Project title (centered, 20pt, bold, wrapped if long)
   - Horizontal separator line
   - Student information table:
     - Student Name: [value]
     - Student ID: [value]
     - Program: [value]
     - Academic Year: [value]
     - Supervisor: [value or 'TBD']
   - Date generated: [current date]
   - Page break

   **PAGE 2+: Content Sections**
   - For each completed step (Background, Objectives, Scope, Methodology, Timeline):
     - Section heading (bold, 16pt, left-aligned, primary color)
     - Section content (normal, 11pt, justified, line height 1.5)
     - 15mm spacing between sections
     - Auto page break when content exceeds page height

5. System formats text content:
   - Preserves line breaks from textarea
   - Wraps long lines to page width (170mm)
   - Converts bullet points to proper list format
   - Maintains paragraph spacing
6. System generates filename:
   ```javascript
   const sanitized = projectTitle
     .replace(/[^a-z0-9 ]/gi, '-')
     .toLowerCase()
     .substring(0, 50)
   const timestamp = new Date().toISOString().split('T')[0]
   const filename = `${sanitized}-proposal-${timestamp}.pdf`
   ```
   Example: `ai-powered-healthcare-system-proposal-2025-12-26.pdf`
7. System triggers browser download using `doc.save(filename)`
8. Browser downloads PDF to default location
9. System displays success toast: "Proposal downloaded successfully!" (green, 3 seconds)
10. Modal remains open for further edits or can be closed

**Alternative Flows:**
- **2a. Validation fails (title empty):**
  - System highlights "Project Title" field in Step 1
  - System shows error: "Please enter a project title"
  - System prevents PDF generation
  - Student fills title and retries
  
- **2b. All sections empty:**
  - System shows warning: "Add content to at least 2 sections"
  - System allows download with confirmation
  - PDF contains only title page if confirmed
  
- **7a. Browser blocks download:**
  - System detects blocked download
  - System shows manual download button
  - System provides instructions: "Please allow downloads"
  
- **3a. jsPDF library not loaded:**
  - System catches error
  - System displays error: "PDF generation failed"
  - System logs error for debugging

**Special Requirements:**
- **PDF Quality**: Professional, university-suitable formatting
- **File size**: Typically 50-150 KB (text-only)
- **Compatibility**: Opens in all PDF readers (Adobe, Chrome, etc.)
- **No backend**: Pure client-side generation (jsPDF library)
- **Accessibility**: Selectable text, proper structure

**PDF Formatting Standards:**
- **Font**: Helvetica (universal support)
- **Font sizes**: 
  - Title: 24pt bold
  - Project title: 20pt bold
  - Headings: 16pt bold
  - Body: 11pt normal
- **Margins**: 20mm (0.79 inches) all sides
- **Line spacing**: 1.5 for readability
- **Page size**: A4 (210 x 297 mm)
- **Text alignment**: Justified for body, left for headings
- **Colors**: Primary color for headings, black for body

**Performance:**
- Generation time: < 2 seconds for typical proposal
- No network calls (entirely client-side)
- Works offline once page loaded

**Frequency of Use:** 2-5 times per proposal (initial + revisions)

---

### UC11: Track Project Progress

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants to monitor FYP progress and stay organized
- System: Provides structured progress tracking

**Preconditions:** 
- Student is authenticated
- Project saved to favourites

**Postconditions:**
- Project has defined phases and tasks
- Progress percentage calculated and displayed
- Timeline and status tracked
- Student can view progress on Favourites page

**Main Success Scenario:**
1. Student opens Favourites page
2. System fetches favourites via GET `/api/favourites/`
3. System displays saved projects with progress indicators
4. Student clicks on project card to expand
5. System displays project details including:
   - Current status badge (Saved/In Progress/Completed)
   - Progress bar (0-100%)
   - Phases list (if defined)
   - Task checklist per phase
6. Student clicks "Enable Progress Tracking" toggle
7. System sends PUT to `/api/progress/enable/<favourite_id>`
8. Backend updates SavedProject.progress_tracking_enabled = True
9. System displays phase management interface:
   - "Add Phase" button
   - Phase list with drag-to-reorder
10. Student clicks "Add Phase"
11. System shows phase creation modal:
    - Phase Name (required)
    - Description (optional textarea)
    - Estimated Duration (weeks, number input)
    - Start Date (date picker, optional)
    - End Date (date picker, optional)
12. Student fills phase details and clicks "Create"
13. System sends POST to `/api/progress/<project_id>/phases`
14. Backend creates ProjectPhase record:
    - saved_project_id
    - phase_name, description
    - phase_order (auto-incremented)
    - estimated_duration_weeks
    - start_date, end_date
    - status = 'not_started'
    - progress_percentage = 0
15. System displays phase in list
16. Student can add tasks to phase:
    - Clicks "Add Task" within phase
    - Enters task name and optional due date
    - System creates PhaseTask record
17. Student checks off completed tasks:
    - Clicks checkbox next to task
    - System updates PhaseTask.is_completed = True
    - System updates PhaseTask.completed_at = now
    - System recalculates phase progress
    - System recalculates overall project progress
18. System auto-updates progress percentage:
    - Phase progress = (completed tasks / total tasks) * 100
    - Project progress = average of all phase progress
19. Progress displayed on Favourites page:
    - Progress bar filled to percentage
    - Status automatically updated based on progress:
      - 0% = 'not_started'
      - 1-99% = 'in_progress'
      - 100% = 'completed'
20. Student can update phase status manually if needed

**Alternative Flows:**
- **6a. Progress tracking already enabled:**
  - System skips enable step
  - Displays existing phases and tasks
  
- **13a. Phase creation fails:**
  - Backend returns error
  - System displays error toast
  - Modal remains open for retry
  
- **17a. Unchecking completed task:**
  - System updates is_completed = False
  - System clears completed_at
  - System recalculates progress (decreases)

**Special Requirements:**
- **Real-time updates**: Progress bar animates on changes
- **Drag-to-reorder**: Phases can be reordered
- **Auto-calculation**: Progress computed from tasks
- **Visual feedback**: Color-coded status badges

**Progress Calculation Formula:**
```javascript
// Phase progress
phaseProgress = (completedTasks / totalTasks) * 100

// Project overall progress  
projectProgress = sum(allPhaseProgress) / totalPhases
```

**Status Logic:**
```javascript
if (progress === 0) status = 'not_started'
else if (progress === 100) status = 'completed'
else status = 'in_progress'
```

**Technology/Data Variations:**
- Component: FavouritesPage.vue, ProjectProgressTracker.vue
- Service: progressService.js
- Backend: /api/progress/* routes
- Models: SavedProject, ProjectPhase, PhaseTask

**Frequency of Use:** Daily for active projects

---

### UC12: Manage Favourites

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants to organize and review saved projects
- System: Provides CRUD operations on favourites

**Preconditions:** 
- Student is authenticated
- At least one project saved

**Postconditions:**
- Favourites list displayed
- Projects can be viewed, edited, deleted
- User notes updated
- Status changed

**Main Success Scenario:**
1. Student clicks "My Favourites" in navigation
2. System sends GET to `/api/favourites/`
3. Backend queries SavedProject table for user's projects
4. Backend joins with ProjectTopic to get full details
5. Backend returns favourites array with:
   - id, saved_at, user_notes, custom_title
   - status, progress_percentage, is_favorite
   - phases array (with tasks)
   - project_topic object (title, description, etc.)
6. System displays favourites in card grid layout
7. Each card shows:
   - Project title (custom or original)
   - Status badge (color-coded)
   - Saved date
   - Progress bar
   - Description preview
   - Difficulty and duration badges
   - Action buttons (Edit, Delete, Build Proposal)
8. Student can perform actions:
   
   **8a. View Details:**
   - Click card to expand full description
   - View objectives, methodology, resources
   - See progress phases and tasks
   
   **8b. Edit Notes:**
   - Click edit icon (pencil)
   - Modal appears with textarea
   - Student enters/updates notes
   - System sends PUT to `/api/favourites/<id>/notes`
   - Backend updates SavedProject.user_notes
   - System displays success toast
   
   **8c. Change Status:**
   - Click status dropdown
   - Select new status (Saved/Not Started/In Progress/Completed/Abandoned)
   - System sends PUT to `/api/favourites/<id>/status`
   - Backend updates SavedProject.status
   - Badge color updates immediately
   
   **8d. Delete Favourite:**
   - Click delete button (trash icon)
   - System shows confirmation: "Remove this project?"
   - If confirmed:
     - System sends DELETE to `/api/favourites/<id>`
     - Backend deletes SavedProject (cascades to phases/tasks)
     - System removes card from list with fade-out animation
     - System displays toast: "Project removed"
   
   **8e. Build Proposal:**
   - Click "Build Proposal" button
   - System opens ProposalBuilderModal
   - System pre-fills with project data
   - Student proceeds with UC8

9. Student can filter/sort favourites:
   - Filter by status
   - Filter by difficulty
   - Sort by date saved (newest/oldest)
   - Sort by progress (highest/lowest)

**Alternative Flows:**
- **2a. No favourites saved:**
  - System displays empty state
  - Icon: Heart outline
  - Message: "No saved projects yet"
  - Button: "Generate Projects" (links to home)
  
- **8b. Update notes fails:**
  - System displays error toast
  - Notes revert to previous value
  
- **8d. Delete fails:**
  - System displays error
  - Card remains in list
  - Student can retry

**Special Requirements:**
- **Loading state**: Skeleton cards while fetching
- **Optimistic UI**: Updates appear immediately
- **Animations**: Smooth card entry/exit
- **Responsive**: Grid adjusts columns (1-3) by screen size

**Favourite Card Layout:**
```
┌─────────────────────────────────────┐
│ ♥ Project Title        [Saved ✓]    │
│ Saved 2 days ago                    │
│                                     │
│ Description preview...              │
│                                     │
│ [Intermediate] [6-8 months]         │
│ Progress: ████████░░░░ 65%          │
│                                     │
│ [✏️ Edit] [🗑️ Delete] [📄 Proposal] │
└─────────────────────────────────────┘
```

**Technology/Data Variations:**
- Component: FavouritesPage.vue
- Service: favouriteService.js
- Backend: /api/favourites/* routes
- Models: SavedProject, ProjectTopic

**Frequency of Use:** 5-10 times per week

---

### UC13: Create Workspace

**Primary Actor:** Student  
**Stakeholders and Interests:**
- Student: Wants to collaborate with peers on FYP
- System: Provides collaborative environment

**Preconditions:** 
- Student is authenticated

**Postconditions:**
- New workspace created in database
- Student is workspace owner
- Workspace accessible from Workspaces page
- Invitation system activated

**Main Success Scenario:**
1. Student clicks "Workspaces" in navigation
2. System displays Workspaces page
3. Student clicks "Create Workspace" button
4. System shows CreateWorkspaceModal
5. Student fills workspace details:
   - Workspace Name (required, text input)
   - Description (optional, textarea)
   - Link to Saved Project (optional, dropdown from favourites)
   - Privacy Settings:
     - Public/Private toggle
     - Max Members (number, default 10)
6. Student clicks "Create Workspace"
7. System validates inputs
8. System sends POST to `/api/workspaces/` with:
   - name, description
   - saved_project_id (if selected)
   - is_public (boolean)
   - max_members (number)
9. Backend creates Workspace record:
   - owner_id = current_user.id
   - name, description, is_public, max_members
   - saved_project_id (if provided)
   - created_at = now
   - invite_code = generated 8-char code
10. Backend returns workspace data
11. System closes modal
12. System displays success: "Workspace created!"
13. System redirects to workspace detail view
14. Workspace detail shows:
    - Workspace name and description
    - Owner badge (current user)
    - Member list (initially just owner)
    - Invite code box with copy button
    - Tabs: Chat, Files, Activity
    - Project details (if linked to saved project)
15. Student can now:
    - Invite members (UC14)
    - Start chat (UC15)
    - Share files (UC16)

**Alternative Flows:**
- **7a. Validation fails (name empty):**
  - System shows error: "Workspace name is required"
  - Modal remains open
  - Student fills name and retries
  
- **8a. Linked project not found:**
  - Backend returns 404
  - System displays error: "Selected project not found"
  - Student selects different project or proceeds without
  
- **8b. User doesn't own selected project:**
  - Backend returns 403 Forbidden
  - System displays error: "You don't own this project"

**Special Requirements:**
- **Invite code**: 8-character alphanumeric, unique
- **Max members**: Enforced by backend (default 10)
- **Owner privileges**: Full control over workspace
- **Project linking**: Optional but recommended

**Workspace Creation Logic:**
```python
# Backend pseudocode
invite_code = secrets.token_urlsafe(6)[:8]
workspace = Workspace(
    name=data['name'],
    owner_id=current_user_id,
    invite_code=invite_code,
    is_public=data.get('is_public', False),
    max_members=data.get('max_members', 10)
)
db.session.add(workspace)
db.session.commit()
```

**Technology/Data Variations:**
- Component: WorkspacesPage.vue, CreateWorkspaceModal.vue
- Service: workspaceService.js
- Backend: /api/workspaces/ (POST)
- Model: Workspace

**Frequency of Use:** 1-3 times per student (per FYP project)

---

### UC14: Collaborate on Project

**Primary Actor:** Student (Workspace Member)  
**Stakeholders and Interests:**
- Students: Want real-time collaboration
- System: Provides chat, files, activity tracking

**Preconditions:** 
- Student is workspace member or owner
- Workspace exists

**Postconditions:**
- Members can communicate in real-time
- Files shared within workspace
- Activity logged and visible

**Main Success Scenario:**
1. Student navigates to Workspaces page
2. System fetches workspaces via GET `/api/workspaces/`
3. System displays owned and joined workspaces
4. Student clicks on workspace card
5. System opens WorkspaceDetailsModal
6. System displays workspace with three tabs:
   - **Chat Tab** (default, UC15)
   - **Files Tab** (UC16)
   - **Activity Tab** (auto-generated log)
7. Chat Tab (UC15) shows:
   - Message list (real-time updates)
   - Message input box
   - Send button
   - Typing indicators
8. Files Tab (UC16) shows:
   - File upload zone (drag & drop)
   - Uploaded files list with download links
   - File metadata (uploader, date, size)
9. Activity Tab shows:
   - Auto-generated activity feed:
     - "Alice joined workspace"
     - "Bob uploaded proposal_draft.pdf"
     - "Carol sent a message"
     - "Diana left workspace"
   - Timestamps (relative: "2 hours ago")
   - User avatars/initials
10. Student can invite new members:
    - Clicks "Invite Members" button
    - System shows invite modal with:
      - Invite code (shareable link)
      - Copy button
      - OR Email invite form
    - Student shares code with peers
11. New member joins:
    - Navigates to `/join/<invite_code>`
    - System validates code and membership limit
    - System creates WorkspaceMember record
    - System logs activity: "[Name] joined workspace"
12. Members see each other in member list:
    - Owner (crown icon)
    - Editors (can upload files, send messages)
    - Viewers (read-only, if implemented)

**Alternative Flows:**
- **5a. Student not a member:**
  - System redirects to workspaces list
  - System shows error: "You don't have access"
  
- **10a. Workspace at max capacity:**
  - System prevents invite code generation
  - System shows warning: "Workspace full"
  
- **11a. Invalid invite code:**
  - System returns 404
  - System displays: "Invalid or expired invite"

**Special Requirements:**
- **Real-time updates**: WebSocket for chat and activity
- **File upload**: Max 50MB per file
- **Activity auto-log**: Backend triggers on all actions
- **Member roles**: Owner vs Member permissions

**Collaborative Features:**
| Feature | Owner | Member | Viewer |
|---------|-------|--------|--------|
| Send messages | ✅ | ✅ | ❌ |
| Upload files | ✅ | ✅ | ❌ |
| Delete files | ✅ | Own only | ❌ |
| Invite members | ✅ | ✅ | ❌ |
| Remove members | ✅ | ❌ | ❌ |
| Delete workspace | ✅ | ❌ | ❌ |

**Technology/Data Variations:**
- Components: WorkspacesPage.vue, WorkspaceDetailsModal.vue, WorkspaceChat.vue, WorkspaceFiles.vue
- Service: workspaceService.js
- Backend: /api/workspaces/<id>/* routes
- Models: Workspace, WorkspaceMember, WorkspaceMessage, WorkspaceFile

**Frequency of Use:** Daily for active collaborations

---

### UC15: Real-time Chat

**Primary Actor:** Student (Workspace Member)  
**Stakeholders and Interests:**
- Students: Want instant communication
- System: Provides WebSocket-based chat

**Preconditions:** 
- Student is workspace member
- Workspace details modal open on Chat tab

**Postconditions:**
- Messages sent and received in real-time
- Chat history persisted to database
- Typing indicators shown

**Main Success Scenario:**
1. Student opens Chat tab in workspace
2. System establishes WebSocket connection:
   - Connects to Socket.IO server
   - Joins room: `workspace_<id>`
   - Receives authentication token
3. System fetches chat history:
   - GET `/api/chat/workspaces/<id>/messages`
   - Backend returns last 50 messages
4. System displays messages in chronological order:
   - Each message shows:
     - Sender name
     - Message content
     - Timestamp (relative)
     - Avatar/initials
5. Student types message in input box
6. System emits typing indicator via WebSocket:
   - Event: `typing`
   - Data: {workspace_id, user_name}
7. Other members see: "[Name] is typing..."
8. Student clicks "Send" or presses Enter
9. System sends POST to `/api/chat/workspaces/<id>/messages`:
   - message: text content
   - workspace_id
10. Backend creates WorkspaceMessage record:
    - workspace_id
    - user_id (sender)
    - message (content)
    - created_at = now
11. Backend emits WebSocket event to room:
    - Event: `new_message`
    - Data: {message object with user details}
12. All connected members receive message instantly
13. System appends message to chat UI
14. System scrolls chat to bottom
15. System displays delivery confirmation (checkmark)
16. Typing indicator clears

**Alternative Flows:**
- **2a. WebSocket connection fails:**
  - System falls back to polling (GET messages every 5s)
  - System shows banner: "Real-time chat unavailable"
  
- **9a. Message send fails:**
  - System shows error: "Failed to send message"
  - System keeps message in input for retry
  - Student can resend
  
- **11a. User not authorized:**
  - Backend returns 403
  - System displays: "You were removed from workspace"
  - System disconnects WebSocket

**Special Requirements:**
- **Real-time**: WebSocket (Socket.IO) for instant delivery
- **Persistence**: All messages saved to database
- **Scroll behavior**: Auto-scroll to bottom on new message
- **Typing indicators**: Timeout after 3 seconds of inactivity

**WebSocket Events:**
| Event | Direction | Data | Purpose |
|-------|-----------|------|---------|
| `join_workspace` | Client → Server | {workspace_id, token} | Join room |
| `new_message` | Server → Client | {message object} | Broadcast message |
| `typing` | Client → Server | {workspace_id, user} | Typing indicator |
| `user_joined` | Server → Client | {user_name} | Member joined |
| `user_left` | Server → Client | {user_name} | Member left |

**Message Object Structure:**
```json
{
  "id": 123,
  "workspace_id": 5,
  "user_id": 42,
  "user_name": "Alice",
  "user_email": "alice@example.com",
  "message": "Hello team!",
  "created_at": "2025-12-26T10:30:00Z"
}
```

**Technology/Data Variations:**
- Component: WorkspaceChat.vue
- Service: chatService.js
- Backend: /api/chat/*, Socket.IO server (sockets.py)
- Model: WorkspaceMessage

**Frequency of Use:** Multiple times per day during collaboration

---

### UC16: Share Files

**Primary Actor:** Student (Workspace Member)  
**Stakeholders and Interests:**
- Students: Want to share proposals, code, documents
- System: Provides file upload/download

**Preconditions:** 
- Student is workspace member
- Workspace details modal open on Files tab

**Postconditions:**
- File uploaded to server
- File accessible to all workspace members
- File metadata stored in database

**Main Success Scenario:**
1. Student opens Files tab in workspace
2. System fetches files via GET `/api/files/workspaces/<id>`
3. System displays uploaded files in list:
   - Filename
   - Uploader name
   - Upload date
   - File size
   - Download button
   - Delete button (own files only)
4. Student clicks "Upload File" or drags file to drop zone
5. System validates file:
   - Size < 50 MB
   - Not executable (security check)
6. System creates FormData with file
7. System sends POST to `/api/files/workspaces/<id>/upload`:
   - FormData containing file binary
   - workspace_id in URL
8. Backend receives file
9. Backend saves file to disk:
   - Path: `uploads/workspace_{id}/{uuid}_{filename}`
   - Ensures unique filename
10. Backend creates WorkspaceFile record:
    - workspace_id
    - user_id (uploader)
    - filename (original name)
    - filepath (server path)
    - filesize (bytes)
    - uploaded_at = now
11. Backend logs activity: "[User] uploaded [filename]"
12. Backend returns file metadata
13. System displays file in list
14. System shows success toast: "File uploaded!"
15. Other members can download:
    - Click download button
    - System sends GET to `/api/files/<file_id>/download`
    - Backend streams file
    - Browser downloads file

**Alternative Flows:**
- **5a. File too large (> 50 MB):**
  - System shows error: "File exceeds 50 MB limit"
  - System prevents upload
  
- **5b. Executable file detected:**
  - System blocks upload for security
  - System shows warning: "Executable files not allowed"
  
- **8a. Upload fails (network error):**
  - System displays error with retry button
  - System keeps file selected for retry
  
- **15a. File deleted by uploader:**
  - Other member clicks download
  - Backend returns 404
  - System displays: "File no longer available"

**Special Requirements:**
- **File size limit**: 50 MB per file
- **Storage path**: `uploads/workspace_{id}/`
- **Security**: No executable files (.exe, .sh, .bat, etc.)
- **Access control**: Only workspace members can download

**Allowed File Types:**
- Documents: .pdf, .doc, .docx, .txt
- Presentations: .ppt, .pptx
- Spreadsheets: .xls, .xlsx, .csv
- Code: .py, .js, .java, .cpp, .html, .css
- Images: .jpg, .png, .gif, .svg
- Archives: .zip, .tar, .gz

**File Upload Workflow:**
```
1. Browser: File selected
2. Frontend: Validate size & type
3. Backend: Save to uploads/ directory
4. Database: Create WorkspaceFile record
5. Activity: Log upload action
6. WebSocket: Notify members (optional)
7. Frontend: Update file list
```

**Technology/Data Variations:**
- Component: WorkspaceFiles.vue
- Service: fileService.js
- Backend: /api/files/* routes
- Model: WorkspaceFile
- Storage: Local filesystem (uploads/)

**Frequency of Use:** 3-5 times per workspace lifecycle

---

### UC17: Admin Dashboard

**Primary Actor:** Admin  
**Stakeholders and Interests:**
- Admin: Wants to monitor system health and user activity
- System: Provides analytics and management tools

**Preconditions:** 
- User is authenticated
- User has role='admin'

**Postconditions:**
- Admin views system statistics
- Admin can manage users
- Admin can view analytics

**Main Success Scenario:**
1. Admin logs in (UC2)
2. System detects user.role === 'admin'
3. System shows admin-specific navigation option
4. Admin clicks "Admin Dashboard" in dropdown
5. System displays AdminDashboard component with 4 tabs:
   - Overview
   - Users
   - Topics
   - Analytics
6. **Overview Tab** shows:
   - System Statistics Cards:
     - Total Users (student + admin counts)
     - Total Project Topics
     - Total Generated Projects
     - Total Saved Projects
   - Recent Activity:
     - New users (last 30 days)
     - Active users (last 30 days)
   - Quick Actions:
     - "View All Users"
     - "View Analytics"
7. **Users Tab** (UC18) displays:
   - User list table
   - Search/filter controls
   - Role management
   - User actions (promote, demote, delete)
8. **Topics Tab** shows:
   - All ProjectTopic records
   - Source type (generated vs manual)
   - AI provider statistics
   - Popular topics
9. **Analytics Tab** (UC19) displays:
   - Usage charts
   - Generation trends
   - User engagement metrics
10. Admin can navigate between tabs freely
11. All data fetched via admin-protected endpoints

**Alternative Flows:**
- **2a. User is not admin:**
  - System hides admin navigation option
  - Direct URL access returns 403 Forbidden
  - System redirects to dashboard
  
- **4a. Admin exits dashboard:**
  - Clicks "Exit Admin" button
  - System returns to normal student view

**Special Requirements:**
- **Authorization**: All admin endpoints require admin role
- **Real-time stats**: Data refreshes on tab switch
- **Responsive**: Tables adapt to mobile screens
- **Export**: Future: export analytics to CSV

**Admin Role Check (Backend):**
```python
@admin_required
def get_overview_stats():
    user = User.query.get(current_user_id)
    if not user.is_admin():
        return 403 Forbidden
    # ... fetch stats
```

**Technology/Data Variations:**
- Component: AdminDashboard.vue, admin/* subcomponents
- Backend: /api/admin/* routes (protected)
- Decorator: @admin_required
- Model: User.role field

**Frequency of Use:** Weekly for system monitoring

---

### UC18: Manage Users

**Primary Actor:** Admin  
**Stakeholders and Interests:**
- Admin: Wants to manage user accounts and roles
- System: Provides user CRUD operations

**Preconditions:** 
- Admin is logged in
- Admin dashboard open on Users tab

**Postconditions:**
- User data displayed
- User roles updated (if changed)
- User accounts managed

**Main Success Scenario:**
1. Admin opens Users tab in dashboard
2. System sends GET to `/api/admin/users`
3. Backend queries all User records
4. Backend returns user list with:
   - id, email, role, created_at
   - onboarding_completed status
   - auth_provider (email or google)
   - last login (if tracked)
5. System displays users in sortable table:
   - Columns: Email, Role, Provider, Created, Status, Actions
   - Rows: One per user
6. Admin can search users by email
7. Admin can filter by:
   - Role (student/admin)
   - Auth provider (email/google)
   - Onboarding status (completed/incomplete)
8. Admin clicks "Promote to Admin" on a student
9. System shows confirmation: "Promote [email] to admin?"
10. Admin confirms
11. System sends POST to `/api/admin/users/<id>/promote`
12. Backend updates User.role = 'admin'
13. System updates table row (role badge turns purple)
14. System displays success: "[Email] is now an admin"
15. Admin can also:
    - **Demote admin** to student (reverses promote)
    - **View user details** (opens modal with full profile)
    - **Delete user** (with cascade to all related data)

**Alternative Flows:**
- **11a. Promote fails (last admin):**
  - Backend prevents demoting last admin
  - System shows error: "Cannot demote last admin"
  
- **11b. Network error:**
  - System displays error toast
  - Table row reverts to previous state
  
- **Delete user flow:**
  - Admin clicks delete icon (trash)
  - System shows confirmation: "Delete [email]? This will remove all their data."
  - Admin confirms
  - System sends DELETE to `/api/admin/users/<id>`
  - Backend cascades deletion (favourites, workspaces, etc.)
  - System removes row from table
  - System displays success: "User deleted"

**Special Requirements:**
- **Pagination**: Show 20 users per page (for large datasets)
- **Search**: Real-time client-side filtering
- **Confirmation**: All destructive actions require confirmation
- **Cascade**: User deletion cascades to related data

**User Table Columns:**
| Column | Data | Sortable | Filterable |
|--------|------|----------|------------|
| Email | user.email | Yes | Yes |
| Role | student/admin | Yes | Yes |
| Provider | email/google | No | Yes |
| Created | YYYY-MM-DD | Yes | No |
| Onboarded | ✓/✗ | No | Yes |
| Actions | Buttons | No | No |

**Admin Actions:**
```javascript
// Promote to admin
POST /api/admin/users/{id}/promote

// Demote to student
POST /api/admin/users/{id}/demote

// Delete user
DELETE /api/admin/users/{id}
```

**Technology/Data Variations:**
- Component: admin/AdminUsers.vue
- Backend: /api/admin/users* routes
- Model: User (role field)

**Frequency of Use:** Weekly for user management

---

### UC19: View Analytics

**Primary Actor:** Admin  
**Stakeholders and Interests:**
- Admin: Wants insights into system usage
- System: Provides data visualization

**Preconditions:** 
- Admin is logged in
- Admin dashboard open on Analytics tab

**Postconditions:**
- Usage metrics displayed
- Trends visualized in charts
- Insights actionable

**Main Success Scenario:**
1. Admin opens Analytics tab in dashboard
2. System sends GET to `/api/admin/stats/usage`
3. Backend aggregates analytics data:
   - Daily project generations (last 30 days)
   - User registration trend
   - Popular project categories
   - AI provider usage breakdown
   - Average projects per user
4. Backend returns analytics JSON
5. System displays charts and metrics:
   
   **Chart 1: Project Generations Over Time**
   - Line chart
   - X-axis: Date (last 30 days)
   - Y-axis: Generation count
   - Shows trend and spikes
   
   **Chart 2: User Growth**
   - Bar chart
   - X-axis: Month
   - Y-axis: New users
   - Compares monthly growth
   
   **Chart 3: Project Categories**
   - Pie chart
   - Slices: AI, Web Dev, Mobile, Data Science, etc.
   - Percentages shown
   
   **Chart 4: AI Provider Usage**
   - Horizontal bar chart
   - Bars: Gemini, OpenAI, Mock Data
   - Shows which providers most used
   
6. System displays key metrics cards:
   - Average projects per user: 3.2
   - Most active day: Friday
   - Peak hour: 14:00-15:00
   - Conversion rate: 65% (users who generate → save)
7. Admin can:
   - Export data as CSV (future feature)
   - Adjust date range (future feature)
   - Drill down into specific metrics

**Alternative Flows:**
- **2a. No data available:**
  - System displays empty state
  - Message: "No analytics data yet"
  - Encourages usage
  
- **3a. Aggregation timeout:**
  - Backend returns partial data
  - System displays what's available
  - Shows warning: "Some data unavailable"

**Special Requirements:**
- **Performance**: Aggregations cached for 1 hour
- **Visualization**: Responsive charts (Chart.js or similar)
- **Real-time**: Stats update on page refresh
- **Privacy**: Aggregated data only (no individual user tracking)

**Analytics Queries (Backend):**
```python
# Daily generations last 30 days
db.session.query(
    func.date(GeneratedProject.created_at).label('date'),
    func.count(GeneratedProject.id).label('count')
).filter(
    GeneratedProject.created_at >= thirty_days_ago
).group_by('date').all()

# Popular categories
db.session.query(
    ProjectTopic.tags,
    func.count(SavedProject.id)
).join(SavedProject).group_by(ProjectTopic.tags).all()
```

**Technology/Data Variations:**
- Component: admin/AdminAnalytics.vue
- Backend: /api/admin/stats/* routes
- Charting: Chart.js or vue-chartjs
- Models: GeneratedProject, SavedProject, User, UserActivity

**Frequency of Use:** Weekly for monitoring trends

---

## 3. Activity Diagrams (Complex Use Cases Only)

### Activity Diagram 1: Topic Discovery with AI Integration

This diagram shows the complete flow of how students discover research topics with AI assistance and graceful fallback to mock data.

#### How to Draw This Activity Diagram

**Swimlanes (Vertical Columns):**
Create two swimlanes:
1. **Student** (left column)
2. **System** (right column)

#### Flow Steps to Draw:

**START** (black filled circle at top of Student swimlane)

**Step 1: Student Actions**
- Draw rounded rectangle: "Navigate to Topic Discovery page"

**Step 2: System Check**
- Draw diamond (decision): "Profile ≥70% complete?"
- Two paths exit: "yes" (right) and "no" (down)

**PATH A: Profile Complete (YES path)**

**Step 3: Student Configuration**
- Rounded rectangle: "Configure search parameters"
  - Add note box: "Select category, Set topic count (1-10), Toggle Use AI"
- Rounded rectangle: "Click 'Generate Topics'"

**Step 4: System Processing**
- Rounded rectangle: "Show loading state"
- Diamond: "Use AI enabled?"
  - Two paths: "yes" and "no"

**PATH A1: AI Enabled (YES)**

**Step 5: AI Configuration Check**
- Diamond: "AI service configured?"
  - Two paths: "yes" and "no"

**PATH A1a: AI Configured (YES)**

**Step 6: Build Prompt**
- Rounded rectangle: "Build AI prompt with:"
  - Add note: "Student profile context, Category filter, Topic count"

**Step 7: Concurrent Actions (Fork)**
- Draw a **thick horizontal bar** (fork/join bar)
- From this bar, draw TWO parallel paths:
  - Path 1: "Call AI API (Gemini/OpenAI/HuggingFace)"
  - Path 2: "Set 30-second timeout"
- Both paths merge back into another **thick horizontal bar**

**Step 8: Response Check**
- Diamond: "Response received within 30s?"
  - Two paths: "success" and "timeout/error"

**PATH A1a-i: Success**

**Step 9: Parse Response**
- Rounded rectangle: "Extract JSON from response"
- Diamond: "Valid JSON array?"
  - Paths: "yes" and "invalid JSON"

**PATH A1a-i-α: Valid JSON**

**Step 10: Validate Topics**
- Rounded rectangle: "Validate topic objects (title, description, category, difficulty)"
- Diamond: "All topics valid?"
  - Paths: "yes" and "some invalid"

**If YES:**
- Rounded rectangle: "Enrich with metadata (id, source='ai', timestamp)"
- Rounded rectangle (GREEN background): "Display AI-generated topics"

**If SOME INVALID:**
- Rounded rectangle: "Filter invalid topics"
- Rounded rectangle: "Supplement with mock topics"
- Rounded rectangle (YELLOW background): "Display mixed topics"
- Add note: "Partial AI success"

**PATH A1a-i-β: Invalid JSON**
- Rounded rectangle: "Log parsing error"
- Rounded rectangle (ORANGE background): "Generate intelligent mock data"
- Rounded rectangle: "Display 'AI response invalid' notice"

**PATH A1a-ii: Timeout/Error**
- Rounded rectangle: "Log timeout/error event"
- Rounded rectangle (ORANGE background): "Generate intelligent mock data based on profile"
- Rounded rectangle: "Display 'AI unavailable' notice"

**PATH A1b: AI Not Configured (NO)**
- Rounded rectangle (ORANGE background): "Generate intelligent mock data"
- Rounded rectangle: "Display 'AI not configured' notice"

**PATH A2: AI Disabled (NO)**
- Rounded rectangle (BLUE background): "Generate mock topics from predefined list"
- Rounded rectangle: "Filter by selected category"

**ALL PATHS MERGE HERE:**

**Step 11: Display Results**
- Rounded rectangle: "Display topics in grid"

**Step 12: Student Review (Loop)**
- Rounded rectangle: "Review topic cards"
- Start a **loop region** (dashed rectangle around the following):
  - Rounded rectangle: "Click to expand topic"
  - Rounded rectangle: "Read full description"
  - Diamond: "Like this topic?"
    - If YES: "Click favorite icon" → "Send POST to /api/favourites" → "Backend saves to database" → "Update UI (heart filled)"
  - Diamond: "More topics?"
    - If YES: Loop back to top
    - If NO: Continue

**Step 13: Final Action**
- Diamond: "Choose action"
  - Three paths:

**Path 1: Build proposal**
- Rounded rectangle: "Click 'Build Proposal'"
- Rounded rectangle (GREEN): "Navigate to Proposal Builder"
- Rounded rectangle: "Pre-fill project title from selected topic"
- **END** (black circle with ring)

**Path 2: View favourites**
- Rounded rectangle: "Navigate to Favourites page"
- Rounded rectangle: "View all saved topics (from backend)"
- **END**

**Path 3: Regenerate**
- Rounded rectangle: "Adjust filters"
- Rounded rectangle: "Click 'Generate' again"
- Loop back to Step 4
- **END**

**PATH B: Profile Incomplete (NO from Step 2)**

**Step 14: Incomplete Profile Handling**
- Rounded rectangle: "Display banner: 'Complete profile for personalized topics'"
- Rounded rectangle: "Allow browsing generic topics"
- Rounded rectangle: "Disable AI features"
- Diamond: "Complete profile now?"
  - If YES: "Navigate to Profile page" → **END**
  - If NO: "Browse generic topics" → **END**

#### Color Coding Legend:
- **GREEN background**: AI-powered success path
- **YELLOW background**: Partial AI success (mixed content)
- **ORANGE background**: Fallback to mock data
- **BLUE background**: Non-AI path (intentional)

#### Key Symbols:
- **Rounded rectangle**: Action/Activity
- **Diamond**: Decision point
- **Thick horizontal bar**: Fork/Join (parallel processes)
- **Dashed rectangle**: Loop or iteration region
- **Note box**: Additional information
- **Black filled circle**: Start
- **Black circle with ring**: End

---

### Activity Diagram 2: Proposal Building with AI-Assisted Content Generation

This diagram shows the multi-step process of building a project proposal with AI assistance for each section.

#### How to Draw This Activity Diagram

**Swimlanes (Vertical Columns):**
Create two swimlanes:
1. **Student** (left column)
2. **System** (right column)

#### Flow Steps to Draw:

**START** (black filled circle at top of Student swimlane)

**Step 1: Initiate Proposal**
- Student: Rounded rectangle: "Click 'Build Proposal'"

**Step 2: System Setup**
- System: Rounded rectangle: "Open proposal modal"
- System: Rounded rectangle: "Check localStorage for draft"
- System: Diamond: "Draft exists?"

**PATH A: Draft Exists (YES)**
- System: Rounded rectangle: "Show prompt: 'Load draft or start fresh?'"
- Student: Diamond: "Load draft?"
  - If YES:
    - System: "Parse JSON from localStorage"
    - System: "Populate form fields"
  - If NO (start fresh):
    - System: "Initialize empty proposal"
    - System: "Clear localStorage"

**PATH B: No Draft (NO)**
- System: "Initialize empty proposal"

**PATHS MERGE:**

**Step 3: Display Modal**
- System: Rounded rectangle: "Display modal with 6-step wizard:"
  - Add note: "Step 1: Project Info
Step 2: Background & Rationale
Step 3: Objectives
Step 4: Methodology
Step 5: Timeline & Deliverables
Step 6: Review & Download"
- System: Rounded rectangle: "Show progress bar (1/6 to 6/6)"

**PARTITION 1: Step-by-Step Wizard Flow** (Draw a large dashed rectangle around all steps)

**Step 4: Wizard Step 1 - Project Info**
- Student: Rounded rectangle: "Fill in project details"
  - Add note: "Title (required - can load from favourite topic), Program (pre-filled from profile), Supervisor (optional), Submission date (optional)"
- System: Rounded rectangle: "Show 'Load from Favorites' button"
- Student: Diamond: "Load from favourites?"
  - If YES:
    - System: "Send GET to /api/favourites"
    - System: "Display favourites modal"
    - Student: "Select a favourite topic"
    - System: "Pre-fill title and show topic category badge"
  - If NO: Continue
- System: Rounded rectangle: "Validate required fields"
- Student: Rounded rectangle: "Click 'Next' button"

**End of Step 1**

**PARTITION 2: Wizard Steps 2-5 - Content Generation** (Draw a large dashed rectangle)

**Step 5: Navigate to Content Step (2-5)**
- System: Rounded rectangle: "Update progress bar (e.g., 2/6)"
- System: Rounded rectangle: "Display section editor for: Background, Objectives, Methodology, or Timeline"
- Student: Rounded rectangle: "Choose content method"

**Step 6: Generation Method**
- Student: Diamond: "Use AI generation?"

**PATH 1: AI Generation (YES)**

**Step 7: System Validation**
- System: Rounded rectangle: "Validate prerequisites: Project title filled, Section type identified"
- System: Diamond: "Prerequisites met?"
  - If NO:
    - System: "Show validation error"
    - System: "Highlight missing fields"
    - Loop back
  - If YES: Continue

**Step 8: AI Call Setup**
- System: Rounded rectangle: "Update button: 'Generating...'"
- System: Rounded rectangle: "Build section-specific prompt"
  - Add note: "Include project title, student profile, format requirements"

**Step 9: Concurrent AI Call (Fork)**
- Draw **thick horizontal bar** (fork)
- Two parallel paths:
  - Path 1: "Call AI API"
  - Path 2: "Set 30-second timeout"
- Merge back with **thick horizontal bar** (join)

**Step 10: AI Response Check**
- System: Diamond: "AI responds?"
  - Two paths: "success" and "timeout/error"

**PATH 1a: Success**
- System: Rounded rectangle: "Parse response text"
- System: Rounded rectangle: "Validate content: Word count OK?, Structure correct?, Mentions project?"
- System: Diamond: "Content valid?"
  - If YES:
    - System: Rounded rectangle (GREEN): "Insert into editor"
    - System: "Button: 'Generated ✓'"
  - If NO (invalid):
    - System: Rounded rectangle (ORANGE): "Load template for section"
    - System: "Notify: 'Using template'"

**PATH 1b: Timeout/Error**
- System: Rounded rectangle (ORANGE): "Load predefined template"
- System: "Notify: 'AI unavailable, template loaded'"

**PATH 2: Manual Entry (NO)**
- Student: Rounded rectangle: "Type content manually"

**PATHS CONVERGE:**

**Step 11: Auto-save (Concurrent Process)**
- Draw a **fork bar**
- Parallel path: System: "Auto-save to localStorage (every 30 seconds)"
- This runs parallel to student editing

**Step 12: Edit Content**
- Student: Rounded rectangle: "Edit/refine content in rich text editor"
- Student: Rounded rectangle: "Check section completion"
- Student: Diamond: "More wizard steps?"
  - If YES (steps 2-5): "Click 'Next'" → "Increment progress bar" → Loop back to Step 5
  - If NO (completed step 5): "Click 'Next' to Review" → Proceed to Step 6

**End of Partition 2**

**PARTITION 3: Wizard Step 6 - Review & Download** (Draw a large dashed rectangle)

**Step 13: Review All Content**
- System: Rounded rectangle: "Update progress bar (6/6)"
- System: Rounded rectangle: "Display summary of all sections with edit buttons"
- Student: Rounded rectangle: "Review entire proposal content"
- Student: Diamond: "Need to edit a section?"
  - If YES:
    - Student: "Click 'Edit [Section]' button"
    - System: "Navigate back to that wizard step"
    - Arrow loops back to appropriate step (2-5)
  - If NO: Continue

**Step 14: Download Proposal**
- Student: Rounded rectangle: "Click 'Download Proposal' button"

**Step 15: Validate Proposal**
- System: Rounded rectangle: "Validate proposal: Project info complete?, Min 3 sections filled?"
- System: Diamond: "Validation passed?"

**PATH A: Validation Failed (NO)**
- System: "Show validation errors"
- System: "Highlight incomplete fields"
- Student: "Complete missing fields"
- Loop back to Step 14

**PATH B: Validation Passed (YES)**

**Step 16: Initialize PDF**
- System: Rounded rectangle: "Initialize jsPDF"

**Step 17: Generate Title Page**
- System: Rounded rectangle: "Generate title page: Centered project title, Student metadata table"
- System: Rounded rectangle: "Add page break"

**Step 18: Loop Through Sections**
- Draw **loop region** around:
  - System: "Add section heading"
  - System: "Format section content: Split text to page width, Apply proper spacing"
  - System: Diamond: "Content exceeds page?"
    - If YES: "Insert page break" → "Continue on new page"
  - Diamond: "More sections?"
    - If YES: Loop back
    - If NO: Continue

**Step 19: Finalize and Download**
- System: Rounded rectangle: "Generate filename: [title-sanitized]-proposal.pdf"
- System: Rounded rectangle: "Trigger browser download"
- System: Rounded rectangle (GREEN): "Show success notification"

**Step 20: Continue or Close**
- Student: Diamond: "Continue editing?"
  - If YES: "Modal stays open" → "Can re-download or edit" → Loop back to Step 13 (Review)
  - If NO: "Close modal" → **END**

**End of Partition 4**

**Note:** All wizard steps auto-save to localStorage every 30 seconds for draft recovery.

#### Color Coding:
- **GREEN**: Successful operation
- **ORANGE**: Fallback/error handling
- **No color**: Normal flow

#### Key Symbols:
- **Partition** (dashed rectangle with label): Logical grouping
- **Fork/Join** (thick horizontal bar): Parallel processes
- **Loop region** (dashed rectangle): Iteration

---

### Activity Diagram 3: User Authentication Flow (Backend Integration)

This diagram shows the complete authentication process including registration, login, and accessing protected routes.

#### How to Draw This Activity Diagram

**Swimlanes (Vertical Columns):**
Create four swimlanes:
1. **Student** (leftmost)
2. **Frontend** 
3. **Flask Backend**
4. **Database** (rightmost - can be combined with Backend if space limited)

#### Flow Steps to Draw:

**START** (black filled circle in Student swimlane)

**PARTITION 1: Registration** (Draw large dashed rectangle around registration steps)

**Step 1: Navigate to Registration**
- Student: Rounded rectangle: "Navigate to /register"

**Step 2: Fill Form**
- Student: Rounded rectangle: "Fill registration form"
  - Note: "Full name, Email, Password, Confirm password"
- Student: Rounded rectangle: "Submit form"

**Step 3: Client Validation**
- Frontend: Rounded rectangle: "Validate client-side: Email format, Password strength, Passwords match"
- Frontend: Diamond: "Client validation OK?"

**PATH A: Validation Failed (NO)**
- Frontend: Rounded rectangle: "Show inline errors"
- Student: Rounded rectangle: "Correct errors"
- Arrow loops back to "Submit form"

**PATH B: Validation Passed (YES)**

**Step 4: Send to Backend**
- Frontend: Rounded rectangle: "Send POST to /api/auth/register"

**Step 5: Backend Processing**
- Flask Backend: Rounded rectangle: "Receive registration data"
- Flask Backend: Rounded rectangle: "Validate server-side"
- Flask Backend: Rounded rectangle: "Query database for email"

**Step 6: Email Check**
- Flask Backend: Diamond: "Email exists?"

**PATH B1: Email Exists (YES)**
- Flask Backend: Rounded rectangle: "Return 409 Conflict"
- Frontend: Rounded rectangle (ORANGE): "Display 'Email already in use'"
- Student: Rounded rectangle: "Try different email"
- Arrow loops back to "Fill registration form"

**PATH B2: Email Unique (NO)**

**Step 7: Create User**
- Flask Backend: Rounded rectangle: "Hash password with bcrypt (cost factor 12)"
- Flask Backend: Rounded rectangle: "Create User model instance"
- Flask Backend: Rounded rectangle: "Commit to SQLite database"
- Flask Backend: Rounded rectangle: "Return 201 Created"

**Step 8: Success**
- Frontend: Rounded rectangle (GREEN): "Display success message"
- Frontend: Rounded rectangle: "Set flag: first_time_user = true"
- Frontend: Rounded rectangle: "Redirect to /login"
- Add note: "User must login to trigger onboarding"

**End of Partition 1**

**PARTITION 1A: Google OAuth Registration** (Draw large dashed rectangle)

**Step 8A: Alternative Registration - Google OAuth**
- Student: Rounded rectangle: "Click 'Sign in with Google' button"
- Frontend: Rounded rectangle: "Redirect to /api/auth/google/login"

**Step 8B: Google Authorization**
- Flask Backend: Rounded rectangle: "Redirect to Google OAuth consent screen"
- Student: Rounded rectangle: "Authorize application (select Google account)"
- Student: Rounded rectangle: "Grant permissions"

**Step 8C: OAuth Callback**
- Google: Rounded rectangle: "Return authorization code to /api/auth/google/callback"
- Flask Backend: Rounded rectangle: "Exchange code for access token"
- Flask Backend: Rounded rectangle: "Fetch user profile from Google"
- Flask Backend: Rounded rectangle: "Extract: email, name, google_id"

**Step 8D: User Lookup**
- Flask Backend: Diamond: "User with google_id exists?"

**PATH 1: Existing User (YES)**
- Flask Backend: Rounded rectangle: "Load user from database"
- Flask Backend: Rounded rectangle: "Update last_login timestamp"
- Go to Step 14 (Generate Token)

**PATH 2: New User (NO)**
- Flask Backend: Diamond: "Email already registered?"
  - If YES (email exists):
    - Flask Backend: Rounded rectangle: "Link Google account to existing user"
    - Flask Backend: "Update: google_id, auth_provider='google'"
    - Flask Backend: "Return 200 OK"
  - If NO (new user):
    - Flask Backend: Rounded rectangle: "Create User with: email, name, google_id, auth_provider='google', role='student', password_hash=NULL"
    - Flask Backend: Rounded rectangle: "Set onboarded=False"
    - Flask Backend: Rounded rectangle: "Commit to database"
- Go to Step 14 (Generate Token)

**End of Partition 1A**

**PARTITION 2: Login** (Draw large dashed rectangle)

**Step 9: Navigate to Login**
- Student: Rounded rectangle: "Navigate to /login"

**Step 10: Enter Credentials**
- Student: Rounded rectangle: "Enter credentials: Email, Password"
- Student: Rounded rectangle: "Click 'Login'"

**Step 11: Send Login Request**
- Frontend: Rounded rectangle: "Send POST to /api/auth/login"

**Step 12: Backend Query**
- Flask Backend: Rounded rectangle: "Receive credentials"
- Flask Backend: Rounded rectangle: "Query User by email"
- Flask Backend: Diamond: "User found?"

**PATH C1: User Not Found (NO)**
- Flask Backend: Rounded rectangle: "Return 401 Unauthorized (no user enumeration)"
- Frontend: Rounded rectangle (ORANGE): "Display 'Invalid credentials'"
- Student: Diamond: "Register instead?"
  - If YES: Loop back to Registration
  - If NO (retry): "Re-enter credentials" → Loop back to "Click Login"

**PATH C2: User Found (YES)**

**Step 13: Password Verification**
- Flask Backend: Rounded rectangle: "Retrieve password hash from database"
- Flask Backend: Rounded rectangle: "Compare using bcrypt: check_password_hash()"
- Flask Backend: Diamond: "Password matches?"

**PATH C2a: Password Incorrect (NO)**
- Flask Backend: Rounded rectangle: "Log failed attempt"
- Flask Backend: Rounded rectangle: "Return 401 Unauthorized"
- Frontend: Rounded rectangle (ORANGE): "Display 'Invalid credentials'"
- Student: Rounded rectangle: "Retry login"
- Arrow loops back to "Enter credentials"

**PATH C2b: Password Correct (YES)**

**Step 14: Generate Token**
- Flask Backend: Rounded rectangle: "Generate JWT token"
  - Note: "Payload: user_id, role, exp; Secret: JWT_SECRET_KEY; Expires: 24 hours"
- Flask Backend: Rounded rectangle: "Return 200 OK with: JWT token, User data (id, name, email, role, onboarded, auth_provider)"

**Step 15: Store Token and Check Onboarding**
- Frontend: Rounded rectangle: "Store token in localStorage"
- Frontend: Rounded rectangle: "Store user data in Vuex/state"
- Frontend: Diamond: "user.onboarded === false?"

**PATH E1: Not Onboarded (YES)**
- Frontend: Rounded rectangle (YELLOW): "Display onboarding modal"
- Student: Rounded rectangle: "Complete onboarding steps: Program, Year of Study, Interests"
- Student: Rounded rectangle: "Click 'Finish Onboarding'"
- Frontend: Rounded rectangle: "Send PUT to /api/auth/onboarding"
- Flask Backend: Rounded rectangle: "Update user.onboarded = True"
- Flask Backend: Rounded rectangle: "Update profile fields"
- Frontend: Rounded rectangle (GREEN): "Close onboarding modal"
- Frontend: Rounded rectangle: "Redirect to /dashboard"

**PATH E2: Already Onboarded (NO)**
- Frontend: Rounded rectangle (GREEN): "Redirect to /dashboard"

**PATHS MERGE:**

**Step 16: Access Features**
- Student: Rounded rectangle: "Access protected features"
- **END** (black circle with ring)

**End of Partition 2**

**PARTITION 3: Accessing Protected Routes** (Draw large dashed rectangle)

**Step 17: Navigate to Protected Page**
- Student: Rounded rectangle: "Navigate to protected page (e.g., /topics, /profile)"

**Step 18: Check Token**
- Frontend: Rounded rectangle: "Retrieve token from localStorage"
- Frontend: Diamond: "Token exists?"

**PATH D1: No Token (NO)**
- Frontend: Rounded rectangle: "Redirect to /login"
- Frontend: Rounded rectangle (ORANGE): "Display 'Please login'"
- Student: Rounded rectangle: "Login to continue"
- Arrow loops back to Partition 2 (Login)

**PATH D2: Token Exists (YES)**

**Step 19: Send Request with Token**
- Frontend: Rounded rectangle: "Add Authorization header: Bearer <token>"
- Frontend: Rounded rectangle: "Send API request"

**Step 20: Verify Token**
- Flask Backend: Rounded rectangle: "Extract token from header"
- Flask Backend: Rounded rectangle: "Verify JWT signature"
- Flask Backend: Rounded rectangle: "Check expiration"
- Flask Backend: Diamond: "Token valid?"

**PATH D2a: Token Invalid/Expired (NO)**
- Flask Backend: Rounded rectangle: "Return 401 Unauthorized"
- Frontend: Rounded rectangle: "Clear invalid token"
- Frontend: Rounded rectangle: "Redirect to /login"
- Frontend: Rounded rectangle (ORANGE): "Display 'Session expired'"
- Student: Rounded rectangle: "Login again"
- Arrow loops back to Partition 2 (Login)

**PATH D2b: Token Valid (YES)**

**Step 21: Execute Request**
- Flask Backend: Rounded rectangle: "Extract user_id from payload"
- Flask Backend: Rounded rectangle: "Execute route handler"
- Flask Backend: Rounded rectangle: "Return requested data"

**Step 22: Render Page**
- Frontend: Rounded rectangle: "Render page with data"
- Student: Rounded rectangle: "Use feature"
- **END**

**End of Partition 3**

#### Color Coding:
- **GREEN**: Successful authentication/operation
- **YELLOW**: Onboarding required
- **ORANGE**: Error or failure state
- **No color**: Normal processing

#### Security Highlights (Add as notes):
- "Bcrypt hashing - password never stored in plaintext (email auth only)"
- "Google OAuth - no password required, google_id used for identity"
- "No user enumeration - same error for invalid email/password"
- "JWT expiration - tokens auto-expire after 24 hours"
- "Token verification - every protected route checks validity"
- "Role-based access - admin routes require role='admin' in JWT payload"

#### Key Symbols:
- **Partition**: Dashed rectangle grouping related steps
- **Loop arrows**: Show retry/error recovery flows
- **Multiple swimlanes**: Show interaction between system components

---

## 4. Summary of Core Use Cases

| Use Case | Complexity | AI Involved | Activity Diagram | Priority | Status |
|----------|-----------|-------------|------------------|----------|--------|
| UC1: Register Account | Medium | No | Yes | High | ✅ Implemented |
| UC2: Login to System | Medium | No | Yes | High | ✅ Implemented |
| UC2A: Login with Google OAuth | Medium | No | No | High | ✅ Implemented |
| UC3: Complete Onboarding | Low | No | No | Medium | ✅ Implemented |
| UC4: Complete Student Profile | Medium | No | No | High | ✅ Implemented |
| UC5: Discover Research Topics | High | Yes | Yes | Critical | ✅ Implemented |
| UC6: Generate AI Topics | High | Yes | Part of UC5 | Critical | ✅ Implemented |
| UC7: Save Favorite Projects | Medium | No | No | High | ✅ Implemented |
| UC8: Build Project Proposal | High | Yes | Yes | Critical | ✅ Implemented |
| UC9: Generate Proposal Sections | High | Yes | Part of UC8 | Critical | ✅ Implemented |
| UC10: Download Proposal as PDF | Medium | No | Part of UC8 | High | ✅ Implemented |
| UC11: Track Project Progress | High | No | No | High | ✅ Implemented |
| UC12: Manage Favourites | Medium | No | No | High | ✅ Implemented |
| UC13: Create Workspace | Medium | No | No | Medium | ✅ Implemented |
| UC14: Collaborate on Project | High | No | No | Medium | ✅ Implemented |
| UC15: Real-time Chat | High | No | No | Medium | ✅ Implemented |
| UC16: Share Files | Medium | No | No | Medium | ✅ Implemented |
| UC17: Admin Dashboard | Medium | No | No | Low | ✅ Implemented |
| UC18: Manage Users | Medium | No | No | Low | ✅ Implemented |
| UC19: View Analytics | Medium | No | No | Low | ✅ Implemented |

**Complexity Rationale:**
- **High**: Multi-step workflow, AI integration, real-time features, complex state management
- **Medium**: Database operations, validation, user interaction, CRUD operations
- **Low**: Simple UI flows, straightforward logic

**Implementation Notes:**
- All core use cases (UC1-UC19) are fully implemented and functional
- Google OAuth (UC2A) integrated with Authlib
- Workspaces feature (UC13-UC16) includes WebSocket support via Socket.IO
- Admin features (UC17-UC19) protected by role-based access control
- Favourites now persisted to backend (not just localStorage)
- Progress tracking includes phases and tasks with auto-calculation

---

## 5. Technology Stack Reference

### Frontend
- **Framework**: Vue 3 (Composition API with `<script setup>`)
- **Styling**: Tailwind CSS with custom design system (primary/secondary colors)
- **Build Tool**: Vite (fast HMR, optimized builds)
- **State Management**: Reactive refs + Services pattern (no Pinia/Vuex)
- **PDF Generation**: jsPDF library (client-side)
- **Icons**: Lucide Vue Next (tree-shakeable)
- **HTTP Client**: Fetch API (native)
- **Real-time**: Socket.IO client (for workspaces)

### Backend
- **Framework**: Flask (Python 3.x)
- **ORM**: Flask-SQLAlchemy (declarative models)
- **Database**: SQLite (development), PostgreSQL-compatible (production)
- **Authentication**: Flask-JWT-Extended (stateless JWT tokens)
- **Password Hashing**: bcrypt (cost factor 12)
- **CORS**: Flask-CORS (cross-origin support)
- **OAuth**: Authlib (Google OAuth 2.0 integration)
- **WebSockets**: Flask-SocketIO (real-time chat)
- **Migrations**: Flask-Migrate (Alembic)

### AI Services
- **Primary**: Google Gemini API (via backend proxy to avoid CORS)
- **Alternatives**: OpenAI GPT (direct from frontend), HuggingFace Inference
- **Integration**: Fetch API for HTTP requests, 30s timeout
- **Fallback**: Intelligent mock data generation (50+ predefined topics)

### Storage
- **User Data**: SQLite database via Flask backend
  - Tables: User, StudentProfile, ProjectTopic, SavedProject, GeneratedProject
  - Workspaces: Workspace, WorkspaceMember, WorkspaceMessage, WorkspaceFile
  - Progress: ProjectPhase, PhaseTask
  - Admin: UserActivity, UserSkill, ResourceCategory, GlobalResource
- **Drafts**: Browser localStorage (proposal drafts)
- **Sessions**: JWT tokens (s → Falls back to intelligent mock data
- API keys not configured → Uses predefined topics
- Network connectivity issues → Cached data + localStorage
- Browser storage disabled → Core features still work
- WebSocket fails → Polling fallback for chat

**Strategy**: Multi-level fallback (AI → Intelligent Mock → Basic Functionality)

### User-Centric Design
- **Instant feedback**: Optimistic UI updates before backend confirmation
- **Clear error messages**: No technical jargon, actionable guidance
- **Progress indicators**: Loading states, progress bars, step counters
- **Undo/edit options**: Mistakes are recoverable (draft system)
- **Onboarding**: Interactive first-time user guide

### Performance
- **Target load times**: < 3 seconds for any page
- **AI timeouts**: 30-second max to prevent hanging
- **Caching**: AI responses, user profiles, workspace data
- **Lazy loading**: Components loaded as needed
- **Optimistic UI**: Assume success, revert on error
- **WebSocket**: Real-time updates without polling

### Security
- **Password security**: Bcrypt with cost factor 12, never stored in plaintext
- **Token management**: JWT with automatic expiration handling
- **Input validation**: Client-side AND server-side validation
- **No user enumeration**: Consistent error messages for auth failures
- **CORS protection**: Backend CORS configured properly
- **File upload security**: Type and size validation, no executables
- **Implemented Features ✅
1. **Collaboration**: ✅ Workspaces with real-time chat, file sharing, member invites
2. **Progress Tracking**: ✅ Project phases, tasks, timeline, status management
3. **Admin Dashboard**: ✅ User management, analytics, system statistics
4. **Google OAuth**: ✅ Social login integration
5. **Favourites System**: ✅ Backend-persisted saved projects
6. **Onboarding**: ✅ Interactive first-time user guide

### Planned Features
1. **Version History**: Track proposal revisions with diff view
2. **Supervisor Matching**: AI-powered supervisor recommendation system
3. **Template Library**: Pre-built proposal templates by discipline
4. **Real-time AI**: Streaming AI responses (SSE or WebSocket)
5. **Email Notifications**: Workspace invites, deadline alerts, activity digests
6. **Mobile App**: Native iOS/Android apps with offline mode
7. **AI Chat Assistant**: Conversational project guidance chatbot
8. **Plagiarism Checker**: Ensure proposal originality
9. **Export Options**: Export favourites as CSV, proposals as DOCX
10. **Calendar Integration**: Sync project deadlines with Google Calendar

### AI Improvements (Future)
- **Fine-tuned models**: Train on actual FYP proposals from universities
- **Multi-language**: Generate proposals in multiple languages
- **Citation generator**: Auto-generate references in APA/IEEE/Harvard
- **Code integration**: Generate starter code for projects
- **Literature review**: Auto-suggest relevant research paperbmit
- **Color contrast**: WCAG AA compliant
- **Screen reader**: Semantic HTML, ARIA labels
- `UserActivity`: Activity tracking for analytics
- `ResourceCategory`: Categories for global resources
- `GlobalResource`: System-wide educational resources

---

## 6. Design Principles

### Graceful Degradation
System remains fully functional even when:
- AI services are unavailable
- API keys not configured
- Network connectivity issues
- Browser storage disabled

**Strategy**: Multi-level fallback (AI → Intelligent Mock → Generic Mock)

### User-Centric Design
- **Instant feedback**: UI updates before backend confirmation
- **Clear error messages**: No technical jargon
- **Progress indicators**: Students know what's happening
- **Undo/edit options**: Mistakes are recoverable

### Performance
- **Target load times**: < 3 seconds for any page
- **Caching**: Reuse AI responses when appropriate
- **Lazy loading**: Load components as needed
- **Optimistic UI**: Assume success, revert on error

### Security
- **Password security**: Bcrypt with cost factor 12
- **Token expiration**: 24-hour JWT validity
- **Input validation**: Client and server-side
- **No user enumeration**: Consistent error messages
- **HTTPS required**: For production deployment

---

## 7. Future Enhancements

### Planned Features
1. **Collaboration**: Multiple students on same proposal
2. **Version History**: Track proposal revisions
3. **Supervisor Review**: Submit for feedback
4. **Template Library**: Pre-built proposal templates
5. **Real-time AI**: Streaming AI responses
6. **Analytics Dashboard**: Track student progress
7. **Notification System**: Email alerts for deadlines
8. **Mobile App**: Native iOS/Android apps

### AI Improvements
- **Fine-tuned models**: Train on actual FYP proposals
- **Multi-language**: Generate in multiple languages
- **Plagiarism detection**: Ensure originality
- **Citation generator**: Auto-generate references

---

*Document Version: 2.0*  
*Last Updated: December 26, 2025*  
*Author: FYP Guidance System Team*  
*Status: Comprehensive - Reflects Full Implementation*

**Major Updates in v2.0:**
- ✅ Added Google OAuth authentication (UC2A)
- ✅ Added Onboarding flow (UC3)
- ✅ Added Workspaces and Collaboration (UC13-UC16)
- ✅ Added Progress Tracking (UC11)
- ✅ Added Backend-persisted Favourites (UC12)
- ✅ Added Admin Dashboard and Analytics (UC17-UC19)
- ✅ Updated all use cases to reflect actual implementation
- ✅ Corrected API endpoints and database models
- ✅ Added WebSocket/Socket.IO real-time features
- ✅ Updated technology stack with accurate details
- ✅ Removed deprecated supervisor matching features (not implemented)
- ✅ Added comprehensive implementation status
