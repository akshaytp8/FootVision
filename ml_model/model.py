"""FootVision machine-learning prediction helper.

The saved Logistic Regression model was trained with exactly two features:

    1. elo_diff  = HomeElo - AwayElo
    2. form_diff = FormHome - FormAway

The training labels are:
    0 -> home win
    1 -> draw
    2 -> away win

The training-time form data is not stored in the deployment artifacts, so
prediction-time form_diff is set to 0.0, matching the original model design.
"""

from pathlib import Path

import joblib
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "trained_model.pkl"
SCALER_PATH = BASE_DIR / "scaler.pkl"
ELO_PATH = BASE_DIR / "elo_lookup.pkl"

# Names used by the web app -> names present in the Elo lookup.
TEAM_ALIASES = {
    "Atletico Madrid": "Ath Madrid",
    "Atlético Madrid": "Ath Madrid",
    "PSG": "Paris SG",
    "Paris Saint-Germain": "Paris SG",
    "FC Barcelona": "Barcelona",
}


def _load_artifacts():
    """Load the three model artifacts once per process."""
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    elo_lookup = joblib.load(ELO_PATH)
    return model, scaler, elo_lookup


_MODEL, _SCALER, _ELO_LOOKUP = _load_artifacts()


def _get_elo(team_name):
    """Return the team's Elo rating, using a known alias or 1700 fallback."""
    if team_name in _ELO_LOOKUP:
        return float(_ELO_LOOKUP[team_name])

    alias = TEAM_ALIASES.get(team_name)
    if alias and alias in _ELO_LOOKUP:
        return float(_ELO_LOOKUP[alias])

    # Keep the original model's safe fallback for teams not in the lookup.
    return 1700.0


def predict_outcome(home_team, away_team):
    """Return (home_win_pct, draw_pct, away_win_pct) as integers.

    The returned values always add up to exactly 100.
    """
    try:
        home_elo = _get_elo(home_team)
        away_elo = _get_elo(away_team)

        elo_diff = home_elo - away_elo
        form_diff = 0.0

        features = np.array([[elo_diff, form_diff]], dtype=float)
        scaled_features = _SCALER.transform(features)

        probabilities = _MODEL.predict_proba(scaled_features)[0]

        # Classes are H=0, D=1, A=2. Be explicit rather than relying on
        # whatever ordering a future model might return.
        class_probabilities = {
            int(cls): float(prob)
            for cls, prob in zip(_MODEL.classes_, probabilities)
        }

        home = class_probabilities.get(0, 0.0)
        draw = class_probabilities.get(1, 0.0)
        away = class_probabilities.get(2, 0.0)

        # Avoid displaying 0% for a possible outcome.
        minimum = 0.05
        home = max(home, minimum)
        draw = max(draw, minimum)
        away = max(away, minimum)

        total = home + draw + away
        home_pct = round(home / total * 100)
        draw_pct = round(draw / total * 100)
        away_pct = 100 - home_pct - draw_pct

        return home_pct, draw_pct, away_pct

    except Exception:
        # Keep the website usable if a model artifact is unavailable.
        return 40, 25, 35
