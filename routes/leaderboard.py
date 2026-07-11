"""
routes/leaderboard.py
---------------------
Shows all users ranked by total points.

Route:  GET /leaderboard
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash
from models import UserScore, User

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("/leaderboard")
def leaderboard():
    if "user_id" not in session:
        flash("Please log in to view the leaderboard.", "warning")
        return redirect(url_for("auth.login"))

    rankings = (UserScore.query
                .join(User, UserScore.user_id == User.id)
                .order_by(UserScore.total_points.desc())
                .all())

    # Find the logged-in user's position
    current_rank = None
    for i, row in enumerate(rankings):
        if row.user_id == session["user_id"]:
            current_rank = i + 1
            break

    return render_template("leaderboard.html",
                           rankings=rankings,
                           current_rank=current_rank)
