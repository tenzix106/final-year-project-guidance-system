import os
from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, migrate, bcrypt, jwt, cors
from .auth.routes import auth_bp
from .ai.routes import ai_bp


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config())

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

    from . import models  # noqa: F401 ensure models imported for migrations

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")

    return app

