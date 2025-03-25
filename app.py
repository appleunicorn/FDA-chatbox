import streamlit as st
from scripts.pages import home, chatbot, key_insights, contact

st.set_page_config(
    page_title="FDA First Generic Approvals",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---- Sidebar Navigation
st.sidebar.markdown("### 🧭 Navigation")
page_choice = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "💬 Chatbot", "📊 Key Insights", "✉️ Contact"],
    label_visibility="collapsed"
)

# Set session_state.page based on sidebar only if no button override
emoji_to_key = {
    "🏠 Home": "home",
    "💬 Chatbot": "chatbot",
    "📊 Key Insights": "key_insights",
    "✉️ Contact": "contact"
}
if not st.session_state.get("override_from_button"):
    st.session_state.page = emoji_to_key[page_choice]

# ---- Render selected page
if st.session_state.page == "home":
    home.run()
elif st.session_state.page == "chatbot":
    chatbot.run()
elif st.session_state.page == "key_insights":
    key_insights.run()
elif st.session_state.page == "contact":
    contact.run()

# Reset override flag (so sidebar works again after navigation)
st.session_state.override_from_button = False
