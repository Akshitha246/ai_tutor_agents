import ollama

def generate_quiz(topic):

    prompt = f"""
Create 7 multiple choice questions about {topic}.

Format strictly like this:

Question 1:
A)
B)
C)
D)
Correct Answer:

Question 2:
A)
B)
C)
D)
Correct Answer:

Continue until Question 7.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role":"user","content":prompt}]
    )

    return response["message"]["content"]