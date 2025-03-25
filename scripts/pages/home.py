import streamlit as st

def run():
    st.title("🏠 Welcome to FDA First Generic Approvals Explorer")

    st.markdown("""
        This web app explores **first-time generic drug approvals** granted by the U.S. FDA.  
        📅 The data comes from the official [FDA source](https://www.fda.gov/drugs/drug-and-biologic-approval-and-ind-activity-reports/first-generic-drug-approvals).  
        💡 The goal is to help researchers, analysts, and curious minds interactively explore this important approval data.

        ---
        ### What you can do here:
        - Ask natural language questions about approval trends
        - Visualize how many approvals occurred each year
        - See which companies (applicants) were most active
        - Explore shares of approvals by the top 20 applicants
    """)

    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        if st.button("🚀 **Start chat!**"):
            st.session_state.page = "chatbot"
            st.session_state.override_from_button = True
            st.experimental_rerun()
    with col2:
        if st.button("📊 What does the data say?"):
            st.session_state.page = "key_insights"
            st.session_state.override_from_button = True
            st.experimental_rerun()
    with col3:
        if st.button("✉️ Contact Me"):
            st.session_state.page = "contact"
            st.session_state.override_from_button = True
            st.experimental_rerun()
