"""Enter a completed match result and award FootVision points.

Edit the variables in the configuration section, then run:
    python update_result.py

Scoring:
    70 points - exact score
    30 points - exact goal difference, when the score is not exact
    20 points - correct outcome, when score and goal difference are wrong
    35 points - correct first goal scorer

Exact score + scorer = 105 points maximum.

For penalty shootouts, enter the FT/ET score in HOME_SCORE/AWAY_SCORE and
the shootout score in PENALTY_HOME/PENALTY_AWAY. The shootout determines
the outcome only; it does not change score or goal-difference points.
"""

# ── EDIT THESE VALUES ─────────────────────────────────────────────
MATCH_ID = 1
HOME_SCORE = 1       # Full-time + extra-time score, excluding penalties
AWAY_SCORE = 0
ACTUAL_SCORER = "Bukayo Saka (ARS)"  # Use None if there was no scorer.

# Use None for normal matches. Set manually for a two-leg tie if the
# competition outcome differs from this match's score.
ACTUAL_OUTCOME = None  # "home_win" | "draw" | "away_win" | None

# Leave both as None when there was no penalty shootout.
PENALTY_HOME = None
PENALTY_AWAY = None
# ─────────────────────────────────────────────────────────────────

from datetime import datetime

from app import create_app
from extensions import db
from models import Match, Prediction, UserScore


VALID_OUTCOMES = {"home_win", "draw", "away_win"}


def calculate_outcome():
    """Calculate match outcome, including a penalty shootout when present."""
    if ACTUAL_OUTCOME in VALID_OUTCOMES:
        return ACTUAL_OUTCOME

    if HOME_SCORE > AWAY_SCORE:
        return "home_win"
    if HOME_SCORE < AWAY_SCORE:
        return "away_win"

    if PENALTY_HOME is not None and PENALTY_AWAY is not None:
        if PENALTY_HOME > PENALTY_AWAY:
            return "home_win"
        if PENALTY_HOME < PENALTY_AWAY:
            return "away_win"

    return "draw"


def run():
    if MATCH_ID < 1:
        print("❌ MATCH_ID must be a positive integer.")
        return

    if HOME_SCORE < 0 or AWAY_SCORE < 0:
        print("❌ Match scores cannot be negative.")
        return

    if (PENALTY_HOME is None) != (PENALTY_AWAY is None):
        print("❌ Enter both penalty scores, or leave both as None.")
        return

    if (
        PENALTY_HOME is not None
        and (PENALTY_HOME < 0 or PENALTY_AWAY < 0)
    ):
        print("❌ Penalty scores cannot be negative.")
        return

    if ACTUAL_OUTCOME is not None and ACTUAL_OUTCOME not in VALID_OUTCOMES:
        print("❌ ACTUAL_OUTCOME must be home_win, draw, away_win, or None.")
        return

    app = create_app()

    with app.app_context():
        match = db.session.get(Match, MATCH_ID)

        if not match:
            print(f"❌ No match found with ID {MATCH_ID}.")
            return

        if match.status == "completed":
            print("⚠️ Match is already marked completed. No changes made.")
            return

        actual_outcome = calculate_outcome()

        print(f"\nMatch   : {match.home_team} vs {match.away_team}")
        print(f"Result  : {HOME_SCORE} – {AWAY_SCORE}")
        print(f"Outcome : {actual_outcome}")
        print(f"Scorer  : {ACTUAL_SCORER or 'None'}")
        if PENALTY_HOME is not None:
            print(f"Penalties: {PENALTY_HOME} – {PENALTY_AWAY}")

        confirm = input("\nSave result and award points? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return

        try:
            match.home_score = HOME_SCORE
            match.away_score = AWAY_SCORE
            match.actual_scorer = ACTUAL_SCORER
            match.penalty_home = PENALTY_HOME
            match.penalty_away = PENALTY_AWAY
            match.status = "completed"

            predictions = Prediction.query.filter_by(
                match_id=MATCH_ID, is_scored=False
            ).all()

            for pred in predictions:
                exact = (
                    pred.predicted_home_score == HOME_SCORE
                    and pred.predicted_away_score == AWAY_SCORE
                )

                predicted_goal_diff = (
                    pred.predicted_home_score - pred.predicted_away_score
                )
                actual_goal_diff = HOME_SCORE - AWAY_SCORE
                goal_diff = (
                    predicted_goal_diff == actual_goal_diff
                    and pred.predicted_outcome == actual_outcome
                )

                outcome = pred.predicted_outcome == actual_outcome

                scorer = bool(
                    ACTUAL_SCORER
                    and pred.predicted_scorer
                    and pred.predicted_scorer.strip().casefold()
                    == ACTUAL_SCORER.strip().casefold()
                )

                points = 0
                if exact:
                    points += 70
                elif goal_diff:
                    points += 30
                elif outcome:
                    points += 20

                if scorer:
                    points += 35

                pred.points_earned = points
                pred.is_scored = True

                score_row = UserScore.query.filter_by(
                    user_id=pred.user_id
                ).first()

                if score_row is None:
                    score_row = UserScore(user_id=pred.user_id)
                    db.session.add(score_row)

                score_row.total_points += points
                score_row.exact_scores += int(exact)
                score_row.correct_goal_diff += int(goal_diff and not exact)
                score_row.correct_outcomes += int(
                    outcome and not exact and not goal_diff
                )
                score_row.correct_scorers += int(scorer)
                score_row.updated_at = datetime.utcnow()

            db.session.commit()

        except Exception:
            db.session.rollback()
            print("❌ Database update failed. Nothing was committed.")
            raise

        print(
            f"\n✅ Done! Points awarded to {len(predictions)} "
            "prediction(s)."
        )

        top = (
            UserScore.query
            .order_by(UserScore.total_points.desc(), UserScore.user_id.asc())
            .limit(5)
            .all()
        )

        print("\n🏆 Current Top 5:")
        for index, row in enumerate(top, 1):
            print(
                f"    {index}. {row.user.username:20s} "
                f"{row.total_points} pts"
            )


if __name__ == "__main__":
    run()
