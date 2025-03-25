import streamlit as st
from langchain_agent import create_sqlite_agent

def app():
    st.title("💬 Ask about FDA Gx Approvals")

    DB_PATH = "fda_first_generic_approvals.db"
    agent = create_sqlite_agent(db_path=DB_PATH)

    st.markdown("#### 🤖 Ask a question about the database:")
    question = st.text_input("E.g., Which company had the most approvals in 2023?")

    if question:
        with st.spinner("Thinking..."):
            try:
                response = agent.run(question)
                st.markdown("### ✅ Answer")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("#### 💡 Guiding Questions:")
    guiding = [
        "How many approvals were there in 2023?",
        "Which company had the most ANDA approvals?",
        "What is the trend in first generics from 2015 to 2024?",
        "How many unique applicants got approvals in 2022?"
    ]
    for q in guiding:
        if st.button(q):
            st.session_state["input"] = q
            st.experimental_rerun()
