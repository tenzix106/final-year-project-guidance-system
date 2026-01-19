# Google OAuth Setup Guide

## Overview
Google OAuth authentication has been successfully integrated into the FYP Guidance System. Users can now sign in with their Google accounts in addition to traditional email/password authentication.

## What Was Implemented

### Backend (Flask)
1. **Authlib Package**: Installed for OAuth 2.0 handling
2. **User Model Updates**: Added `google_id` and `auth_provider` fields
3. **OAuth Endpoints**:
   - `GET /api/auth/google/login` - Initiates Google OAuth flow
   - `GET /api/auth/google/callback` - Handles Google's callback with user info
4. **Database Migration**: Applied migration to add new fields to existing users

### Frontend (Vue 3)
1. **Google Sign-In Button**: Added to AuthModal component
2. **OAuth Callback Handler**: Automatically captures JWT token from URL after OAuth
3. **Seamless Integration**: Works alongside existing email/password authentication

## Setup Instructions

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth 2.0 Client ID**
5. Configure the OAuth consent screen if prompted:
   - User Type: External (for testing)
   - Add your email as a test user
   - Scopes: email, profile, openid
6. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: FYP Guidance System (or your preferred name)
   - Authorized JavaScript origins:
     ```
     http://localhost:3000
     http://127.0.0.1:3000
     ```
   - Authorized redirect URIs:
     ```
     http://localhost:5000/api/auth/google/callback
     http://127.0.0.1:5000/api/auth/google/callback
     ```
7. Copy the **Client ID** and **Client Secret**

### Step 2: Configure Backend Environment

1. Navigate to `backend_flask/` directory
2. Create a `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and add your Google OAuth credentials:
   ```env
   # Flask Configuration
   SECRET_KEY=your-random-secret-key-here
   JWT_SECRET_KEY=your-random-jwt-secret-here
   
   # Database
   DATABASE_URL=sqlite:///app.db
   
   # Google OAuth Configuration
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   
   # Frontend URL (for OAuth redirects)
   FRONTEND_URL=http://localhost:3000
   ```

### Step 3: Run the Application

1. **Start Flask Backend** (Terminal 1):
   ```bash
   cd backend_flask
   flask --app wsgi run --debug
   ```
   Backend will run on `http://127.0.0.1:5000`

2. **Start Frontend** (Terminal 2):
   ```bash
   npm run dev
   ```
   Frontend will run on `http://localhost:3000`

### Step 4: Test Google OAuth

1. Open your browser to `http://localhost:3000`
2. Click the **Sign In** button in the top-right corner
3. In the auth modal, click **Continue with Google**
4. You'll be redirected to Google's consent screen
5. Sign in with your Google account and grant permissions
6. You'll be redirected back to the app, automatically signed in

## How It Works

### OAuth Flow

1. **User clicks "Continue with Google"**
   - Frontend redirects to: `http://127.0.0.1:5000/api/auth/google/login`

2. **Flask initiates OAuth flow**
   - Redirects user to Google's consent page with your Client ID
   - Google asks user to sign in and grant permissions

3. **Google redirects to callback**
   - Google calls: `http://127.0.0.1:5000/api/auth/google/callback?code=...`
   - Flask exchanges authorization code for access token
   - Flask fetches user info from Google (email, name, google_id)

4. **User creation/login**
   - If user exists (by google_id or email): log them in
   - If new user: create account with Google info
   - If existing email user signs in with Google: link accounts

5. **JWT token generation**
   - Flask creates a JWT token for the user
   - Redirects to frontend: `http://localhost:3000?token=JWT_TOKEN`

6. **Frontend completes authentication**
   - authService captures token from URL
   - Stores token in localStorage
   - Fetches user details
   - Updates UI to show logged-in state

### Account Linking

- If a user signs up with email/password (`user@example.com`)
- Then later signs in with Google using the same email
- The system automatically links the accounts
- `auth_provider` is updated to `'google'`
- User can now sign in with either method

## Database Schema

### User Model Fields

```python
id: Integer (Primary Key)
email: String (Unique, Not Null)
password_hash: String (Nullable - for OAuth users)
google_id: String (Unique, Nullable - Google user ID)
auth_provider: String (Default: 'email', Options: 'email' | 'google')
full_name: String (Nullable - populated from Google)
created_at: DateTime
# ... other profile fields
```

## Security Features

1. **HTTPS in Production**: Ensure you use HTTPS for production deployments
2. **Secure Tokens**: JWT tokens are signed with your JWT_SECRET_KEY
3. **OAuth State Protection**: Authlib handles CSRF protection automatically
4. **Token Expiration**: JWT tokens expire (configure in Flask-JWT-Extended settings)
5. **Scope Limitation**: Only requests `openid email profile` scopes from Google

## Troubleshooting

### "Google OAuth not configured" Error
- Check that `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set in `.env`
- Restart the Flask server after adding credentials

### "redirect_uri_mismatch" Error
- Ensure your redirect URI in Google Console exactly matches:
  `http://127.0.0.1:5000/api/auth/google/callback`
- Check for trailing slashes (should NOT have one)

### "Access blocked: This app's request is invalid"
- Complete the OAuth consent screen configuration
- Add your email as a test user in Google Console
- Ensure scopes are configured: `openid email profile`

### User Not Logged In After OAuth
- Check browser console for errors
- Verify Flask backend is running on port 5000
- Check that `FRONTEND_URL` in `.env` matches your frontend URL

### Database Errors
- If migration fails, ensure Flask backend is not running
- Try: `flask --app wsgi db stamp head` to reset migration state
- Then: `flask --app wsgi db upgrade` to apply migrations

## Production Deployment

### Environment Variables

Update these for production:

```env
# Use strong random keys
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-production-jwt-secret

# Production database (e.g., PostgreSQL)
DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Google OAuth (same Client ID, or create production credentials)
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret

# Production frontend URL
FRONTEND_URL=https://yourdomain.com
```

### Google Console Updates

1. Add production URLs to **Authorized JavaScript origins**:
   ```
   https://yourdomain.com
   ```

2. Add production callback to **Authorized redirect URIs**:
   ```
   https://api.yourdomain.com/api/auth/google/callback
   ```

3. Update OAuth consent screen:
   - Publishing status: In production
   - Add privacy policy and terms of service URLs

### Security Checklist

- [ ] Use HTTPS everywhere
- [ ] Set secure, random SECRET_KEY and JWT_SECRET_KEY
- [ ] Configure CORS properly (don't use `origins: "*"` in production)
- [ ] Set JWT expiration times
- [ ] Enable Flask-JWT-Extended security features
- [ ] Use production-grade database (PostgreSQL, MySQL)
- [ ] Set up proper logging and monitoring
- [ ] Keep dependencies updated

## Testing

### Test User Creation
1. Sign in with Google using a new email
2. Check database: `google_id` and `auth_provider='google'` should be set
3. Verify user has no `password_hash`

### Test Account Linking
1. Create account with email/password
2. Sign out
3. Sign in with Google using same email
4. Check database: `google_id` added, `auth_provider` updated to `'google'`

### Test JWT Flow
1. Sign in with Google
2. Check browser localStorage for `auth_token`
3. Make API request to `/api/auth/me` with token
4. Should return user info

## Support

For issues or questions:
1. Check Flask backend logs for detailed error messages
2. Check browser console for frontend errors
3. Verify all environment variables are correctly set
4. Ensure Google OAuth credentials are valid and scopes are granted
