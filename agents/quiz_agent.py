import ollama

def generate_quiz(topic):

    if not topic or topic.strip() == "":
        return "Please enter a valid topic."

    prompt = f"""
You are a quiz generator.

Create EXACTLY 10 multiple choice questions about the topic below.

Topic: {topic}

STRICT RULES:
- Must generate exactly 10 questions
- Each question must have 4 options: A, B, C, D
- Clearly mention correct answer
- No extra explanation
- Follow format EXACTLY

FORMAT:

Question 1:
<question text>
A) option
B) option
C) option
D) option
Correct Answer: <A/B/C/D>

Question 2:
...
Continue until Question 10.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    # Safety fallback
    if not content or "Question" not in content:
        return "Failed to generate quiz. Try again."

    return content.strip()