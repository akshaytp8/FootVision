"""
ml_model/model.py
-----------------
Loads the pre-trained model and predicts match outcome.
Called by routes/prediction.py for every prediction page.
"""

import os
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))

def predict_outcome(home_team, away_team):
    """
    Returns (win_pct, draw_pct, loss_pct) — integers summing to 100.
    Uses pre-trained Logistic Regression model.
    Falls back to simple defaults if model not trained yet.
    """
    try:
        import joblib

        model      = joblib.load(os.path.join(BASE, "trained_model.pkl"))
        scaler     = joblib.load(os.path.join(BASE, "scaler.pkl"))
        elo_lookup = joblib.load(os.path.join(BASE, "elo_lookup.pkl"))

        h_elo = float(elo_lookup.get(home_team, 1700))
        a_elo = float(elo_lookup.get(away_team, 1700))

        X     = np.array([[h_elo - a_elo, 0.0]])
        probs = model.predict_proba(scaler.transform(X))[0]

        # Clamp each to min 5%, then re-normalise
        probs = np.maximum(probs, 0.05)
        probs = probs / probs.sum()

        w = round(probs[0] * 100)
        d = round(probs[1] * 100)
        l = 100 - w - d   # remainder goes to loss

        return int(w), int(d), int(l)

    except Exception:
        return 40, 25, 35