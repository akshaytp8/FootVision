"""
routes/prediction.py
--------------------
Dashboard and prediction form.

AUTO-LOCK LOGIC (VIVA explanation):
  Every time a user opens the predict page, the server checks:
    current IST time  >=  match kickoff time?
  If YES → predictions are locked automatically.
  No cron jobs or schedulers needed — it just checks the clock.

Routes:
  GET       /dashboard          → list all matches
  GET/POST  /predict/<match_id> → submit prediction
"""

from flask import (Blueprint, render_template, request,
                   redirect, url_for, flash, session)
from extensions import db
from models import Match, Prediction, UserScore
from ml_model.model import predict_outcome
from datetime import datetime, timezone, timedelta
from functools import wraps

prediction_bp = Blueprint("prediction", __name__)

# Indian Standard Time = UTC + 5:30
IST = timezone(timedelta(hours=5, minutes=30))


# ── Helpers ───────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def is_locked(match):
    """Return True if kickoff time has passed or match is completed."""
    if match.status == "completed":
        return True
    try:
        time_str = match.match_time_ist.replace("IST", "").strip()
        kickoff  = datetime.strptime(
            f"{match.match_date} {time_str}", "%Y-%m-%d %H:%M"
        ).replace(tzinfo=IST)
        return datetime.now(tz=IST) >= kickoff
    except Exception:
        return False


def countdown(match):
    """Return e.g. '2d 3h left' until kickoff, or '' if locked."""
    try:
        time_str = match.match_time_ist.replace("IST", "").strip()
        kickoff  = datetime.strptime(
            f"{match.match_date} {time_str}", "%Y-%m-%d %H:%M"
        ).replace(tzinfo=IST)
        diff = kickoff - datetime.now(tz=IST)
        if diff.total_seconds() <= 0:
            return ""
        d = diff.days
        h = diff.seconds // 3600
        m = (diff.seconds % 3600) // 60
        if d > 0:   return f"{d}d {h}h left"
        if h > 0:   return f"{h}h {m}m left"
        return f"{m}m left"
    except Exception:
        return ""


# ── Routes ────────────────────────────────────────────────────────

@prediction_bp.route("/dashboard")
@login_required
def dashboard():
    matches    = Match.query.order_by(Match.match_date).all()
    user_preds = {p.match_id: p for p in
                  Prediction.query.filter_by(user_id=session["user_id"]).all()}
    score_row  = UserScore.query.filter_by(user_id=session["user_id"]).first()
    total_pts  = score_row.total_points if score_row else 0

    lock_status = {m.id: is_locked(m)  for m in matches}
    countdowns  = {m.id: countdown(m)  for m in matches}

    return render_template("dashboard.html",
                           matches=matches,
                           user_preds=user_preds,
                           total_pts=total_pts,
                           lock_status=lock_status,
                           countdowns=countdowns)


@prediction_bp.route("/predict/<int:match_id>", methods=["GET", "POST"])
@login_required
def predict(match_id):
    match = Match.query.get_or_404(match_id)

    if is_locked(match):
        flash("Predictions are locked — match has already started or ended.", "warning")
        return redirect(url_for("prediction.dashboard"))

    existing    = Prediction.query.filter_by(
                    user_id=session["user_id"], match_id=match_id).first()
    win_pct, draw_pct, loss_pct = predict_outcome(match.home_team, match.away_team)
    scorer_list = match.get_scorer_list()
    cd          = countdown(match)

    if request.method == "POST":
        # Re-check lock in case form was submitted exactly at kickoff
        if is_locked(match):
            flash("Predictions just closed — match has started!", "warning")
            return redirect(url_for("prediction.dashboard"))

        try:
            home_score = int(request.form.get("home_score", 0))
            away_score = int(request.form.get("away_score", 0))
        except ValueError:
            flash("Score must be a whole number.", "danger")
            return render_template("prediction.html", match=match,
                                   win_pct=win_pct, draw_pct=draw_pct,
                                   loss_pct=loss_pct, scorer_list=scorer_list,
                                   existing=existing, countdown=cd)

        outcome = request.form.get("outcome", "")
        scorer  = request.form.get("scorer", "")

        if home_score < 0 or away_score < 0:
            flash("Scores cannot be negative.", "danger")
            return render_template("prediction.html", match=match,
                                   win_pct=win_pct, draw_pct=draw_pct,
                                   loss_pct=loss_pct, scorer_list=scorer_list,
                                   existing=existing, countdown=cd)

        if outcome not in ("home_win", "draw", "away_win"):
            flash("Please select a match outcome.", "danger")
            return render_template("prediction.html", match=match,
                                   win_pct=win_pct, draw_pct=draw_pct,
                                   loss_pct=loss_pct, scorer_list=scorer_list,
                                   existing=existing, countdown=cd)

        if existing:
            existing.predicted_home_score = home_score
            existing.predicted_away_score = away_score
            existing.predicted_outcome    = outcome
            existing.predicted_scorer     = scorer
            db.session.commit()
            flash("Prediction updated! 🔄", "success")
        else:
            db.session.add(Prediction(
                user_id              = session["user_id"],
                match_id             = match_id,
                predicted_home_score = home_score,
                predicted_away_score = away_score,
                predicted_outcome    = outcome,
                predicted_scorer     = scorer,
            ))
            db.session.commit()
            flash("Prediction submitted! Good luck! ⚽", "success")

        return redirect(url_for("prediction.dashboard"))

    return render_template("prediction.html", match=match,
                           win_pct=win_pct, draw_pct=draw_pct,
                           loss_pct=loss_pct, scorer_list=scorer_list,
                           existing=existing, countdown=cd)
