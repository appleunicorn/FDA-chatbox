import streamlit as st

st.set_page_config(page_title="Contact", page_icon="✉️", layout="wide")

st.title("✉️ Contact Me")

st.markdown("If you have questions, suggestions, or want to collaborate, drop me a message below!")

with st.form("contact_form"):
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    message = st.text_area("Your message")

    submitted = st.form_submit_button("Send")
    if submitted:
        st.success("✅ Message submitted! Thanks for reaching out 🙌")
        # (Optional) You can add backend email functionality here (e.g., SMTP, Mail API)
