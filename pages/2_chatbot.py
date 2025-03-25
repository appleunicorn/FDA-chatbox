import streamlit as st
from scripts.langchain_agent import create_sqlite_agent

st.set_page_config(page_title="Chatbot", page_icon="💬", layout="wide")

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
