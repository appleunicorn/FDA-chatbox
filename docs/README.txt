1️⃣ File 1: FDA Data Downloader (done ✅)

Downloads latest FDA data

Skips existing downloads

Archives older ones

Adds ISO timestamp

Saves CSVs to data/fda_data_download/

2️⃣ File 2: SQL Database Creator (done ✅)

Loads the most recent CSVs

Parses timestamps from filename

Loads data into fda_first_generic_approvals.db

Creates full preview with HTML + SQLite

Note: Once in production, need to add smart import logic; need to change to append mode: only add new approvals

3️⃣ File 3: SQL Analysis (To Be Built)

Query the DB directly (sqlite3 or pandas.read_sql)

Run statistical analysis (groupby, value_counts)

Create charts and dashboards

4️⃣ File 4: Streamlit Web App with Natural Language Q&A (To Be Built 🚧)

Show tables + filters

Show charts (Plotly, Altair)

Enable natural language Q&A (LangChain + OpenAI)
