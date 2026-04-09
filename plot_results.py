import matplotlib
matplotlib.use('TkAgg')   # 🔥 forces popup window

import matplotlib.pyplot as plt

def plot_accuracy(llm_acc, logreg_acc, dt_acc, rf_acc):

    models = ["Llama3 (LLM)", "LogReg", "Decision Tree", "Random Forest"]
    accuracy = [llm_acc, logreg_acc, dt_acc, rf_acc]

    plt.figure()
    plt.bar(models, accuracy)

    plt.xlabel("Models")
    plt.ylabel("Accuracy")
    plt.title("Model Accuracy Comparison")

    for i, v in enumerate(accuracy):
        plt.text(i, v + 0.01, f"{v:.2f}", ha='center')

    plt.tight_layout()
    plt.show()


def plot_confusion_matrix(cm):

    plt.figure()
    plt.imshow(cm)

    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    for i in range(len(cm)):
        for j in range(len(cm)):
            plt.text(j, i, cm[i][j], ha="center", va="center")

    plt.tight_layout()
    plt.show()