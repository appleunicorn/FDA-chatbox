import streamlit as st
from scripts.charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie_range
)

st.set_page_config(page_title="Key Insights", layout="wide")

st.sidebar.title("🧭 Navigation")
st.sidebar.page_link("app.py", label="🏠 Home", icon="🏠")
st.sidebar.page_link("pages/2_chatbot.py", label="💬 Chatbot")
st.sidebar.page_link("pages/3_key_insights.py", label="📊 Key Insights")
st.sidebar.page_link("pages/4_contact.py", label="✉️ Contact")

st.title("📊 Key Insights from FDA Gx Approvals")
db_path = "fda_first_generic_approvals.db"

st.subheader("📈 Approvals by Year")
df1 = plot_anda_approvals_by_year(db_path=db_path, show=False)
st.pyplot()
st.markdown("> 💡 Approvals have shown interesting year-to-year variation.")

st.subheader("🏢 Unique Applicants by Year")
df2 = plot_applicants_by_year(db_path=db_path, show=False)
st.pyplot()
st.markdown("> 🧠 There has been steady participation across companies, with some spikes.")

st.subheader("🥇 Top 20 Applicants (2020–2024)")
df3 = plot_top_20_applicants_pie_range(start_year=2020, end_year=2024, db_path=db_path, show=False)
st.pyplot()
st.markdown("> 🧪 The market is dominated by a few key players.")
