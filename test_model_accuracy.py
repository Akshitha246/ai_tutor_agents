import ollama
import json
import re

def extract_option(text):
    """
    Extract A/B/C/D from model response safely
    """
    text = text.strip().upper()

    match = re.search(r'[ABCD]', text)
    return match.group() if match else ""

def evaluate_model():

    # Load dataset
    with open("test_data.json", "r") as f:
        data = json.load(f)

    correct = 0
    total = len(data)

    print("\n===== MODEL EVALUATION STARTED =====\n")

    for i, item in enumerate(data, start=1):

        prompt = f"""
Answer the following multiple choice question.

Question:
{item['question']}

Options:
{chr(10).join(item['options'])}

IMPORTANT:
- Reply ONLY with A, B, C, or D
- Do NOT explain
"""

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response["message"]["content"]
        predicted = extract_option(raw_output)
        actual = item["answer"]

        is_correct = predicted == actual

        print(f"Q{i}: {item['question']}")
        print(f"Model Answer: {predicted} | Correct Answer: {actual} | {'✅' if is_correct else '❌'}\n")

        if is_correct:
            correct += 1

    accuracy = (correct / total) * 100

    print("===== FINAL RESULTS =====")
    print(f"Total Questions: {total}")
    print(f"Correct Answers: {correct}")
    print(f"Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    evaluate_model()