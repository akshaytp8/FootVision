# Trains a simple ML model using dataset1.csv and dataset2.csv.


import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

BASE    = os.path.dirname(os.path.abspath(__file__))
ROOT    = os.path.join(BASE, "..")
DATA1   = os.path.join(BASE, "dataset1.csv")
DATA2   = os.path.join(BASE, "dataset2.csv")
MODEL   = os.path.join(BASE, "trained_model.pkl")
SCALER  = os.path.join(BASE, "scaler.pkl")

print("Training ML model...")

# --- Load dataset1 (match results) ---
df = pd.read_csv(DATA1, low_memory=False)

# Use whichever form column exists
form_h = "Form5Home" if "Form5Home" in df.columns else "Form3Home"
form_a = "Form5Away" if "Form5Away" in df.columns else "Form3Away"

df = df[["HomeElo", "AwayElo", form_h, form_a, "FTResult"]].dropna()
df = df[df["FTResult"].isin(["H", "D", "A"])]

# --- Load dataset2 (ELO ratings) ---
elo_df = pd.read_csv(DATA2)
# Get the latest ELO for each club from dataset2
latest_elo = elo_df.sort_values("date").groupby("club")["elo"].last().to_dict()

print(f"Matches loaded   : {len(df)}")
print(f"Teams with ELO   : {len(latest_elo)}")

# --- Features: elo_diff and form_diff ---
df["elo_diff"]  = df["HomeElo"] - df["AwayElo"]
df["form_diff"] = df[form_h]    - df[form_a]

X = df[["elo_diff", "form_diff"]].values
y = df["FTResult"].map({"H": 0, "D": 1, "A": 2}).values

# --- Train ---
scaler  = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(max_iter=200)
model.fit(X_scaled, y)

# --- Save ---
joblib.dump(model,      MODEL)
joblib.dump(scaler,     SCALER)
joblib.dump(latest_elo, os.path.join(BASE, "elo_lookup.pkl"))

from sklearn.metrics import accuracy_score
acc = accuracy_score(y, model.predict(X_scaled))
print(f"Accuracy         : {acc*100:.1f}%")
print("Saved: trained_model.pkl, scaler.pkl, elo_lookup.pkl")
print("Done ✅")
