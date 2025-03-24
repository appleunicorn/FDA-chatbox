import streamlit as st
from langchain_agent import create_sqlite_agent
from charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie,
    plot_top_20_applicants_pie_range
)
import os
import sqlite3

st.set_page_config(page_title="FDA GPT Explorer", layout="wide")
st.title("💬 FDA First Generic Approvals Q&A")

DB_PATH = "fda_first_generic_approvals.db"
agent = create_sqlite_agent(db_path=DB_PATH)

# --- User Input ---
question = st.text_input("Ask a question about the FDA approval data:")

if question:
    with st.spinner("🤖 Thinking..."):
        try:
            response = agent.run(question)
            st.markdown("### ✅ Answer")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")

# --- Optional Chart Shortcuts ---
st.sidebar.header("📊 Visual Charts")

chart_type = st.sidebar.selectbox("Choose Chart", [
    "Approvals by Year",
    "Applicants by Year",
    "Top 20 Applicants (Single Year)",
    "Top 20 Applicants (Year Range)"
])

if chart_type == "Approvals by Year":
    if st.sidebar.button("Show"):
        df = plot_anda_approvals_by_year(db_path=DB_PATH, show=True)
        st.dataframe(df)

elif chart_type == "Applicants by Year":
    if st.sidebar.button("Show"):
        df = plot_applicants_by_year(db_path=DB_PATH, show=True)
        st.dataframe(df)

elif chart_type == "Top 20 Applicants (Single Year)":
    year = st.sidebar.number_input("Year", value=2024)
    if st.sidebar.button("Generate"):
        df = plot_top_20_applicants_pie(db_path=DB_PATH, year=year, show=True)
        st.dataframe(df)

elif chart_type == "Top 20 Applicants (Year Range)":
    start = st.sidebar.number_input("Start Year", value=2020)
    end = st.sidebar.number_input("End Year", value=2024)
    if st.sidebar.button("Generate Range"):
        df = plot_top_20_applicants_pie_range(start_year=start, end_year=end, db_path=DB_PATH, show=True)
        st.dataframe(df)
