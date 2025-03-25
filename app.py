import streamlit as st

st.set_page_config(
    page_title="FDA Chatbot",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optional home content (or leave blank)
st.switch_page("pages/1_home.py")
