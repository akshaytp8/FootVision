import os


class Config:
    SECRET_KEY = "losblancos-secret-key-2026"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    db_url = os.environ.get("DATABASE_URL") or "sqlite:///database.db"

    SQLALCHEMY_DATABASE_URI = db_url
