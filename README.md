# FootVision

A football prediction app I built for the World Cup 2026. Basically, me and my friends predict match results (score, outcome, first goalscorer) and compete on a leaderboard.

Live at: https://FootVision.pythonanywhere.com

## Why I built this

I wanted a project that combined a web app with something ML-related, and a prediction game felt like a fun way to do both. Also wanted an excuse to actually finish a full project end to end (auth, database, frontend, deployed) instead of leaving it half done.

## What it does

- Sign up with a username + PIN (plus a security question for password recovery)
- See all World Cup 2026 matches from Round of 32 to the Final
- Before you predict, a logistic regression model shows a rough Win/Draw/Loss % based on team Elo ratings
- Predict the score, outcome, and first goalscorer for each match
- Predictions lock automatically once the match kicks off
- Leaderboard updates live with points, streaks, and accuracy

## How scoring works

| Prediction | Points |
|---|---|
| Correct outcome (win/draw/loss) | 20 |
| Correct goal difference | 30 |
| Correct first goalscorer | 35 |
| Exact score | 70 |

## Project structure

app.py # creates the Flask app, registers routes
extensions.py # database setup
models.py # User, Match, Prediction, UserScore tables
seed_data.py # loads the initial match list
update_result.py # scores predictions once a match finishes

routes/
auth.py # login, register, forgot password
prediction.py # dashboard + making predictions
leaderboard.py # leaderboard page

ml_model/
train.py # trains the logistic regression model
model.py # loads the model and returns predictions
dataset1.csv, dataset2.csv # match data from Kaggle used for training

templates/ # HTML pages
static/ # CSS, JS, team logos


## How the prediction model works

1. Look up each team's Elo rating
2. Take the difference between the two
3. Turn that into a feature vector and scale it
4. Feed it into the trained logistic regression model
5. Get back probabilities for home win / draw / away win
6. Clean up the numbers so they don't show anything unrealistically low, and make sure they add up to 100%

It's a simple model — not meant to be a serious predictor, more of a fun feature to see before you lock in your own guess.

## Running it locally

git clone https://github.com/akshaytp8/FootVision.git
cd FootVision
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

create a .env file (see .env.example) and set SECRET_KEY

python3 -c "from app import create_app; from extensions import db; app = create_app(); app.app_context().push(); db.create_all()"
flask run


## What I'd improve if I kept working on this

- Add a well secured Admin panel for easy use.
- The ML model is pretty basic - Elo + logistic regression. A more interesting version would pull in recent form, home advantage, or player-level data instead of just team ratings.
- No automated tests yet. Would want to at least cover the scoring logic since that's the core of the whole app.
- The "instant re-seed on every app restart" behaviour in app.py is a leftover from early development — should be a one-time setup step instead.
- Would like to add password reset via email instead of the security-question approach.

## Tech used

- Backend: Python, Flask
- Database: SQLite + SQLAlchemy
- Frontend: Jinja2 templates, plain CSS/JS
- Hosting: PythonAnywhere
- Model: scikit-learn logistic regression

---
Built by Akshay T P.
