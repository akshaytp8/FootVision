"""
remove_match.py
----------------
Removes match(es) from the live database, by ID. Also deletes any
predictions tied to those matches (required — otherwise they'd point
to a match that no longer exists). NEVER touches `users` or
`user_scores` — nobody's total points change, ever.

HOW TO USE
----------
1. Run:  python remove_match.py
2. It lists every match currently in the database, with its ID and
   how many predictions are linked to it.
3. Type the ID(s) you want to remove, comma-separated (e.g. 17,18) —
   or "cancel" to exit without changing anything.
4. Confirm with "yes".
5. Reload your web app from the PythonAnywhere Web tab.
"""

from app import create_app
from extensions import db
from models import Match, Prediction


def run():
    app = create_app()

    with app.app_context():
        matches = Match.query.order_by(Match.match_date).all()

        if not matches:
            print("No matches in the database.")
            return

        print("\nCurrent matches:")
        for m in matches:
            pred_count = Prediction.query.filter_by(match_id=m.id).count()
            print(f"  [{m.id}] {m.home_team} vs {m.away_team}  "
                  f"({m.match_date})  — {m.competition}  "
                  f"[{pred_count} prediction(s)]")

        raw = input(
            "\nEnter the ID(s) to remove, comma-separated (or 'cancel'): "
        ).strip()

        if raw.lower() == "cancel" or not raw:
            print("Cancelled.")
            return

        try:
            ids_to_remove = [int(x.strip()) for x in raw.split(",")]
        except ValueError:
            print("Invalid input — please enter numbers only, e.g. 17,18")
            return

        targets = [m for m in matches if m.id in ids_to_remove]
        if not targets:
            print("No matching match IDs found in the database.")
            return

        total_preds = sum(
            Prediction.query.filter_by(match_id=m.id).count() for m in targets
        )

        print(f"\nAbout to PERMANENTLY delete:")
        for m in targets:
            pc = Prediction.query.filter_by(match_id=m.id).count()
            print(f"  [{m.id}] {m.home_team} vs {m.away_team}  "
                  f"({m.match_date})  — {pc} linked prediction(s) will go too")

        print(f"\nUser accounts and TOTAL points are NOT affected — only "
              f"these {len(targets)} match row(s) and their {total_preds} "
              f"linked prediction row(s) are removed.")

        confirm = input("\nType 'yes' to confirm: ").strip().lower()
        if confirm != "yes":
            print("Cancelled. No changes made.")
            return

        target_ids = [m.id for m in targets]
        Prediction.query.filter(
            Prediction.match_id.in_(target_ids)
        ).delete(synchronize_session=False)

        Match.query.filter(
            Match.id.in_(target_ids)
        ).delete(synchronize_session=False)

        db.session.commit()

        print(f"\n✅  Removed {len(targets)} match(es) and "
              f"{total_preds} linked prediction(s).")
        print("   User accounts and total points are untouched.")


if __name__ == "__main__":
    run()
