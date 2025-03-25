import streamlit as st

def app():
    st.title("💊 FDA First Generic Approvals Explorer")

    st.markdown("""
    ### 🧬 About the Database
    This database tracks **first generic drug approvals (Gx)** by the U.S. FDA. First generics are important as they mark the first time a non-brand version of a drug is approved, often lowering drug costs and increasing access.

    ### 🎯 Purpose of this App
    This webapp allows you to:
    - Ask natural language questions about the FDA Gx approval data
    - Visualize trends and company activity in first generic approvals
    - Interact with charts and key summaries

    ### 🧠 Try Asking Questions Like:
    - *"How many approvals were there in 2023?"*
    - *"Which company had the most ANDA approvals?"*
    - *"What is the trend in first generics from 2015 to 2024?"*

    ---
    """)

    if st.button("🔍 Go to Chatbot"):
        st.switch_page("scripts/app_page_chatbot.py")

    st.markdown("---")
    st.subheader("📬 Contact Me")
    st.markdown("For questions or feedback, feel free to [email me](mailto:autumn.qiut@gmail.com)")
