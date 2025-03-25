import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.sidebar.title("🧭 Navigation")
st.sidebar.page_link("app.py", label="🏠 Home", icon="🏠")
st.sidebar.page_link("pages/2_chatbot.py", label="💬 Chatbot")
st.sidebar.page_link("pages/3_key_insights.py", label="📊 Key Insights")
st.sidebar.page_link("pages/4_contact.py", label="✉️ Contact")

st.title("🏠 Welcome to FDA First Generic Approvals Explorer")

st.markdown("""
This web app explores **first-time generic drug approvals** granted by the U.S. FDA.

📅 The data comes directly from the [FDA website](https://www.fda.gov/drugs/drug-and-biologic-approval-and-ind-activity-reports/first-generic-drug-approvals).

💡 The goal is to help researchers, analysts, and curious minds interactively explore this important approval data.

---
### 🤖 What you can do here:
- Ask natural language questions about approval trends
- Visualize how many approvals occurred each year
- See which companies (applicants) were most active
- Explore the share of approvals by top 20 applicants
""")

st.markdown("---")

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    if st.button("🚀 **Start chat!**"):
        st.switch_page("pages/2_chatbot.py")

with col2:
    if st.button("📈 What does the data say?"):
        st.switch_page("pages/3_key_insights.py")

with col3:
    if st.button("✉️ Contact me"):
        st.switch_page("pages/4_contact.py")
