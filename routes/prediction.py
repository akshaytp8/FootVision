"""Dashboard and prediction routes for FootVision."""

from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from extensions import db
from ml_model.model import predict_outcome
from models import Match, Prediction, UserScore


prediction_bp = Blueprint("prediction", __name__)

IST = timezone(timedelta(hours=5, minutes=30))
VALID_OUTCOMES = {"home_win", "draw", "away_win"}


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated


def _kickoff(match):
    """Parse the stored IST date/time into an aware datetime."""
    time_str = match.match_time_ist.replace("IST", "").strip()
    return datetime.strptime(
        f"{match.match_date} {time_str}", "%Y-%m-%d %H:%M"
    ).replace(tzinfo=IST)


def is_locked(match):
    """Return True once kickoff has passed or the match is completed."""
    if match.status == "completed":
        return True

    try:
        return datetime.now(tz=IST) >= _kickoff(match)
    except (TypeError, ValueError):
        # A malformed match should not accidentally become permanently locked.
        return False


def countdown(match):
    """Return a short human-readable countdown until kickoff."""
    try:
        diff = _kickoff(match) - datetime.now(tz=IST)
    except (TypeError, ValueError):
        return ""

    if diff.total_seconds() <= 0:
        return ""

    total_seconds = int(diff.total_seconds())
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes = remainder // 60

    if days:
        return f"{days}d {hours}h left"
    if hours:
        return f"{hours}h {minutes}m left"
    return f"{minutes}m left"


def _render_prediction_page(match, existing, win_pct, draw_pct, loss_pct, scorer_list, message=None):
    if message:
        flash(message, "danger")

    return render_template(
        "prediction.html",
        match=match,
        win_pct=win_pct,
        draw_pct=draw_pct,
        loss_pct=loss_pct,
        scorer_list=scorer_list,
        existing=existing,
        countdown=countdown(match),
    )


@prediction_bp.route("/dashboard")
def dashboard():
    matches = Match.query.order_by(Match.match_date, Match.id).all()

    user_preds = {}
    total_pts = 0

    if session.get("user_id"):
        user_preds = {
            p.match_id: p
            for p in Prediction.query.filter_by(user_id=session["user_id"]).all()
        }
        score_row = UserScore.query.filter_by(
            user_id=session["user_id"]
        ).first()
        total_pts = score_row.total_points if score_row else 0

    lock_status = {m.id: is_locked(m) for m in matches}
    countdowns = {m.id: countdown(m) for m in matches}

    return render_template(
        "dashboard.html",
        matches=matches,
        user_preds=user_preds,
        total_pts=total_pts,
        lock_status=lock_status,
        countdowns=countdowns,
    )


@prediction_bp.route("/predict/<int:match_id>", methods=["GET", "POST"])
@login_required
def predict(match_id):
    match = Match.query.get_or_404(match_id)

    if is_locked(match):
        flash(
            "Predictions are locked — match has already started or ended.",
            "warning",
        )
        return redirect(url_for("prediction.dashboard"))

    existing = Prediction.query.filter_by(
        user_id=session["user_id"], match_id=match_id
    ).first()

    win_pct, draw_pct, loss_pct = predict_outcome(
        match.home_team, match.away_team
    )
    scorer_list = match.get_scorer_list()

    if request.method == "POST":
        # Always re-check on the server. JavaScript is only a convenience.
        if is_locked(match):
            flash("Predictions just closed — match has started!", "warning")
            return redirect(url_for("prediction.dashboard"))

        try:
            home_score = int(request.form.get("home_score", ""))
            away_score = int(request.form.get("away_score", ""))
        except (TypeError, ValueError):
            return _render_prediction_page(
                match, existing, win_pct, draw_pct, loss_pct, scorer_list,
                "Score must be a whole number.",
            )

        if not (0 <= home_score <= 20 and 0 <= away_score <= 20):
            return _render_prediction_page(
                match, existing, win_pct, draw_pct, loss_pct, scorer_list,
                "Scores must be between 0 and 20.",
            )

        outcome = request.form.get("outcome", "").strip()
        scorer = request.form.get("scorer", "").strip()

        if outcome not in VALID_OUTCOMES:
            return _render_prediction_page(
                match, existing, win_pct, draw_pct, loss_pct, scorer_list,
                "Please select a match outcome.",
            )

        # Do not trust the browser's radio-button selection.
        expected_outcome = (
            "home_win" if home_score > away_score
            else "away_win" if home_score < away_score
            else "draw"
        )
        if outcome != expected_outcome:
            return _render_prediction_page(
                match, existing, win_pct, draw_pct, loss_pct, scorer_list,
                "The selected outcome must match the predicted score.",
            )

        if scorer and scorer not in scorer_list:
            return _render_prediction_page(
                match, existing, win_pct, draw_pct, loss_pct, scorer_list,
                "Please select a valid goal scorer.",
            )

        try:
            if existing:
                existing.predicted_home_score = home_score
                existing.predicted_away_score = away_score
                existing.predicted_outcome = outcome
                existing.predicted_scorer = scorer or None
                db.session.commit()
                flash("Prediction updated! 🔄", "success")
            else:
                db.session.add(
                    Prediction(
                        user_id=session["user_id"],
                        match_id=match_id,
                        predicted_home_score=home_score,
                        predicted_away_score=away_score,
                        predicted_outcome=outcome,
                        predicted_scorer=scorer or None,
                    )
                )
                db.session.commit()
                flash("Prediction submitted! Good luck! ⚽", "success")
        except Exception:
            db.session.rollback()
            flash("Could not save your prediction. Please try again.", "danger")
            return _render_prediction_page(
                match, existing, win_pct, draw_pct, loss_pct, scorer_list
            )

        return redirect(url_for("prediction.dashboard"))

    return render_template(
        "prediction.html",
        match=match,
        win_pct=win_pct,
        draw_pct=draw_pct,
        loss_pct=loss_pct,
        scorer_list=scorer_list,
        existing=existing,
        countdown=countdown(match),
    )
