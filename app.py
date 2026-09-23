"""FootVision Flask application factory.

Run locally with:
    python app.py

PythonAnywhere WSGI entry point:
    wsgi.py
"""

import os

from flask import Flask

from config import Config
from extensions import bcrypt, db
from seed_data import seed_matches


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Make sure the SQLite instance directory exists before SQLAlchemy opens it.
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)

    from routes.auth import auth_bp
    from routes.leaderboard import leaderboard_bp
    from routes.prediction import prediction_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(leaderboard_bp)

    with app.app_context():
        db.create_all()
        seed_matches()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
