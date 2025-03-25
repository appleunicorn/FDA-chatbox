import streamlit as st
import app_page_home
import app_page_chatbot
import app_page_key_insights

PAGES = {
    "Home": app_page_home,
    "Chatbot": app_page_chatbot,
    "Key Insights": app_page_key_insights,
}

st.sidebar.title("📚 Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.app()
