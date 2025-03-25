import streamlit as st

st.set_page_config(page_title="Home", layout="wide")

st.title("🏠 Welcome to FDA First Generic Approvals Explorer")

st.markdown("""
This app helps you explore **first-time generic drug approvals** granted by the U.S. FDA.

📅 **Data source**: [FDA website](https://www.fda.gov/drugs/drug-approvals-and-databases/first-generic-drug-approvals)  
💡 **Purpose**: Enable interactive analysis of FDA's first generic (Gx) approvals for researchers, analysts, and curious minds.

---

### 🤖 What can I do here?
- Ask natural language questions about approval trends
- Visualize how many approvals occurred each year
- See which companies (applicants) were most active
- Explore the share of approvals by top 20 applicants
""")

st.markdown("---")

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    if st.button("🚀 **Start chat!**", use_container_width=True):
        st.switch_page("pages/2_chatbot.py")

with col2:
    if st.button("📈 What does the data say?", use_container_width=True):
        st.switch_page("pages/3_key_insights.py")

with col3:
    if st.button("✉️ Contact Me", use_container_width=True):
        st.switch_page("pages/4_contact.py")
