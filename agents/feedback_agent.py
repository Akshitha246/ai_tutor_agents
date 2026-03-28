import ollama

def give_feedback(topic, evaluation):

    prompt = f"""
Topic: {topic}

Evaluation:
{evaluation}

Provide constructive feedback and study advice.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]