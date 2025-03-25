import streamlit as st

st.set_page_config(
    page_title="FDA First Generic Explorer",
    page_icon="💊",
    layout="wide"
)

# Redirect users to home automatically
st.switch_page("pages/1_home.py")
