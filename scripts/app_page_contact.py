import streamlit as st
import requests

def run():
    st.title("✉️ Contact Me")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")

        submitted = st.form_submit_button("Send")

        if submitted:
            if name and email and message:
                # For real apps, replace with proper email backend or service
                st.success("Thanks! Your message has been sent.")
                # Placeholder - print to logs or send via API
                print(f"Message from {name} <{email}>: {message}")
            else:
                st.error("Please fill out all fields.")
