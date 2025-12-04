import os
from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, migrate, bcrypt, jwt, cors
from .auth.routes import auth_bp, init_oauth
from .favourites.routes import favourites_bp
from .progress import progress_bp
from . import models  # ensure models are registered for migrations


def create_app() -> Flask:
    # Load environment variables from a .env file if present
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config())
    
    # Disable strict slashes to prevent redirects
    app.url_map.strict_slashes = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize OAuth
    init_oauth(app)
    
    # Configure CORS with proper settings
    cors.init_app(
        app, 
        resources={r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }}
    )

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(favourites_bp, url_prefix="/api/favourites")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")

    return app

