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
        SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
