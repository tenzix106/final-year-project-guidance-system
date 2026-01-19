# Profile Completion Feature

## Overview
New users are now required to complete their profile before accessing the main system. This ensures we have essential user information for personalized project recommendations.

## User Flow

### 1. Authentication
- User registers or logs in (email/password or Google OAuth)
- For OAuth users, they are redirected back with a JWT token in the URL

### 2. Profile Completion Check
- System checks if `onboarding_completed` is `false`
- Triggered in two ways:
  - **After email/password authentication**: `handleAuthSuccess()` checks immediately
  - **After OAuth callback**: `onMounted()` and `watch()` detect the authenticated user
- If not completed, **ProfileCompletionModal** is shown (cannot be closed)
- If completed, user proceeds to main system

### 3. Profile Completion Modal

#### Step 1: Basic Information (Required)
- **Full Name** - User's complete name
- **University/Institution** - Educational institution
- **Program/Major** - Field of study (dropdown with "Other" option)
- **Academic Year** - Current year level

#### Step 2: Interests & Skills (Optional)
- **Areas of Interest** - Research/project interests (comma-separated)
- **Technical Skills** - Programming languages, tools, etc. (comma-separated)
- **Project Type Preference** - Research/Development/Both/No Preference
- **Expected Project Duration** - 3-4, 4-6, 6-8, or 8-12 months

### 4. Actions
- **Next** - Proceed from Step 1 to Step 2 (validates required fields)
- **Back** - Return to Step 1 from Step 2
- **Skip for now** - Complete onboarding without filling optional fields
- **Complete Profile** - Save all information and mark onboarding as complete

## Technical Implementation

### Database Schema
New fields added to `User` model:
```python
# Basic profile fields (already existed)
full_name = db.Column(db.String(255), nullable=True)
university = db.Column(db.String(255), nullable=True)
program = db.Column(db.String(100), nullable=True)
academic_year = db.Column(db.String(10), nullable=True)

# New extended profile fields
interests = db.Column(JSON, nullable=True)  # Array of strings
skills = db.Column(JSON, nullable=True)  # Array of strings
project_preference = db.Column(db.String(50), nullable=True)
expected_duration = db.Column(db.String(20), nullable=True)
```

### Backend Endpoints

#### PUT `/api/auth/profile`
Updates user profile information.

**Request Body:**
```json
{
  "full_name": "John Doe",
  "university": "Example University",
  "program": "Computer Science",
  "academic_year": "Year 3",
  "interests": ["AI", "Web Development"],
  "skills": ["Python", "JavaScript", "React"],
  "project_preference": "Both",
  "expected_duration": "6-8 months"
}
```

**Response:**
```json
{
  "message": "profile updated successfully",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "university": "Example University",
    "program": "Computer Science",
    "academic_year": "Year 3",
    "interests": ["AI", "Web Development"],
    "skills": ["Python", "JavaScript", "React"],
    "project_preference": "Both",
    "expected_duration": "6-8 months",
    "auth_provider": "email",
    "onboarding_completed": true,
    "role": "student"
  }
}
```

#### POST `/api/auth/complete-onboarding`
Marks onboarding as completed (sets `onboarding_completed` to `true`).

### Frontend Components

#### ProfileCompletionModal.vue
- Two-step form with progress indicator
- Client-side validation for required fields
- Parses comma-separated inputs into arrays
- Calls `authService.updateProfile()` and `authService.completeOnboarding()`
- Emits `@completed` event when done

#### App.vue Integration
```javascript
// Show profile completion for new users after email/password auth
const handleAuthSuccess = async (type) => {
  if (currentUser.value && !currentUser.value.onboarding_completed) {
    profileCompletionModalOpen.value = true
  } else {
    setActiveView('home')
  }
}

// Check for OAuth users on mount
onMounted(() => {
  if (isAuthenticated.value && currentUser.value && !currentUser.value.onboarding_completed) {
    setTimeout(() => {
      profileCompletionModalOpen.value = true
    }, 500)
  }
})

// Watch for OAuth authentication completion
watch([isAuthenticated, currentUser], ([newAuth, newUser]) => {
  if (newAuth && newUser && !newUser.onboarding_completed && !profileCompletionModalOpen.value) {
    profileCompletionModalOpen.value = true
  }
}, { deep: true })

// Handle completion
const handleProfileCompletion = async (skipped) => {
  profileCompletionModalOpen.value = false
  setActiveView('home')
}
```

## Benefits

1. **Better Personalization** - Profile data enables more relevant project suggestions
2. **User Segmentation** - Understand user demographics and interests
3. **Analytics** - Track which programs and skills are most common
4. **Future Features** - Foundation for advanced recommendation algorithms

## Migration

Applied migration: `9826b652d71c_add_profile_completion_fields_to_user_.py`

Adds 4 new columns to `user` table:
- `interests` (JSON)
- `skills` (JSON)
- `project_preference` (VARCHAR(50))
- `expected_duration` (VARCHAR(20))

## Testing Checklist

- [ ] New email registration shows profile completion modal
- [ ] Google OAuth registration shows profile completion modal
- [ ] Existing Google user login (already completed profile) doesn't show modal
- [ ] OAuth callback correctly stores token and fetches user data
- [ ] Profile completion modal appears after OAuth redirect
- [ ] Cannot close modal without completing or skipping
- [ ] Step 1 validation works (required fields)
- [ ] Step 2 optional fields can be left empty
- [ ] "Skip for now" marks onboarding as complete
- [ ] "Complete Profile" saves all data correctly
- [ ] Profile data appears in `/api/auth/me` response
- [ ] Existing users with `onboarding_completed=true` not affected
- [ ] Profile can be edited later via Edit Profile button
- [ ] Multiple OAuth login attempts don't show modal repeatedly
