import ollama

def chat_with_tutor(user_question, topic=None, history=None):

    if history is None:
        history = []

    # Safety check
    if not user_question or user_question.strip() == "":
        return "Please enter a valid question.", history

    # Limit history (avoid memory overflow)
    history = history[-5:]

    system_prompt = f"""
You are an expert AI tutor.

Rules:
- Explain clearly and simply
- Use structured answers
- Give examples when helpful
- Encourage understanding
- Stay mostly focused on topic: {topic}

Format answers like:
1. Explanation
2. Example (if needed)
3. Key takeaway
"""

    messages = [{"role": "system", "content": system_prompt}]

    # Add history
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})

    messages.append({"role": "user", "content": user_question})

    response = ollama.chat(
        model="llama3",
        messages=messages
    )

    answer = response["message"]["content"]

    # Safety fallback
    if not answer:
        answer = "Sorry, I couldn't generate a response. Try again."

    history.append({
        "user": user_question,
        "assistant": answer
    })

    return answer.strip(), history