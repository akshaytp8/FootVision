# ⚽ FootVision — Prediction Game

A football prediction platform built with Flask, where friends compete to predict match results across the entire FIFA World Cup 2026 bracket — from the Round of 32 all the way to the Final.

---

## 🌍 Live Site

> Hosted on [PythonAnywhere](https://www.pythonanywhere.com)  
> `https://FootVision.pythonanywhere.com`

---

## 📸 Features

- 🔐 **Secure accounts** — register with a username, 4-digit PIN, and an optional security question for password recovery
- 📅 **Match schedule** — all World Cup 2026 fixtures from Round of 32 to the Final
- 🤖 **ML outcome predictor** — mathematical model shows predicted Win / Draw / Loss % before you submit
- 🎯 **Predictions** — pick the score, outcome, and first goalscorer for each match
- 🔒 **Auto-lock** — predictions lock automatically at kickoff time
- 🏆 **Live leaderboard** — real-time points table with rank, streak, and accuracy
- 🌙 **Dark FIFA theme** — deep navy / FIFA red colour palette, optimised for mobile

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

## 🧠 ML Model — How It Works

The predictor in `ml_model/model.py` uses a logistic regression model.

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

## 🏅 Scoring System

| Prediction | Points |
|---|---|
| Correct outcome (W/D/L) | +20 |
| Exact score | +70 |
| Correct first goalscorer | +35 |
| Correct goal difference | +30 |

---

## 🗄️ Database Schema

```
users           — id, username, password_hash, security_answer_hash
matches         — id, home_team, away_team, competition, match_date,
                  match_time_ist, venue, home_logo_url, away_logo_url,
                  status, scorer_options, home_score, away_score, first_scorer
predictions     — id, user_id, match_id, home_score, away_score,
                  outcome, first_scorer, points_earned
user_scores     — id, user_id, total_points
```

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

## 🛠️ Admin Scripts

All scripts are interactive — they show you what they'll change and ask for `yes` before touching anything.

### Add new round's matches (after winners are confirmed)
```bash
# Edit NEW_MATCHES list inside the file first, then:
python admin/add_match.py
```

### Remove a match by ID
```bash
python admin/remove_match.py
# Lists all matches with IDs → type the ID(s) to remove
```

### Swap the entire match list (one-time use)
```bash
python admin/migrate_matches.py
```

### Reset all user accounts (keep matches)
```bash
python admin/wipe_users.py
```

### Reset points only (keep accounts)
```python
# Run in a Python shell with app context:
from models import UserScore, Prediction
Prediction.query.delete(synchronize_session=False)
UserScore.query.update({UserScore.total_points: 0})
db.session.commit()
```

### Mark a match as completed and score predictions
```bash
python update_result.py
```

---

## 🌐 Deploying on PythonAnywhere (Free Tier)

1. Upload project files via the **Files tab**
2. Create a virtual environment in the Bash console and `pip install -r requirements.txt`
3. Set up a new **Web app** → Manual configuration → Python 3.x
4. Set the WSGI file to point to your `app.py`
5. Add `SECRET_KEY` as an environment variable in the Web tab
6. Run the database init and seed commands from the Bash console
7. **Reload** the web app

---

## 📋 Tournament Workflow

The World Cup runs in stages. This is the recommended workflow:

| Stage | Action |
|---|---|
| Before tournament | Run `migrate_matches.py` with Round of 32 fixtures |
| After each match | Run `update_result.py` to score predictions |
| After each round | Run `add_match.py` with confirmed next-round fixtures |
| Repeat | Until the Final on 20 July 2026 |

---

## 🔒 Security Notes

- Passwords are stored as hashed values (Werkzeug `generate_password_hash`)
- Security answers are also hashed — never stored in plain text
- Sessions are server-side signed with Flask's secret key
- Predictions lock automatically at kickoff — no manual intervention needed

---

## 🧰 Tech Stack

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
