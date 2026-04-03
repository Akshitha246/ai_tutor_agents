import ollama
import json
import re

def evaluate_answer(question, user_answer):

    prompt = f"""
You are an expert evaluator.

Question:
{question}

User Answer:
{user_answer}

Evaluate the answer.

Return STRICT JSON ONLY (no extra text):
{{
    "result": "Correct or Incorrect",
    "confidence": "High/Medium/Low",
    "explanation": "Short explanation"
}}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    # -----------------------
    # STEP 1: Extract JSON safely
    # -----------------------
    try:
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())

            # ensure all keys exist
            return {
                "result": parsed.get("result", "Incorrect"),
                "confidence": parsed.get("confidence", "Low"),
                "explanation": parsed.get("explanation", "No explanation provided")
            }

    except:
        pass

    # -----------------------
    # STEP 2: Fallback logic
    # -----------------------
    result = "Correct" if "correct" in content.lower() else "Incorrect"

    return {
        "result": result,
        "confidence": "Low",
        "explanation": content.strip()
    }