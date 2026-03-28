import streamlit as st

from agents.tutor_agent import explain_topic
from agents.quiz_agent import generate_quiz
from agents.evaluator_agent import evaluate_answer
from agents.feedback_agent import give_feedback
from ui.chat_agent import chat_with_tutor
from memory.progress_memory import ProgressMemory

# Initialize memory
memory = ProgressMemory()

# Streamlit page setup
st.set_page_config(
    page_title="AI Multi-Agent Tutor",
    layout="wide"
)

st.title("🤖 AI Multi-Agent Tutor")

# Session state
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Lesson", "Quiz", "Chat Tutor", "Progress"]
)

topic = st.sidebar.text_input("Enter Topic")

# -----------------------
# LESSON PAGE
# -----------------------

if menu == "Lesson":

    st.header("📘 AI Lesson Generator")

    if st.button("Generate Lesson"):

        explanation = explain_topic(topic)

        st.subheader("Explanation")
        st.write(explanation)

# -----------------------
# QUIZ PAGE
# -----------------------

elif menu == "Quiz":

    st.header("🧠 Quiz")

    if st.button("Start Quiz"):

        quiz_text = generate_quiz(topic)

        questions = quiz_text.split("Question")[1:]

        st.session_state.quiz_questions = questions
        st.session_state.current_question = 0

    if st.session_state.quiz_questions:

        q_index = st.session_state.current_question

        if q_index < len(st.session_state.quiz_questions):

            question_block = "Question" + st.session_state.quiz_questions[q_index]
            question_only = question_block.split("Correct Answer")[0]

            st.subheader(f"Question {q_index + 1}")

            st.write(question_only)

            user_answer = st.radio(
                "Select your answer",
                ["A", "B", "C", "D"]
            )

            if st.button("Submit Answer"):

                evaluation = evaluate_answer(question_only, user_answer)

                st.subheader("Evaluation")
                st.write(evaluation)

                feedback = give_feedback(topic, evaluation)

                st.subheader("Feedback")
                st.write(feedback)

                correct = "Correct" in evaluation
                memory.update(correct)

                st.session_state.current_question += 1

        else:

            st.success("Quiz Completed!")

# -----------------------
# CHAT TUTOR
# -----------------------

elif menu == "Chat Tutor":

    st.header("💬 Ask AI Tutor")

    user_question = st.text_input("Ask a question")

    if st.button("Ask Tutor"):

        answer, st.session_state.history = chat_with_tutor(
            user_question,
            topic,
            st.session_state.history
        )

        st.write(answer)

# -----------------------
# PROGRESS PAGE
# -----------------------

elif menu == "Progress":

    st.header("📊 Learning Progress")

    stats = memory.stats()

    st.metric("Questions Attempted", stats["attempted"])
    st.metric("Correct Answers", stats["correct"])
    st.metric("Accuracy", f"{stats['accuracy']}%")