import ollama

def explain_topic(topic):

    prompt = f"""
You are an AI tutor.

Explain the topic clearly.

Topic: {topic}

Include:
1. Simple explanation
2. Example
3. Key takeaway
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]