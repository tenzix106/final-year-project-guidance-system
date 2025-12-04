from flask import Blueprint, request, jsonify, url_for, redirect
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from authlib.integrations.flask_client import OAuth
from ..extensions import db
from ..models import User
import os


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


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

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


@auth_bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "user not found"}), 404
    return jsonify({
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "auth_provider": user.auth_provider
    })

