"""
config.py
---------
App settings. That's it.
"""

class Config:
    SECRET_KEY = "losblancos-secret-key-2026"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
