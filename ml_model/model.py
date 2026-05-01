"""
ml_model/model.py
-----------------
Predicts match outcome probabilities using a mathematical model.

VIVA EXPLANATION:
  Input  → two team names
  Output → Win %, Draw %, Loss % (always sum to 100)

HOW IT WORKS:
  1. Each team has a strength rating (0–10) based on squad quality
  2. Home team gets +0.7 bonus (home advantage)
  3. Net advantage = home strength − away strength
  4. Sigmoid function converts net advantage → win probability
     sigmoid(x) = 1 / (1 + e^-x)
     → always between 0 and 1
     → when x=0 (equal teams) → 0.5 (50%)
  5. Draw probability is highest when teams are closely matched
  6. All three values are normalised to sum to 100%
"""

import math

# Team strength ratings (0–10 scale)
TEAM_STRENGTHS = {
    "Arsenal"           : 8.5,
    "Atletico Madrid"   : 8.3,
    "Bayern Munich"     : 8.9,
    "PSG"               : 9.2,
    "FC Barcelona"      : 8.8,
    "Real Madrid"       : 9.2,
    "UCL Final – Team A": 8.4,
    "UCL Final – Team B": 8.75,
}

HOME_ADVANTAGE = 0.7


def predict_outcome(home_team, away_team):
    """
    Returns (win_pct, draw_pct, loss_pct) as integers summing to 100.
    win_pct  = probability home team wins
    loss_pct = probability away team wins
    """
    home_str = TEAM_STRENGTHS.get(home_team, 7.5)
    away_str = TEAM_STRENGTHS.get(away_team, 7.5)

    net = (home_str + HOME_ADVANTAGE) - away_str

    win_raw  = 1.0 / (1.0 + math.exp(-net * 0.9))
    loss_raw = 1.0 / (1.0 + math.exp( net * 0.9))

    draw_raw = max(0.10, 0.30 - abs(net) * 0.12)

    # Normalise win + loss to fill remaining probability after draw
    remaining = 1.0 - draw_raw
    total_wl  = win_raw + loss_raw
    win_prob  = (win_raw  / total_wl) * remaining
    loss_prob = (loss_raw / total_wl) * remaining

    win_pct  = max(5, round(win_prob  * 100))
    loss_pct = max(5, round(loss_prob * 100))
    draw_pct = 100 - win_pct - loss_pct

    return win_pct, draw_pct, loss_pct
