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

# --- 🧼 Always clear memory and chat log on refresh ---
if "memory" in st.session_state:
    st.session_state.memory.clear()
if "chat_log" in st.session_state:
    st.session_state.chat_log.clear()

# --- 🧬 Intro Section ---
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

if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# --- 🧹 Wipe Memory Button ---
st.markdown("---")
if st.button("🧹 Wipe Memory"):
    st.session_state.memory.clear()
    st.session_state.chat_log.clear()
    st.success("Chat memory wiped. Start fresh!")

# --- 📝 Question Input + Multi-Question Logic ---
question = st.text_input(
    "Ask a question about the FDA approval data:",
    placeholder="e.g., Who were top players in past 5 years in number of approvals?"
)

if question:
    sub_questions = [q.strip() for q in question.split("?") if q.strip()]
    full_context = ""
    is_multi = len(sub_questions) > 1

    for i, q in enumerate(sub_questions, 1):
        q_full = q + "?"
        if full_context:
            input_query = f"{q_full} Based on the previous questions: {full_context}"
        else:
            input_query = q_full

        with st.spinner("🤖 Answering..."):
            try:
                response = st.session_state.agent.run(input_query)

                label = f"### 🔹 Q{i}:" if is_multi else "### 🔹 Q:"
                st.markdown(f"{label} {q_full}")
                st.write(response)

                st.session_state.chat_log.append(("You", q_full))
                st.session_state.chat_log.append(("Bot", response))

                full_context += " " + q_full
            except Exception as e:
                st.error(f"Error: {e}")

# --- 💡 Sample Questions ---
st.markdown("---")
st.subheader("💡 Try asking:")
st.markdown("""
- *What is the trend of ANDA approvals over the last 5 years?*  
- *Which company had the most approvals in 2023?*  
- *How many applicants were there from 2018 to 2024 in each year?*  
- *Who were the top 5 companies from 2020 to 2024?*  
""")


# --- 🧠 Simple Scrollable Chat History Box ---
st.markdown("---")
st.subheader("🧠 Chat History")

if st.session_state.chat_log:
    st.markdown("### ")
    with st.expander("Click to view full conversation", expanded=True):
        # HTML to create scrollable container
        st.markdown("""
        <div style='height: 300px; overflow-y: auto; background-color: #f9f9f9; padding: 10px; border-radius: 5px; border: 1px solid #ccc;'>
        """, unsafe_allow_html=True)

        # Loop inside the grey box
        for role, msg in st.session_state.chat_log:
            st.markdown(f"**{role}:** {msg}")

        # Close the scrollable div
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("No conversation history yet.")





# --- 📬 Contact Section ---
st.markdown("---")
st.subheader("📬 Contact Me")
st.markdown("""
Created by **Autumn Qiu**  
📧 Email: autumn.qiut@gmail.com  
🌐 GitHub: [appleunicorn](https://github.com/appleunicorn)
""")
