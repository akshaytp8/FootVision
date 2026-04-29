"""
ml_model/train.py
-----------------
Educational example showing how scikit-learn Logistic Regression
would be trained on football data.

This file is for VIVA demonstration only.
The live app uses the simpler model.py instead.

Run:  python ml_model/train.py
"""

import numpy as np
from sklearn.linear_model    import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics         import accuracy_score, classification_report
from sklearn.preprocessing   import StandardScaler

np.random.seed(42)


def generate_data(n=600):
    X, y = [], []
    for _ in range(n):
        hs = np.random.uniform(5, 10)   # home strength
        as_ = np.random.uniform(5, 10)  # away strength
        ha = 1.0                         # home advantage (always 1)
        hf = np.random.uniform(0, 10)   # home recent form
        af = np.random.uniform(0, 10)   # away recent form

        score = (hs + ha + hf * 0.3) - (as_ + af * 0.3) + np.random.normal(0, 1.5)

        if score > 1.5:   label = 0   # Home Win
        elif score > -1.5: label = 1  # Draw
        else:              label = 2  # Away Win

        X.append([hs, as_, ha, hf, af])
        y.append(label)

    return np.array(X), np.array(y)

def train():
    X, y = generate_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    scaler  = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

    model = LogisticRegression(multi_class="multinomial", max_iter=500)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Accuracy: {acc*100:.1f}%")
    print(classification_report(y_test, model.predict(X_test),
          target_names=["Home Win", "Draw", "Away Win"]))


if __name__ == "__main__":
    train()
