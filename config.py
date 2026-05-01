"""
config.py
---------
App settings. That's it.
"""

import os

class Config:
    SECRET_KEY = "losblancos-secret-key-2026"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    db_url = os.environ.get("DATABASE_URL") or "sqlite:///database.db"

    # Render gives 'postgres://' but SQLAlchemy needs 'postgresql://'
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
