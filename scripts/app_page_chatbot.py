import streamlit as st
from langchain_agent import create_sqlite_agent

def run():
    st.title("💬 Chat with me about FDA data!")

    agent = create_sqlite_agent(db_path="fda_first_generic_approvals.db")

    st.markdown("#### Ask me about the FDA database:")
    question = st.text_input("")

    if question:
        with st.spinner("🤖 Thinking..."):
            try:
                response = agent.run(question)
                st.success("✅ Answer")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown("#### Suggested Questions:")
    suggestions = [
        "What is the trend of ANDA approvals from 2020 to 2024?",
        "Which companies received the most approvals in 2023?",
        "How many unique applicants were there in 2022?",
        "Show me approval data for 2024 only."
    ]

    for q in suggestions:
        if st.button(q):
            st.experimental_set_query_params(question=q)
            st.rerun()

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Back to Home"):
            st.switch_page("scripts/app_page_home.py")
    with col2:
        if st.button("📊 Key Insights"):
            st.switch_page("scripts/app_page_key_insights.py")
