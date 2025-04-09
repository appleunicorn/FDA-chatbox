# Replace the hardcoded alias_dict with CSV-based lookup
import os
import re
import pandas as pd
import sqlite3
from glob import glob
from datetime import datetime
import pytz
import webbrowser

# === File Paths ===
csv_folder = "data/fda_data_download"
db_path = "fda_first_generic_approvals.db"
table_name = "fda_approvals"
output_html_path = "fda_preview.html"
applicant_keys_path = "data/applicant_keys.csv"

# === Load Alias Mapping from CSV ===
applicant_keys_df = pd.read_csv(applicant_keys_path, header=None, names=["original", "alias"])
alias_dict = dict(zip(applicant_keys_df["original"].str.strip().str.lower(), applicant_keys_df["alias"].str.strip()))

def get_alias_for_applicant(applicant: str) -> str:
    return alias_dict.get(applicant.strip().lower(), applicant.strip())

# === Load CSV Files ===
csv_files = glob(os.path.join(csv_folder, "first-time-gx-approval-*.csv"))

# === Connect to SQLite ===
conn = sqlite3.connect(db_path)

# === Drop and Recreate Table ===
print("\U0001F5D1️ Dropping and recreating table...")
conn.execute(f"DROP TABLE IF EXISTS {table_name};")

create_table_query = f"""
CREATE TABLE {table_name} (
    year_anda_number TEXT PRIMARY KEY,
    year INTEGER,
    anda_number TEXT,
    generic_name TEXT,
    anda_applicant TEXT,
    company_name_short TEXT, 
    brand_name TEXT,
    anda_approval_date DATE,
    anda_indication_description TEXT,
    import_timestamp DATETIME
);
"""

conn.execute(create_table_query)

# === Load & Insert Each CSV ===
eastern = pytz.timezone("US/Eastern")

for csv_file in csv_files:
    print(f"\U0001F4E5 Processing: {csv_file}")
    df = pd.read_csv(csv_file)

    df = df.rename(columns={
        "ANDA Number": "anda_number",
        "Generic Name": "generic_name",
        "ANDA Applicant": "anda_applicant",
        "Brand Name": "brand_name",
        "ANDA Approval Date": "anda_approval_date",
        "ANDA Indication+": "anda_indication_description"
    })

    df["anda_approval_date"] = pd.to_datetime(df["anda_approval_date"], errors="coerce").dt.date

    filename = os.path.basename(csv_file)
    year = int(filename.split("-")[4])
    df["year"] = year
    df["company_name_short"] = df["anda_applicant"].apply(get_alias_for_applicant)

    match = re.search(r"downloaded at-(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}[-+]\d{2}-\d{2})", filename)
    if match:
        raw_timestamp = match.group(1)
        iso_string = re.sub(r'T(\d{2})-(\d{2})-(\d{2})([-+]\d{2})-(\d{2})', r'T\1:\2:\3\4:\5', raw_timestamp)
        dt = datetime.fromisoformat(iso_string).astimezone(eastern)
    else:
        dt = datetime.now(eastern)

    df["import_timestamp"] = dt.strftime("%Y-%m-%d %H:%M:%S")

    df["year_anda_number"] = df["year"].astype(str) + "-" + df["anda_number"].astype(str)

    df = df[[
        "year_anda_number",
        "year",
        "anda_number",
        "generic_name",
        "anda_applicant",
        "company_name_short",
        "brand_name",
        "anda_approval_date",
        "anda_indication_description",
        "import_timestamp"
    ]]

    try:
        df.to_sql(table_name, conn, if_exists="append", index=False)
    except sqlite3.IntegrityError as e:
        print(f"⚠️ Skipping duplicate entries in {csv_file}: {e}")

print("✅ All files inserted into the database.\n")

# === View Summary Info ===
print("📋 Table Columns:")
columns_info = pd.read_sql(f"PRAGMA table_info({table_name});", conn)
print(columns_info[["name", "type"]])

first_rows = pd.read_sql(f"""
    SELECT * FROM {table_name}
    ORDER BY anda_approval_date ASC, LOWER(anda_applicant) ASC
    LIMIT 5;
""", conn)

last_rows = pd.read_sql(f"""
    SELECT * FROM (
        SELECT * FROM {table_name}
        ORDER BY anda_approval_date DESC, LOWER(anda_applicant) DESC
        LIMIT 5
    ) sub
    ORDER BY anda_approval_date ASC, LOWER(anda_applicant) ASC;
""", conn)

print("\n🔼 First 5 Rows:")
print(first_rows)

print("\n🔽 Last 5 Rows:")
print(last_rows)

preview_html = """
<html>
<head><title>FDA First Generic Approvals Preview</title></head>
<body>
    <h2>First 5 Rows</h2>
    {first_table}
    <br><br>
    <h2>Last 5 Rows</h2>
    {last_table}
</body>
</html>
"""

first_html = first_rows.to_html(index=False, border=1)
last_html = last_rows.to_html(index=False, border=1)
html_content = preview_html.format(first_table=first_html, last_table=last_html)

with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

webbrowser.open(f"file://{os.path.abspath(output_html_path)}")
print(f"\n🌐 Preview opened: {output_html_path}")

conn.close()