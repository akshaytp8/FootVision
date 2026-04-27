"""
update_result.py
----------------
Run this after a match ends to enter the result and award points.

STEPS:
  1. Edit the 4 variables below
  2. Save the file
  3. Run:  python update_result.py
  4. Type "yes" to confirm

MATCH IDs:
  1 → Arsenal vs Atletico Madrid    (6 May 2026)
  2 → Bayern Munich vs PSG          (7 May 2026)
  3 → FC Barcelona vs Real Madrid   (11 May 2026)
  4 → UCL Final                     (30 May 2026)
"""

# ── EDIT THESE 4 LINES ───────────────────────────────────────────

MATCH_ID      = 1
HOME_SCORE    = 2
AWAY_SCORE    = 1
ACTUAL_SCORER = "Bukayo Saka"   # must match exactly as shown in dropdown

# ─────────────────────────────────────────────────────────────────

from app import create_app
from extensions import db
from models import Match, Prediction, UserScore
from datetime import datetime


def run():
    app = create_app()

    with app.app_context():
        match = Match.query.get(MATCH_ID)

        if not match:
            print(f"❌  No match found with ID {MATCH_ID}")
            return

        if match.status == "completed":
            print(f"⚠️   Match already marked completed. No changes made.")
            return

        print(f"\n  Match  : {match.home_team} vs {match.away_team}")
        print(f"  Result : {HOME_SCORE} – {AWAY_SCORE}")
        print(f"  Scorer : {ACTUAL_SCORER or 'None'}")

        confirm = input("\nSave and award points? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            return

        # Save result
        match.home_score   = HOME_SCORE
        match.away_score   = AWAY_SCORE
        match.actual_scorer = ACTUAL_SCORER
        match.status       = "completed"

        # Work out actual outcome
        if HOME_SCORE > AWAY_SCORE:
            actual_outcome = "home_win"
        elif HOME_SCORE < AWAY_SCORE:
            actual_outcome = "away_win"
        else:
            actual_outcome = "draw"

        # ── SCORING RULES ─────────────────────────────────────────
        # +10  exact score
        # +3   correct outcome only (not if already got +10)
        # +5   correct goal scorer
        # +6   bonus when BOTH exact score AND scorer are correct
        # ──────────────────────────────────────────────────────────

        predictions = Prediction.query.filter_by(
            match_id=MATCH_ID, is_scored=False
        ).all()

        for pred in predictions:
            pts = 0

            exact   = (pred.predicted_home_score == HOME_SCORE and
                       pred.predicted_away_score == AWAY_SCORE)
            outcome = (pred.predicted_outcome == actual_outcome)
            scorer  = (ACTUAL_SCORER and pred.predicted_scorer and
                       pred.predicted_scorer.strip().lower() ==
                       ACTUAL_SCORER.strip().lower())

            if exact:
                pts += 100
            elif outcome:
                pts += 30

            if scorer:
                pts += 50

            if exact and scorer:
                pts += 30   # everything correct bonus

            pred.points_earned = pts
            pred.is_scored     = True

            # Update leaderboard row
            us = UserScore.query.filter_by(user_id=pred.user_id).first()
            if not us:
                us = UserScore(user_id=pred.user_id)
                db.session.add(us)

            us.total_points     += pts
            us.exact_scores     += 1 if exact else 0
            us.correct_outcomes += 1 if (outcome and not exact) else 0
            us.correct_scorers  += 1 if scorer else 0
            us.updated_at        = datetime.utcnow()

        db.session.commit()
        print(f"\n✅  Done! Points awarded to {len(predictions)} user(s).")

        # Show top 5
        top = UserScore.query.order_by(UserScore.total_points.desc()).limit(5).all()
        print("\n🏆  Current Top 5:")
        for i, row in enumerate(top, 1):
            print(f"    {i}. {row.user.username:20s} {row.total_points} pts")


if __name__ == "__main__":
    run()
