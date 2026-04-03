import streamlit as st

def human_in_loop_evaluation(question, user_answer, ai_eval, q_index):

    st.subheader("🤖 AI Evaluation")
    st.write(f"Result: {ai_eval['result']}")
    st.write(f"Confidence: {ai_eval['confidence']}")
    st.write(f"Explanation: {ai_eval['explanation']}")

    st.subheader("🧑 Human Review (HITL)")

    # unique keys to prevent reset
    decision = st.radio(
        "Do you agree with AI?",
        ["Accept AI Decision", "Override AI Decision"],
        key=f"decision_{q_index}"
    )

    if decision == "Override AI Decision":

        correct = st.radio(
            "Final decision:",
            ["Correct", "Incorrect"],
            key=f"correct_{q_index}"
        )

        manual_feedback = st.text_area(
            "Custom feedback",
            key=f"feedback_{q_index}"
        )

        return {
            "result": correct,
            "feedback": manual_feedback if manual_feedback else "Human override"
        }

    else:
        return {
            "result": ai_eval["result"],
            "feedback": ai_eval["explanation"]
        }