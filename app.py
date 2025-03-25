import streamlit as st
from pages import home, chatbot, key_insights, contact

st.set_page_config(
    page_title="FDA First Generic Approvals",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar nav (custom!)
st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "💬 Chatbot", "📊 Key Insights", "✉️ Contact"],
    label_visibility="collapsed"
)

# Route to page
if page == "🏠 Home":
    home.run()
elif page == "💬 Chatbot":
    chatbot.run()
elif page == "📊 Key Insights":
    key_insights.run()
elif page == "✉️ Contact":
    contact.run()


#trivial change