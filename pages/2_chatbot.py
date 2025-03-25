import streamlit as st
from scripts.langchain_agent import create_sqlite_agent

st.set_page_config(page_title="Chatbot", layout="wide")

st.title("💬 Chat with me about FDA data!")

agent = create_sqlite_agent(db_path="fda_first_generic_approvals.db")

st.markdown("#### Ask me about the FDA database:")

question = st.text_input("")

if question:
    with st.spinner("🤖 Thinking..."):
        try:
            response = agent.run(question)
            st.markdown("### ✅ Answer")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("##### 💡 Try asking:")
st.markdown("""
- How many first generic approvals were there in 2023?
- Who are the top 5 companies by number of approvals?
- What is the trend in approvals from 2016 to 2024?
""")

col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Go to Home"):
        st.switch_page("pages/1_home.py")
with col2:
    if st.button("📊 Go to Key Insights"):
        st.switch_page("pages/3_key_insights.py")
