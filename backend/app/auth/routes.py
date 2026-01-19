from flask import Blueprint, request, jsonify, url_for, redirect
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from authlib.integrations.flask_client import OAuth
from ..extensions import db
from ..models import User
import os
import re


auth_bp = Blueprint("auth", __name__)

# Initialize OAuth
oauth = OAuth()


def init_oauth(app):
    """Initialize OAuth with the Flask app"""
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    return oauth


def validate_password(password):
    """Validate password strength
    Requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one number
    - Contains at least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
    
    return True, "Password is valid"


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    # Validate password strength
    is_valid, message = validate_password(password)
    if not is_valid:
        return jsonify({"message": message}), 400

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "email already registered"}), 409

    user = User(email=email, auth_provider='email')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "email": user.email}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return jsonify({"message": "invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token})


@auth_bp.get("/google/login")
def google_login():
    """Initiate Google OAuth flow"""
    if not os.getenv('GOOGLE_CLIENT_ID') or not os.getenv('GOOGLE_CLIENT_SECRET'):
        return jsonify({"message": "Google OAuth not configured"}), 500
    
    # Get the frontend URL from environment or use default
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    redirect_uri = url_for('auth.google_callback', _external=True)
    
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.get("/google/callback")
def google_callback():
    """Handle Google OAuth callback"""
    try:
        # Exchange authorization code for access token
        token = oauth.google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            user_info = oauth.google.userinfo()
        
        google_id = user_info.get('sub')
        email = user_info.get('email')
        full_name = user_info.get('name')
        
        if not google_id or not email:
            return redirect(f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}?error=invalid_google_response")
        
        # Check if user exists by google_id or email
        user = User.query.filter_by(google_id=google_id).first()
        if not user:
            user = User.query.filter_by(email=email).first()
            if user:
                # Link existing email account to Google
                user.google_id = google_id
                user.auth_provider = 'google'
            else:
                # Create new user
                user = User(
                    email=email,
                    google_id=google_id,
                    auth_provider='google',
                    full_name=full_name
                )
                db.session.add(user)
        else:
            # Update full name if it has changed
            if full_name and user.full_name != full_name:
                user.full_name = full_name
        
        db.session.commit()
        
        # Create JWT token
        jwt_token = create_access_token(identity=str(user.id))
        
        # Redirect to frontend with token
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}?token={jwt_token}")
        
    except Exception as e:
        print(f"Google OAuth error: {str(e)}")
        return redirect(f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}?error=oauth_failed")


@auth_bp.post("/complete-onboarding")
@jwt_required()
def complete_onboarding():
    """Mark user's onboarding as completed"""
    user_id = get_jwt_identity()
    # Convert to int since JWT identity is stored as string
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid token"}), 401
    
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "user not found"}), 404
    
    user.onboarding_completed = True
    db.session.commit()
    
    return jsonify({"message": "onboarding completed", "onboarding_completed": True})


@auth_bp.put("/profile")
@jwt_required()
def update_profile():
    """Update user profile information"""
    user_id = get_jwt_identity()
    print(f"[DEBUG] Profile update - JWT identity: {user_id}")
    
    # Convert to int since JWT identity is stored as string
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        print(f"[ERROR] Invalid user_id type: {type(user_id)}, value: {user_id}")
        return jsonify({"message": "Invalid token"}), 401
    
    user = User.query.get(user_id)
    if user is None:
        print(f"[ERROR] User not found with id: {user_id}")
        return jsonify({"message": "user not found"}), 404
    
    data = request.get_json(silent=True) or {}
    print(f"[DEBUG] Profile update data: {data}")
    
    # Update allowed fields
    if 'full_name' in data:
        user.full_name = data['full_name'].strip() if data['full_name'] else None
    if 'university' in data:
        user.university = data['university'].strip() if data['university'] else None
    if 'program' in data:
        user.program = data['program'].strip() if data['program'] else None
    if 'academic_year' in data:
        user.academic_year = data['academic_year'].strip() if data['academic_year'] else None
    
    # Update extended profile fields
    if 'interests' in data:
        user.interests = data['interests'] if isinstance(data['interests'], list) else None
    if 'skills' in data:
        user.skills = data['skills'] if isinstance(data['skills'], list) else None
    if 'project_preference' in data:
        user.project_preference = data['project_preference'].strip() if data['project_preference'] else None
    if 'expected_duration' in data:
        user.expected_duration = data['expected_duration'].strip() if data['expected_duration'] else None
    
    db.session.commit()
    print(f"[DEBUG] Profile updated successfully for user {user_id}")
    
    return jsonify({
        "message": "profile updated successfully",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "university": user.university,
            "program": user.program,
            "academic_year": user.academic_year,
            "interests": user.interests,
            "skills": user.skills,
            "project_preference": user.project_preference,
            "expected_duration": user.expected_duration,
            "auth_provider": user.auth_provider,
            "onboarding_completed": user.onboarding_completed,
            "role": user.role
        }
    })


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    # Convert to int since JWT identity is stored as string
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid token"}), 401
    
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "user not found"}), 404
    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "university": user.university,
        "program": user.program,
        "academic_year": user.academic_year,
        "interests": user.interests,
        "skills": user.skills,
        "project_preference": user.project_preference,
        "expected_duration": user.expected_duration,
        "auth_provider": user.auth_provider,
        "onboarding_completed": user.onboarding_completed,
        "role": user.role
    })


@auth_bp.post("/change-password")
@jwt_required()
def change_password():
    """Change user password (email auth only)"""
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"message": "Invalid token"}), 401
    
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "user not found"}), 404
    
    # Only allow password change for email auth users
    if user.auth_provider != 'email':
        return jsonify({"message": "Password change not available for OAuth accounts"}), 403
    
    data = request.get_json(silent=True) or {}
    current_password = data.get("current_password") or ""
    new_password = data.get("new_password") or ""
    
    if not current_password or not new_password:
        return jsonify({"message": "Current password and new password are required"}), 400
    
    if len(new_password) < 6:
        return jsonify({"message": "New password must be at least 6 characters"}), 400
    
    # Verify current password
    if not user.check_password(current_password):
        return jsonify({"message": "Current password is incorrect"}), 401
    
    # Update password
    user.set_password(new_password)
    db.session.commit()
    
    return jsonify({"message": "Password changed successfully"}), 200
