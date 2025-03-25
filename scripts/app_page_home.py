import streamlit as st

def run():
    st.title("🏠 Welcome to FDA First Generic Approvals Explorer")

    st.markdown("""
        This web app explores **first-time generic drug approvals** granted by the U.S. FDA.  
        📅 The data comes directly from the [FDA website](https://www.fda.gov/drugs/drug-approvals-and-databases/first-generic-drug-approvals).  
        💡 The goal is to help researchers, analysts, and curious minds interactively explore this important approval data.

        ---
        ### 🤖 What you can do here
        - Ask natural language questions about approval trends
        - Visualize how many approvals occurred each year
        - See which companies (applicants) were most active
        - Explore the share of approvals by top 20 applicants

        ---
    """)

    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        if st.button("🚀 **Start chat!**"):
            st.switch_page("scripts/app_page_chatbot.py")

    with col2:
        if st.button("📈 What does the data say?"):
            st.switch_page("scripts/app_page_key_insights.py")

    with col3:
        if st.button("✉️ Contact Me"):
            st.switch_page("scripts/app_page_contact.py")
