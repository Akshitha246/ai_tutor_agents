from agents.tutor_agent import explain_topic
from agents.quiz_agent import generate_quiz
from agents.evaluator_agent import evaluate_answer
from agents.feedback_agent import give_feedback
from memory.progress_memory import ProgressMemory

memory = ProgressMemory()

print("AI Multi-Agent Tutor")

topic = input("Enter topic: ")

print("\n--- Explanation ---\n")
print(explain_topic(topic))

print("\n--- Quiz ---\n")

quiz = generate_quiz(topic)

questions = quiz.split("Question")[1:]

for i, q in enumerate(questions, start=1):

    question_text = "Question" + q
    question_only = question_text.split("Correct Answer")[0]

    print("\n----------------------------")
    print(question_only)

    user_answer = input("Your answer (A/B/C/D): ").strip().upper()

    print("\n--- Evaluation ---")

    evaluation = evaluate_answer(question_only, user_answer)

    print(evaluation)

    correct = "Correct" in evaluation
    memory.update(correct)

    print("\n--- Feedback ---")

    feedback = give_feedback(topic, evaluation)
    print(feedback)

print("\n--- Final Score ---")
print(memory.stats())