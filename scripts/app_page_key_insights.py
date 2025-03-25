import streamlit as st
from charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie_range
)

def run():
    st.title("📊 Key Insights from FDA Gx Approvals")
    db_path = "fda_first_generic_approvals.db"

    st.subheader("📈 Trend of Approvals by Year")
    df1 = plot_anda_approvals_by_year(db_path=db_path, show=False)
    st.pyplot()
    st.markdown("> 📝 We observe a consistent pattern in approvals, with notable increases in recent years.")

    st.subheader("🏢 Number of Unique Applicants by Year")
    df2 = plot_applicants_by_year(db_path=db_path, show=False)
    st.pyplot()
    st.markdown("> 🧪 The number of unique applicants has been steady with occasional spikes.")

    st.subheader("🥧 Top 20 Applicants (2020–2024)")
    df3 = plot_top_20_applicants_pie_range(start_year=2020, end_year=2024, db_path=db_path, show=False)
    st.pyplot()
    st.markdown("> 🏆 A few large players dominate approvals, but there is a long tail of other companies contributing.")
