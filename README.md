# ⚽ FootVision — Prediction Game

A football prediction platform built with Flask, where friends compete to predict match results across the entire FIFA World Cup 2026 bracket — from the Round of 32 all the way to the Final.

---
> Hosted on [PythonAnywhere](https://www.pythonanywhere.com)  
> `https://FootVision.pythonanywhere.com`

---

## Features

- **Secure accounts** — register with a username, 4-digit PIN, and an optional security question for password recovery
- **Match schedule** — all World Cup 2026 fixtures from Round of 32 to the Final
- **ML outcome predictor** — mathematical model shows predicted Win / Draw / Loss % before you submit
- **Predictions** — pick the score, outcome, and first goalscorer for each match
- **Auto-lock** — predictions lock automatically at kickoff time
- **Live leaderboard** — real-time points table with rank, streak, and accuracy
- **Dark FIFA theme** — deep navy / FIFA red colour palette, optimised for mobile

---

## 🗃️ Project Structure

```
├── app.py                  # App factory, blueprint registration
├── extensions.py           # SQLAlchemy instance
├── models.py               # User, Match, Prediction, UserScore
├── seed_data.py            # Initial match data (Round of 32)
├── update_result.py        # Mark a match completed, score predictions
│
├── routes/
│   ├── auth.py             # Register, login, logout, forgot password
│   ├── prediction.py       # Dashboard, make/edit prediction
│   └── leaderboard.py      # Leaderboard view
│
├── ml_model/
│   ├── dataset1.csv            # football dataset from kaggle
│   ├── dataset2.csv
|   ├── train.py                # trains the logistic regression model
|   └── model.py                # predicts model the output
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── prediction.html
│   ├── leaderboard.html
│   └── forgot_password.html
│
├── static/
│   ├── css/style.css       # Dark WC2026 theme
│   ├── js/main.js
│   └── images/logos/       # Team flag/crest images (.jpeg)
│
├── admin/
│   ├── add_match.py        # Add new round's matches to live DB
│   ├── remove_match.py     # Remove match(es) by ID from live DB
│   ├── migrate_matches.py  # Swap entire match list (one-time use)
│   └── wipe_users.py       # Reset all user accounts (keep matches)
│
└── database.db             # SQLite database (gitignored)
```

---

ML Model

The predictor in `ml_model` uses a logistic regression model.

1. Retrieve the latest Elo ratings for both teams.
2. Compute the Elo difference.
3. Generate the feature vector.
4. Scale the input using the saved scaler.
5. Pass the features to the trained Logistic Regression model.
6. Obtain class probabilities using predict_proba().
7. Convert probabilities into percentage values for:
Home Win
Draw
Away Win
8. Apply a minimum probability threshold to avoid extremely low confidence predictions and normalize the probabilities so they sum to 100%.

---

Scoring System

| Prediction | Points |
|---|---|
| Correct outcome (W/D/L) | +20 |
| Exact score | +70 |
| Correct first goalscorer | +35 |
| Correct goal difference | +30 |

---

## 🚀 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/footvision.git
cd footvision

# 2. Create a virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Set environment variable for Flask secret key
export SECRET_KEY="your-secret-key-here"

# 4. Initialise the database and seed matches
python3 -c "from app import create_app; from extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
python3 -c "from app import create_app; from seed_data import seed_matches; app = create_app(); app.app_context().push(); seed_matches()"

# 5. Run locally
flask run
```

---

## Security 

- Passwords are stored as hashed values (Werkzeug `generate_password_hash`)
- Security answers are also hashed — never stored in plain text
- Sessions are server-side signed with Flask's secret key
- Predictions lock automatically at kickoff — no manual intervention needed

---

## Tech 

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask |
| Database | SQLite + SQLAlchemy ORM |
| Frontend | Jinja2 templates, CSS, JS |
| Hosting | PythonAnywhere (free tier) |
| ML Model | Logistic regression |


---

## 👤 Author

Built for the FIFA World Cup 2026 by **Akshay T P**  
Final year project — Football Prediction Platform with ML-based outcome modelling
