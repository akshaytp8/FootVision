import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-key-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    db_url = os.environ.get("DATABASE_URL") or "sqlite:///database.db"

    SQLALCHEMY_DATABASE_URI = db_url
