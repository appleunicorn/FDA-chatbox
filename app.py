import streamlit as st

st.info("👋 app.py is running")

st.set_page_config(
    page_title="FDA First Generic Approvals",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fallback message if someone runs app.py directly
st.markdown("<!-- This app uses multipage navigation -->")
