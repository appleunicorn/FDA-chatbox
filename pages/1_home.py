import streamlit as st

def main():
    st.title("🏠 Welcome to FDA First Generic Approvals Explorer")

    st.markdown("""
        This web app explores **first-time generic drug approvals** granted by the U.S. FDA.  
        📅 The data comes from the official [FDA source](https://www.fda.gov/drugs/drug-and-biologic-approval-and-ind-activity-reports/first-generic-drug-approvals).  
        💡 The goal is to help researchers, analysts, and curious minds interactively explore this important approval data.
    """)

    st.markdown("---")
    st.subheader("What would you like to do?")
    col1, col2, col3 = st.columns([1.2, 1, 1])

    with col1:
        if st.button("🚀 Start chat!"):
            st.switch_page("pages/2_chatbot.py")
    with col2:
        if st.button("📊 What does the data say?"):
            st.switch_page("pages/3_key_insights.py")
    with col3:
        if st.button("✉️ Contact me"):
            st.switch_page("pages/4_contact.py")

# 🔁 Call the main function!
main()
