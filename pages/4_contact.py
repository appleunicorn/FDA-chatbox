import streamlit as st

st.set_page_config(page_title="Contact", layout="wide")

st.title("✉️ Contact Me")

st.markdown("If you'd like to reach out, please fill in your message below:")

with st.form("contact_form"):
    name = st.text_input("Your name")
    email = st.text_input("Your email")
    message = st.text_area("Message", height=200)

    submitted = st.form_submit_button("Send Message")
    if submitted:
        st.success("Thanks! Your message has been sent.")
        # Optionally, send via email or store in a database here
