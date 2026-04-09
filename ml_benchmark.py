import ollama
import json
import re
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    mean_squared_error,
    r2_score
)

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVR

from plot_results import plot_accuracy, plot_confusion_matrix


# ---------- HELPERS ----------
def extract_option(text):
    text = text.strip().upper()
    match = re.search(r'[ABCD]', text)
    return match.group() if match else ""


def encode_label(label):
    return {"A": 0, "B": 1, "C": 2, "D": 3}.get(label, -1)


# ---------- LLM ----------
def llm_evaluation(data):

    y_true = []
    y_pred = []

    print("\n===== LLM EVALUATION =====\n")

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

    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)

    cm = confusion_matrix(y_true, y_pred)

    print("\n--- LLM Metrics ---")
    print(f"Accuracy : {acc:.2f}")
    print(f"Precision: {prec:.2f}")
    print(f"Recall   : {rec:.2f}")
    print(f"F1 Score : {f1:.2f}")

    return np.array(y_true), acc, cm


# ---------- CLASSIFICATION ----------
def classification_models(X, y):

    results = {}

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "LogReg": LogisticRegression(max_iter=200),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier()
    }

    print("\n===== CLASSIFICATION MODELS =====\n")

    for name, model in models.items():

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)

        print(f"{name} Accuracy: {acc:.2f}")
        results[name] = acc

    return results


# ---------- REGRESSION ----------
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


# ---------- MAIN ----------
def main():

    with open("test_data.json", "r") as f:
        data = json.load(f)

    y, llm_acc, cm = llm_evaluation(data)

    X = np.arange(len(y)).reshape(-1, 1)

    results = classification_models(X, y)

    regression_models(X, y)

    # GRAPH POPUPS
    plot_accuracy(
        llm_acc,
        results["LogReg"],
        results["Decision Tree"],
        results["Random Forest"]
    )

    plot_confusion_matrix(cm)


if __name__ == "__main__":
    main()