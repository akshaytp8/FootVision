# FootVision

FootVision is a simple football match prediction web app built as my MCA final-year project.

The idea is straightforward: users can register, predict the result of selected football matches, and earn points based on how accurate their predictions are. The project also includes a small machine learning model that gives an estimated outcome for each match.

## Features

- User registration and login (with forgot password feature)
- Football match predictions
- Match score and first goal scorer predictions
- Machine learning based match outcome prediction
- Leaderboard with user scores
- Admin tools for adding, removing and updating matches
- SQLite database
- Responsive web interface

## How the scoring works

Points are awarded based on the prediction:

- Correct score: 70 points
- Correct goal difference: 30 points
- Correct match outcome: 20 points
- Correct first goal scorer: 35 points

Only the highest result from score, goal difference and
outcome is counted.

## Machine Learning

The ML part uses Logistic Regression to predict the match outcome.

The model uses features such as:

-   Home team's Elo rating
-   Away team's Elo rating
-   Difference between the two Elo ratings
-   Current form difference

The trained model and supporting files are stored in the `ml_model`
folder and loaded using `joblib`.

## Tech Stack

- Python
- Flask
- SQLite
- HTML / CSS / JavaScript
- scikit-learn
- Pandas
- Joblib

## Project Structure

Some of the main files and folders in the project are:

- `app.py` – main Flask application
- `models.py` – database models
- `config.py` – application configuration
- `routes/` – login, prediction and leaderboard routes
- `templates/` – HTML pages
- `static/` – CSS and JavaScript files
- `ml_model/` – trained machine learning model and prediction code
- `FootVision_ML_Model.ipynb` - ML model code
- `instance/` – SQLite database
- `update_result.py` – used to update match results and scores
- `seed_data.py` – adds the initial match data
- `wsgi.py` – PythonAnywhere configuration

## Running Locally

Clone the repository and open the project folder:

``` bash
git clone <your-repository-url>
cd FootVision
```

Create a virtual environment:

``` bash
python -m venv venv
```

Activate it on Windows:

``` bash
venv\Scripts\activate
```

Install the required packages:

``` bash
pip install -r requirements.txt
```

Start the Flask application:

``` bash
python app.py
```

Then open the local address shown in the terminal.

## Deployment

FootVision is designed to run on "PythonAnywhere" using Flask and SQLite.

Deleted FootVision_ML_Model.ipynb before deployment.

The project includes `wsgi.py` for the PythonAnywhere WSGI configuration. SQLite is used as the database, so no separate database server is required.

