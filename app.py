"""
app.py
------
Creates and starts the Flask app.

Run with:  python app.py

NOTE: When going official in May, delete testing_match.py
      and remove the testing_match import line below.
"""

from flask import Flask
from config import Config
from extensions import db, bcrypt
from seed_data import seed_matches

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)

    from routes.auth        import auth_bp
    from routes.prediction  import prediction_bp
    from routes.leaderboard import leaderboard_bp

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
