import ollama

def explain_topic(topic):

    if not topic or topic.strip() == "":
        return "Please enter a valid topic."

    prompt = f"""
You are an expert AI tutor.

Teach the topic in a clear, structured, and engaging way.

Topic: {topic}

Follow this format strictly:

1. Simple Explanation:
Explain in easy terms.

2. Example:
Give a real-world or intuitive example.

3. Key Takeaways:
- Point 1
- Point 2
- Point 3

Keep it concise but informative.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    # Safety fallback
    if not content:
        return "Unable to generate explanation. Try again."

    return content.strip()