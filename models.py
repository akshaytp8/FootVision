"""
models.py
---------
Database table definitions.

Tables:
  User       — registered users
  Match      — the 4 competition matches
  Prediction — each user's prediction per match
  UserScore  — total points per user (used for leaderboard)
"""

from datetime import datetime
from extensions import db, bcrypt


class User(db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    dob           = db.Column(db.Date, nullable=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    predictions  = db.relationship("Prediction", backref="user", lazy=True)
    score_record = db.relationship("UserScore",  backref="user", uselist=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Match(db.Model):
    __tablename__ = "matches"

    id             = db.Column(db.Integer, primary_key=True)
    home_team      = db.Column(db.String(100), nullable=False)
    away_team      = db.Column(db.String(100), nullable=False)
    competition    = db.Column(db.String(100), nullable=False)
    match_date     = db.Column(db.String(20),  nullable=False)  # "YYYY-MM-DD"
    match_time_ist = db.Column(db.String(20),  nullable=False)  # "00:30 IST"
    venue          = db.Column(db.String(200), nullable=True)
    home_logo_url  = db.Column(db.String(400), nullable=True)   # e.g. "logos/arsenal.png"
    away_logo_url  = db.Column(db.String(400), nullable=True)

    # "upcoming" | "completed"
    status         = db.Column(db.String(20), default="upcoming")

    # Filled in after match by running update_result.py
    home_score     = db.Column(db.Integer, nullable=True)
    away_score     = db.Column(db.Integer, nullable=True)
    actual_scorer  = db.Column(db.String(100), nullable=True)

    # Comma-separated player names for the goal scorer dropdown
    scorer_options = db.Column(db.Text, nullable=True)

    predictions    = db.relationship("Prediction", backref="match", lazy=True)

    def get_scorer_list(self):
        """Return scorer options as a Python list."""
        if self.scorer_options:
            return [s.strip() for s in self.scorer_options.split(",")]
        return []


class Prediction(db.Model):
    __tablename__ = "predictions"

    id                   = db.Column(db.Integer, primary_key=True)
    user_id              = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    match_id             = db.Column(db.Integer, db.ForeignKey("matches.id"), nullable=False)
    predicted_home_score = db.Column(db.Integer, nullable=False)
    predicted_away_score = db.Column(db.Integer, nullable=False)
    predicted_outcome    = db.Column(db.String(20), nullable=False)  # home_win / draw / away_win
    predicted_scorer     = db.Column(db.String(100), nullable=True)
    points_earned        = db.Column(db.Integer, default=0)
    is_scored            = db.Column(db.Boolean, default=False)
    created_at           = db.Column(db.DateTime, default=datetime.utcnow)

    # One prediction per user per match
    __table_args__ = (
        db.UniqueConstraint("user_id", "match_id", name="uq_user_match"),
    )


class UserScore(db.Model):
    __tablename__ = "user_scores"

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True)
    total_points     = db.Column(db.Integer, default=0)
    exact_scores     = db.Column(db.Integer, default=0)
    correct_outcomes = db.Column(db.Integer, default=0)
    correct_scorers  = db.Column(db.Integer, default=0)
    updated_at       = db.Column(db.DateTime, default=datetime.utcnow)
