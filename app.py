import streamlit as st
from scripts.pages import home, chatbot, key_insights, contact

st.set_page_config(
    page_title="FDA First Generic Approvals",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar nav (manual, with session state)
st.sidebar.markdown("### 🧭 Navigation")
page_choice = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "💬 Chatbot", "📊 Key Insights", "✉️ Contact"],
    label_visibility="collapsed"
)

# Convert emoji nav to internal state names
page_map = {
    "🏠 Home": "home",
    "💬 Chatbot": "chatbot",
    "📊 Key Insights": "key_insights",
    "✉️ Contact": "contact"
}
st.session_state.page = page_map[page_choice]

# Load the selected page
if st.session_state.page == "home":
    home.run()
elif st.session_state.page == "chatbot":
    chatbot.run()
elif st.session_state.page == "key_insights":
    key_insights.run()
elif st.session_state.page == "contact":
    contact.run()
