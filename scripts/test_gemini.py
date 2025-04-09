import google.generativeai as genai
import streamlit as st

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

print("Available Gemini Models:\n")
for model in genai.list_models():
    print(f"- {model.name} (available: {model.supported_generation_methods})")
