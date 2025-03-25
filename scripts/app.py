import streamlit as st
from scripts import app_page_home, app_page_chatbot, app_page_key_insights, app_page_contact

PAGES = {
    "🏠 Home": app_page_home.run,
    "💬 Chatbot": app_page_chatbot.run,
    "📊 Key Insights": app_page_key_insights.run,
    "✉️ Contact Me": app_page_contact.run,
}

st.set_page_config(page_title="FDA GPT Explorer", layout="wide")

st.sidebar.title("📌 Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
PAGES[selection]()
