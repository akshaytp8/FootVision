"""
Adds new match(es) to the live database. NEVER deletes anything —
1. Edit the NEW_MATCHES list below — paste in the Match(...) entries
   for the round that's just been confirmed (real team names, dates,
   logos, scorer lists).
2. Run:  python add_match.py
3. It shows what's currently in the database, what it's about to add,
   automatically skips anything that looks like a duplicate, and asks
   you to confirm before touching anything.
4. Reload your web app from the PythonAnywhere Web tab.
"""

from app import create_app
from extensions import db
from models import Match


# EDIT THIS LIST EACH TIME A NEW ROUND IS CONFIRMED 
NEW_MATCHES = [
    Match(
        home_team      = "TEAM A",            
        away_team      = "TEAM B",             
        competition    = "THIRD PRICE – Match 31",
        match_date     = "2026-07-04",
        match_time_ist = "22:30 IST",
        venue          = "Stadium Name, Country",
        home_logo_url  = "logos/teama.jpeg",
        away_logo_url  = "logos/teamb.jpeg",
        status         = "upcoming",
        scorer_options = "No Goal, ...",          
    ),
    # Add as many Match(...) 
]
# END ------------------------------------------------------


def run():
    app = create_app()

    with app.app_context():
        existing = Match.query.order_by(Match.match_date).all()

        print(f"\nCurrently {len(existing)} match(es) in the database:")
        for m in existing:
            print(f"  [{m.id}] {m.home_team} vs {m.away_team}  "
                  f"({m.match_date})  — {m.competition}")

        existing_keys = {(m.home_team, m.away_team, m.match_date) for m in existing}

        to_add = []
        for m in NEW_MATCHES:
            key = (m.home_team, m.away_team, m.match_date)
            if key in existing_keys:
                print(f"\n⚠️  Skipping duplicate: {m.home_team} vs {m.away_team} "
                      f"on {m.match_date} (already in database)")
                continue
            to_add.append(m)

        if not to_add:
            print("\nNothing new to add.")
            return

        print(f"\nAbout to ADD {len(to_add)} new match(es):")
        for m in to_add:
            print(f"  {m.home_team} vs {m.away_team}  ({m.match_date})  — {m.competition}")

        confirm = input(
            "\nProceed? Nothing existing will be touched. (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Cancelled.")
            return

        db.session.add_all(to_add)
        db.session.commit()

        print(f"\n✅  Added {len(to_add)} match(es). "
              "Existing matches, predictions, and points are untouched.")


if __name__ == "__main__":
    run()
