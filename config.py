"""
config.py
---------
App settings. That's it.
"""

import os

class Config:
    SECRET_KEY = "losblancos-secret-key-2026"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Use PostgreSQL on Render, SQLite locally
    if os.environ.get("DATABASE_URL"):
        # Render provides DATABASE_URL
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    else:
        # Local development — use SQLite (no psycopg2 needed)
        db_url = os.environ.get("DATABASE_URL") or "postgresql://localhost/FootVision"
# Fix URL prefix for psycopg v3 and SQLAlchemy compatibility
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql+psycopg://", 1)
        elif db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+psycopg://", 1)
        SQLALCHEMY_DATABASE_URI = db_url
