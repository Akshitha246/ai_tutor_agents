import streamlit as st
import pandas as pd
import altair as alt

from agents.tutor_agent import explain_topic
from agents.quiz_agent import generate_quiz
from agents.evaluator_agent import evaluate_answer
from agents.feedback_agent import give_feedback
from ui.hitl import human_in_loop_evaluation
from ui.chat_agent import chat_with_tutor
from memory.progress_memory import ProgressMemory

# ---------------- MEMORY ----------------
if "memory" not in st.session_state:
    st.session_state.memory = ProgressMemory()

memory = st.session_state.memory

# ---------------- PAGE ----------------
st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("🤖 AI Multi-Agent Tutor (HITL)")

# ---------------- SESSION ----------------
if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "last_eval" not in st.session_state:
    st.session_state.last_eval = None

if "show_next" not in st.session_state:
    st.session_state.show_next = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ NEW: store per-question correctness (for spike graph)
if "question_history" not in st.session_state:
    st.session_state.question_history = []

# ---------------- SIDEBAR ----------------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Lesson", "Quiz", "Chat Tutor", "Progress"]
)

topic = st.sidebar.text_input("Enter Topic")

# ---------------- LESSON ----------------
if menu == "Lesson":

    st.header("📘 Lesson")

    if st.button("Generate Lesson"):
        st.write(explain_topic(topic))

# ---------------- QUIZ ----------------
elif menu == "Quiz":

    st.header("🧠 Quiz")

    # Restart
    if st.button("🔄 Restart Quiz"):
        st.session_state.quiz_questions = []
        st.session_state.current_question = 0
        st.session_state.submitted = False
        st.session_state.last_eval = None
        st.session_state.show_next = False
        st.session_state.question_history = []  # reset graph

        memory.total_questions = 0
        memory.correct_answers = 0

        st.rerun()

    # Start
    if st.button("Start Quiz"):

        quiz_text = generate_quiz(topic)
        questions = quiz_text.split("Question")[1:]

        st.session_state.quiz_questions = questions
        st.session_state.current_question = 0
        st.session_state.submitted = False
        st.session_state.last_eval = None
        st.session_state.show_next = False
        st.session_state.question_history = []  # reset graph

        memory.total_questions = 0
        memory.correct_answers = 0

    if st.session_state.quiz_questions:

        q_index = st.session_state.current_question
        total_q = len(st.session_state.quiz_questions)

        if q_index < total_q:

            st.progress(q_index / total_q, text=f"Question {q_index + 1} of {total_q}")

            stats_live = memory.stats()
            st.info(f"Score: {stats_live['correct']} / {stats_live['attempted']}")

            block = "Question" + st.session_state.quiz_questions[q_index]
            question_only = block.split("Correct Answer")[0]

            st.subheader(f"Question {q_index + 1}")
            st.write(question_only)

            user_answer = st.radio(
                "Choose answer",
                ["A", "B", "C", "D"],
                key=f"answer_{q_index}"
            )

            if not st.session_state.submitted:
                if st.button("Submit Answer"):

                    ai_eval = evaluate_answer(question_only, user_answer)

                    st.session_state.last_eval = ai_eval
                    st.session_state.submitted = True
                    st.session_state.show_next = False

            if st.session_state.submitted and st.session_state.last_eval:

                ai_eval = st.session_state.last_eval

                st.subheader("🤖 AI Evaluation")
                st.write(f"Result: {ai_eval['result']}")
                st.write(f"Confidence: {ai_eval['confidence']}")
                st.write(f"Explanation: {ai_eval['explanation']}")

                ai_feedback = give_feedback(topic, ai_eval)
                st.subheader("📘 AI Feedback")
                st.write(ai_feedback)

                if ai_eval["confidence"] in ["Low", "Medium"]:
                    hitl = human_in_loop_evaluation(
                        question_only,
                        user_answer,
                        ai_eval,
                        q_index
                    )
                    final_result = hitl["result"]
                    final_feedback = hitl["feedback"]
                else:
                    st.success("High confidence — auto accepted")
                    final_result = ai_eval["result"]
                    final_feedback = ai_eval["explanation"]

                st.subheader("🧑 Final Decision")
                st.write(final_result)

                st.subheader("📝 Final Feedback")
                st.write(final_feedback)

                correct = final_result == "Correct"

                # ✅ store spike data
                if not st.session_state.show_next:
                    memory.update(correct)
                    st.session_state.question_history.append(1 if correct else 0)
                    st.session_state.show_next = True

                if st.button("➡️ Next Question"):

                    st.session_state.current_question += 1
                    st.session_state.submitted = False
                    st.session_state.last_eval = None
                    st.session_state.show_next = False

                    st.rerun()

        else:
            st.success("🎉 Quiz Completed")

            stats = memory.stats()

            st.write("### Final Score")
            st.write(f"Correct: {stats['correct']}")
            st.write(f"Total: {stats['attempted']}")
            st.write(f"Accuracy: {stats['accuracy']}%")

            # ✅ Spike graph here too
            if st.session_state.question_history:
                df = pd.DataFrame({
                    "Question": list(range(1, len(st.session_state.question_history) + 1)),
                    "Result": st.session_state.question_history
                })

                chart = alt.Chart(df).mark_line(point=True).encode(
                    x="Question:Q",
                    y=alt.Y("Result:Q", scale=alt.Scale(domain=[0, 1])),
                    tooltip=["Question", "Result"]
                )

                st.subheader("📈 Performance Spike Graph")
                st.altair_chart(chart, use_container_width=True)

# ---------------- CHAT ----------------
elif menu == "Chat Tutor":

    st.header("💬 Chat with AI Tutor")

    user_question = st.text_input("Ask your question")

    if st.button("Ask"):

        answer, st.session_state.chat_history = chat_with_tutor(
            user_question,
            topic,
            st.session_state.chat_history
        )

        st.write(answer)

# ---------------- PROGRESS ----------------
elif menu == "Progress":

    st.header("📊 Progress")

    stats = memory.stats()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Questions Attempted", stats["attempted"])

    with col2:
        st.metric("Correct Answers", stats["correct"])

    with col3:
        st.metric("Accuracy (%)", stats["accuracy"])

    # ✅ Spike graph in Progress tab
    if st.session_state.question_history:
        df = pd.DataFrame({
            "Question": list(range(1, len(st.session_state.question_history) + 1)),
            "Result": st.session_state.question_history
        })

        chart = alt.Chart(df).mark_line(point=True).encode(
            x="Question:Q",
            y=alt.Y("Result:Q", scale=alt.Scale(domain=[0, 1])),
            tooltip=["Question", "Result"]
        )

        st.subheader("📈 Overall Performance (Spike Graph)")
        st.altair_chart(chart, use_container_width=True)