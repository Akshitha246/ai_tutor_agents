import ollama
import json
import re
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_squared_error,
    r2_score
)

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVR

# ---------------- HELPER ----------------
def extract_option(text):
    text = text.strip().upper()
    match = re.search(r'[ABCD]', text)
    return match.group() if match else ""

def encode_label(label):
    return {"A": 0, "B": 1, "C": 2, "D": 3}.get(label, -1)

# ---------------- LLM EVALUATION ----------------
def llm_evaluation(data):

    y_true = []
    y_pred = []

    print("\n===== LLM (LLAMA3) EVALUATION =====\n")

    for i, item in enumerate(data, start=1):

        prompt = f"""
Answer the MCQ.

{item['question']}

Options:
{chr(10).join(item['options'])}

Reply ONLY A/B/C/D
"""

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        pred = extract_option(response["message"]["content"])
        actual = item["answer"]

        y_true.append(encode_label(actual))
        y_pred.append(encode_label(pred))

        print(f"Q{i}: Pred={pred} | Actual={actual}")

    print("\n--- LLM Metrics ---")
    print("Accuracy :", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred, average='weighted', zero_division=0))
    print("Recall   :", recall_score(y_true, y_pred, average='weighted', zero_division=0))
    print("F1 Score :", f1_score(y_true, y_pred, average='weighted', zero_division=0))

    return np.array(y_true)


# ---------------- ML CLASSIFICATION ----------------
def classification_models(X, y):

    print("\n===== CLASSIFICATION MODELS =====\n")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=200),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier()
    }

    for name, model in models.items():

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        print(f"{name} Accuracy:", accuracy_score(y_test, preds))


# ---------------- REGRESSION ----------------
def regression_models(X, y):

    print("\n===== REGRESSION MODELS =====\n")

    y = y.astype(float)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(),
        "SVR": SVR()
    }

    for name, model in models.items():

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        print(f"{name}")
        print(f"  MSE: {mse:.2f}")
        print(f"  R2 : {r2:.2f}")


# ---------------- CROSS VALIDATION ----------------
def cross_validation_models(X, y):

    print("\n===== CROSS VALIDATION =====\n")

    model1 = LogisticRegression(max_iter=200)
    model2 = RandomForestClassifier()

    scores1 = cross_val_score(model1, X, y, cv=5)
    scores2 = cross_val_score(model2, X, y, cv=5)

    print("Logistic Regression CV Mean:", scores1.mean())
    print("Random Forest CV Mean     :", scores2.mean())


# ---------------- MAIN ----------------
def main():

    with open("test_data.json", "r") as f:
        data = json.load(f)

    # Step 1: LLM Evaluation
    y = llm_evaluation(data)

    # Step 2: Create dummy features (since MCQ has no features)
    X = np.arange(len(y)).reshape(-1, 1)

    # Step 3: Classification
    classification_models(X, y)

    # Step 4: Regression
    regression_models(X, y)

    # Step 5: Cross-validation
    cross_validation_models(X, y)


if __name__ == "__main__":
    main()