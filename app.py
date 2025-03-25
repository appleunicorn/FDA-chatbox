import streamlit as st
import pandas as pd
from scripts.langchain_agent import create_sqlite_agent
from scripts.charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie,
    plot_top_20_applicants_pie_range
)

st.set_page_config(page_title="FDA chatbot", layout="wide")
st.title("🤖 FDA ANDA Approvals Chatbot")

# --- 🧾 Intro Section ---
st.markdown("""
Welcome to **FDA First Generic Approvals Chatbot** 🎉

This app helps you explore trends, companies, and insights in FDA first-time generic drug approvals using a conversational AI and interactive analysis.

---

### 🧬 About the Data
- **Source:** [FDA First Generics](https://www.fda.gov/drugs/drug-and-biologic-approval-and-ind-activity-reports/first-generic-drug-approvals)
- **Data:** ANDA number, drug names, company, approval date, and more
- **Coverage:** Approvals from 2016 to present

---
""")

# --- 🤖 Chatbot Setup ---
st.subheader("💬 Chat with the Data")

DB_PATH = "fda_first_generic_approvals.db"

if "agent" not in st.session_state or "memory" not in st.session_state:
    agent, memory = create_sqlite_agent(db_path=DB_PATH)
    st.session_state.agent = agent
    st.session_state.memory = memory

# --- 🧹 Clear Memory Button ---
st.markdown("---")
if st.button("🧹 Wipe Memory"):
    if "memory" in st.session_state:
        st.session_state.memory.clear()
        st.success("Chat memory wiped. Start fresh!")

# --- 📝 User Input + Split Compound Questions ---
question = st.text_input(
    "Ask a question about the FDA approval data:",
    placeholder="e.g., Who were top players in past 5 years? In past 3 years? Compare the lists."
)

if question:
    sub_questions = [q.strip() for q in question.split("?") if q.strip()]
    
    for i, q in enumerate(sub_questions, 1):
        with st.spinner(f"🤖 Answering part {i}..."):
            try:
                response = st.session_state.agent.run(q + "?")
                st.markdown(f"### 🔹 Q{i}: {q}?")
                st.write(response)
            except Exception as e:
                st.error(f"Error processing Q{i}: {e}")

# --- 💬 Chat History ---
if st.session_state.memory.buffer:
    st.markdown("---")
    st.subheader("🧠 Chat History")
    for msg in st.session_state.memory.chat_memory.messages:
        role = "You" if msg.type == "human" else "Bot"
        st.markdown(f"**{role}:** {msg.content}")

# --- 💡 Sample Questions ---
st.markdown("---")
st.subheader("💡 Try asking:")
st.markdown("""
- *What is the trend of ANDA approvals over the last 5 years?*  
- *Which company had the most first generics approved in 2023?*  
- *How many first Gx applicants were there in 2020?*  
- *Who were the top 5 companies from 2020 to 2024?*  
- *Compare top applicants in the past 5 years vs past 3 years.*
""")

# --- 📬 Contact Section ---
st.markdown("---")
st.subheader("📬 Contact Me")
st.markdown("""
Created by **Autumn Qiu**  
📧 Email: autumn.qiut@gmail.com  
🌐 GitHub: [appleunicorn](https://github.com/appleunicorn)
""")
