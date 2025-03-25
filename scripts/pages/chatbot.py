import streamlit as st
from scripts.langchain_agent import create_sqlite_agent

def run():
    st.title("💬 Chat with me about FDA data!")
    st.markdown("Ask me about the FDA database:")

    DB_PATH = "fda_first_generic_approvals.db"
    agent = create_sqlite_agent(db_path=DB_PATH)

    question = st.text_input("Enter your question:")
    if question:
        with st.spinner("🤖 Thinking..."):
            try:
                response = agent.run(question)
                st.markdown("### ✅ Answer")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")

    # Navigation buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Back to Home"):
            st.session_state.page = "home"
            st.session_state.override_from_button = True
            st.experimental_rerun()
    with col2:
        if st.button("📊 See Key Insights"):
            st.session_state.page = "key_insights"
            st.session_state.override_from_button = True
            st.experimental_rerun()
