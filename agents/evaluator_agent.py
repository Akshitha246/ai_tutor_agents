import ollama

def evaluate_answer(question, answer):

    prompt = f"""
Question:
{question}

User answer:
{answer}

Evaluate if the answer is correct.

Return:

Result: Correct or Incorrect
Explanation:
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]
