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

# Store chat logs manually for display
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# --- 🧹 Wipe Memory Button ---
st.markdown("---")
if st.button("🧹 Wipe Memory"):
    st.session_state.memory.clear()
    st.session_state.chat_log.clear()
    st.success("Chat memory wiped. Start fresh!")

# --- 📝 Input + Contextual Multi-Question Handler ---
question = st.text_input(
    "Ask a question about the FDA 1st Gx ANDA approval data:",
    placeholder="e.g., What is the trend of ANDA approvals over the last 5 years?"
)

if question:
    sub_questions = [q.strip() for q in question.split("?") if q.strip()]
    full_context = ""

    for i, q in enumerate(sub_questions, 1):
        q_full = q + "?"
        # Append previous context for follow-ups
        if full_context:
            input_query = f"{q_full} (based on previous context: '{full_context}')"
        else:
            input_query = q_full

        with st.spinner(f"🤖 Answering Q{i}..."):
            try:
                response = st.session_state.agent.run(input_query)

                st.markdown(f"### 🔹 Q{i}: {q_full}")
                st.write(response)

                # Save for chat history
                st.session_state.chat_log.append(("You", q_full))
                st.session_state.chat_log.append(("Bot", response))

                full_context += " " + q_full  # Build full rolling context

            except Exception as e:
                st.error(f"Error processing Q{i}: {e}")

# --- 💡 Suggested Questions ---
st.markdown("---")
st.subheader("💡 Try asking:")
st.markdown("""
- *What is the trend of ANDA approvals over the last 5 years?*  
- *Which company had the most first generics approved in 2024?*  
- *How many first Gx approvals were there in 2020-2024?*  
""")

# --- 🧠 Scrollable Chat History Box ---
st.markdown("---")
st.subheader("🧠 Chat History")

if st.session_state.chat_log:
    history_html = ""
    for role, msg in st.session_state.chat_log:
        icon = "🧑" if role == "You" else "🤖"
        history_html += f"<div><strong>{icon} {role}:</strong> {msg}</div><br>"

    st.markdown(f"""
    <div style='height: 300px; overflow-y: auto; padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 5px;'>
        {history_html}
    </div>
    """, unsafe_allow_html=True)
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
