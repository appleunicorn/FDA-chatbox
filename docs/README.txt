FDA_project
├── app.py		     # Linked to Streamlit Cloud
├── .streamlit/
│   └── config.toml
├── requirements.txt	     # Required libraries
├── scripts/
│   ├── charts.py           # Functions for data visualization (bar charts, pie charts, etc.)
│   ├── analyze_sql.py      # SQL query utilities (optional; assumed from name)
│   ├── prompts.py          # Contains custom prompts for LangChain agent
│   └── langchain_agent.py  # Creates and configures the LangChain SQLite agent + 