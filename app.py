import streamlit as st

# ❗ This MUST be the very first Streamlit call
st.set_page_config(
    page_title="FDA First Generic Approvals",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Do NOT include anything else here that uses Streamlit
# Streamlit will auto-load 1_home.py from the /pages folder
