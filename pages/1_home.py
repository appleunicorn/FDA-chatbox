import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

st.title("🏠 Welcome to FDA First Generic Approvals Explorer")

st.markdown("""
This web app explores **first-time generic drug approvals** granted by the U.S. FDA.  
📅 The data comes from the official [FDA source](https://www.fda.gov/drugs/drug-and-biologic-approval-and-ind-activity-reports/first-generic-drug-approvals).  
💡 The goal is to help researchers, analysts, and curious minds interactively explore this important approval data.

---

### What you can do here:
- Ask natural language questions about approval trends
- Visualize how many approvals occurred each year
- See which companies (applicants) were most active
- Explore shares of approvals by the top 20 applicants

👉 Use the **navigation bar on the left** to explore the app.
""")
