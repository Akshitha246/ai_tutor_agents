import ollama

def chat_with_tutor(user_question, topic=None, history=None):
    
    if history is None:
        history = []

    system_prompt = f"""
You are an AI tutor helping students learn clearly.

Rules:
- Explain concepts simply
- Give real-world examples
- Encourage learning
- If the topic is {topic}, stay mostly related to that topic
- Keep answers structured and easy to understand
"""

    messages = [{"role": "system", "content": system_prompt}]

    # add conversation history
    for h in history:
        messages.append({"role": "user", "content": h["user"]})
        messages.append({"role": "assistant", "content": h["assistant"]})

    messages.append({"role": "user", "content": user_question})

    response = ollama.chat(
        model="llama3",
        messages=messages
    )

    answer = response["message"]["content"]

    history.append({
        "user": user_question,
        "assistant": answer
    })

    return answer, history