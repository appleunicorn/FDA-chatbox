import streamlit as st

# This must be the first command
st.set_page_config(
    page_title="FDA First Generic Approvals",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar navigation
page = st.sidebar.selectbox("Select a page", ["Home", "Chatbot", "Key Insights", "Contact"])

if page == "Home":
    st.write("✅ You selected Home!")
elif page == "Chatbot":
    st.write("✅ You selected Chatbot!")
elif page == "Key Insights":
    st.write("✅ You selected Key Insights!")
elif page == "Contact":
    st.write("✅ You selected Contact!")
