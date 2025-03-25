# scripts/app.py

import streamlit as st
from app_page_home import show as show_home
from app_page_chatbot import show as show_chatbot
from app_page_key_insights import show as show_key_insights
from app_page_contact import show as show_contact

# App-wide configuration
st.set_page_config(page_title="FDA GPT Explorer", layout="wide")

# Permanent sidebar navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "💬 Chatbot", "📊 Key Insights", "📬 Contact"])

# Route to selected page
if page == "🏠 Home":
    show_home()
elif page == "💬 Chatbot":
    show_chatbot()
elif page == "📊 Key Insights":
    show_key_insights()
elif page == "📬 Contact":
    show_contact()
