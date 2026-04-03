import ollama

def give_feedback(topic, evaluation):
    """
    Generates structured feedback based on evaluation result.
    Expects evaluation as a dictionary.
    """

    # Safety check
    if not isinstance(evaluation, dict):
        return "Invalid evaluation format."

    result = evaluation.get("result", "Unknown")
    confidence = evaluation.get("confidence", "Low")
    explanation = evaluation.get("explanation", "")

    prompt = f"""
You are an AI learning coach.

Topic: {topic}

Evaluation Result: {result}
Confidence: {confidence}
Explanation: {explanation}

Provide structured feedback in this format:

1. What the student did well
2. What needs improvement
3. Study advice (2-3 actionable tips)

Keep it clear and concise.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    if not content:
        return "Unable to generate feedback."

    return content.strip()