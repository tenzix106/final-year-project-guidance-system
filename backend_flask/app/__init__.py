import os
from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, migrate, bcrypt, jwt, cors
from .auth.routes import auth_bp
from .favourites.routes import favourites_bp
from .progress import progress_bp
from . import models  # ensure models are registered for migrations


def create_app() -> Flask:
    # Load environment variables from a .env file if present
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config())

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(favourites_bp, url_prefix="/api/favourites")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")

    return app

