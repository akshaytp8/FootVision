"""Application configuration for FootVision.

The production deployment uses SQLite on PythonAnywhere.
The SQLite database lives in Flask's instance/ directory.
"""

import os


class Config:
    SECRET_KEY = os.environ.get("FOOTVISION_SECRET_KEY", "change-this-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLite is intentional for the PythonAnywhere deployment.
    # Flask-SQLAlchemy resolves this relative SQLite path inside app.instance_path.
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
