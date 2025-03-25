import streamlit as st

st.set_page_config(page_title="Contact", layout="wide")

st.sidebar.title("🧭 Navigation")
st.sidebar.page_link("app.py", label="🏠 Home", icon="🏠")
st.sidebar.page_link("pages/2_chatbot.py", label="💬 Chatbot")
st.sidebar.page_link("pages/3_key_insights.py", label="📊 Key Insights")
st.sidebar.page_link("pages/4_contact.py", label="✉️ Contact")

st.title("✉️ Contact Me")

with st.form(key="contact_form"):
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    message = st.text_area("Your message")

    if st.form_submit_button("Send"):
        st.success("Thanks! Your message has been sent to autumn.qiut@gmail.com.")
