import streamlit as st

def run():
    st.title("✉️ Contact Me")
    st.markdown("Feel free to reach out using the form below.")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submitted = st.form_submit_button("Send")

        if submitted:
            if name and email and message:
                st.success("✅ Thank you! Your message has been sent.")
                # Optional: integrate with email API (like Formspree or EmailJS)
            else:
                st.error("❌ Please fill in all fields.")
