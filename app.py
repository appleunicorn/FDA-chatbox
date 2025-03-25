import streamlit as st
from scripts.langchain_agent import create_sqlite_agent
from scripts.charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie,
    plot_top_20_applicants_pie_range
)

st.set_page_config(page_title="FDA chatbot", layout="wide")
st.title("💬 FDA ANDA Approvals Chatbot")

# --- Landing Page Info ---
st.markdown("""
Welcome to **FDA First Generic Approvals Chatbot** 🎉

This web app allows you to explore the data and insights based on FDA first-time generic drug ANDA approvals since 2016. It is powered by an interactive natural language agent using OpenAI and LangChain.

---

### 🧬 **About the Database**
This dataset contains yearly records of **first generic ANDA (Abbreviated New Drug Application) approvals** from the FDA. First generics are the first version of a brand-name drug to be approved, marking the beginning of market competition.

- **Data source**: [FDA First Generics](https://www.fda.gov/drugs/drug-and-biologic-approval-and-ind-activity-reports/first-generic-drug-approvals)  
- **Data format**: CSV files downloaded from the FDA website  
- **Data fields**: ANDA number, generic and brand name, applicant (company), approval date, indication, etc.

---

### 🎯 **Purpose of this Web App**
This app helps users:
- Analyze trends in generic approvals over time
- Explore top applicants in each year or across year ranges
- Interact with the database using **natural language questions**
- Generate dynamic visualizations on demand

---
""")

# --- 💬 Chatbot Section ---
st.subheader("💬 Chat with the Data")

DB_PATH = "fda_first_generic_approvals.db"
agent = create_sqlite_agent(db_path=DB_PATH)

question = st.text_input(
    "Ask a question about the FDA approval data:",
    placeholder="e.g., Which company had the most first generics approved in 2023?"
)

if question:
    with st.spinner("🤖 Thinking..."):
        try:
            response = agent.run(question)
            st.markdown("### ✅ Answer")
            st.write(response)
        except Exception as e:
            st.error(f"Error: {e}")

# --- 💡 Guiding Questions (non-clickable) ---
st.markdown("---")
st.subheader("💡 Try asking one of these:")

st.markdown("""
- *What is the trend of ANDA approvals over the last 5 years?*  
- *Which company had the most first generics approved in 2023?*  
- *How many first Gx applicants were there in 2020?*  
- *Show a chart of number of approvals by year.*  
- *Who were the top 20 generic applicants from 2020 to 2024?*  
""")

# --- 📊 Visual Chart Section ---
st.markdown("---")
st.subheader("📊 Key Insights from Data")

chart_type = st.selectbox("Choose a chart to view:", [
    "Number of approvals by Year",
    "Number of applicants by Year",
    "Top 20 Applicants (Single Year)",
    "Top 20 Applicants (Year Range)"
])

if chart_type == "Number of approvals by Year":
    if st.button("Show"):
        df = plot_anda_approvals_by_year(db_path=DB_PATH, show=True)
        st.dataframe(df)

elif chart_type == "Number of applicants by Year":
    if st.button("Show"):
        df = plot_applicants_by_year(db_path=DB_PATH, show=True)
        st.dataframe(df)

elif chart_type == "Top 20 Applicants (Single Year)":
    year = st.number_input("Year", value=2024)
    if st.button("Generate"):
        df = plot_top_20_applicants_pie(db_path=DB_PATH, year=year, show=True)
        st.dataframe(df)

elif chart_type == "Top 20 Applicants (Year Range)":
    start = st.number_input("Start Year", value=2020)
    end = st.number_input("End Year", value=2024)
    if st.button("Generate Range"):
        df = plot_top_20_applicants_pie_range(start_year=start, end_year=end, db_path=DB_PATH, show=True)
        st.dataframe(df)

# --- 📬 Contact Section ---
st.markdown("---")
st.subheader("📬 Contact Me")
st.markdown("""
Created by **Autumn Qiu**  
📧 Email: autumn.qiut@gmail.com  
🌐 GitHub: [appleunicorn](https://github.com/appleunicorn)
""")
