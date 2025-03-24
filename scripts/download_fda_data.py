# %% Step 1: import libraries and check api keys
import os
import re
from IPython.display import display, Markdown, HTML, Latex, JSON
import math
import statistics
import random 
import csv
import webbrowser
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import redlines
import openai
import plotly.express as px
import seaborn as sns
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# %%
dotenv_path = os.path.join('utils', '.env')
load_dotenv(dotenv_path)
openai_api_key = os.getenv('OPENAI_API_KEY')
print(openai_api_key)
openai.api_key = openai_api_key
print("Current Working Directory:", os.getcwd())
files_and_dirs = os.listdir('.')
print("Files and Directories:", files_and_dirs)


# %% 
#client = openai.OpenAI()

#def get_completion(prompt, model="gpt-3.5-turbo"):
#    messages = [{"role": "user", "content": prompt}]
#    response = client.chat.completions.create(
#        model=model,
#        messages=messages,
#        temperature=0
#    )
#    return response.choices[0].message.content


# %% Step 2: download FDA data

# %% Step 1: download FDA data only if not already present

import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from glob import glob
import shutil

# === Load FDA URLs from file ===
url_file_path = os.path.join("utils", "fda_urls.txt")
fda_urls = {}

with open(url_file_path, "r") as file:
    for line in file:
        line = line.strip()
        if not line or "," not in line:
            continue
        try:
            year_str, url = line.split(",", 1)
            fda_urls[int(year_str)] = url.strip()
        except ValueError:
            print(f"⚠️ Skipping invalid line: {line}")

# === Setup Directories ===
output_dir = os.path.join("data", "fda_data_download")
archive_dir = os.path.join("data", "fda_data_archive")
os.makedirs(output_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)

# === Scraper Config ===
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}
local_tz = pytz.timezone("US/Eastern")

# === Loop through URLs ===
for year, url in fda_urls.items():
    print(f"🔎 Checking year: {year}")

    # Check for existing files
    existing_files = sorted(
        glob(os.path.join(output_dir, f"first-time-gx-approval-{year}-downloaded at-*.csv")),
        reverse=True
    )

    if existing_files:
        print(f"⏩ Skipping download for {year} — latest file exists: {os.path.basename(existing_files[0])}")
        continue

    print(f"🌐 Downloading new data for {year}...")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table")
        if not table:
            print(f"⚠️ No table found for year {year}.")
            continue

        # Parse table into DataFrame
        if table and hasattr(table, "find_all"):
            table_headers = [th.text.strip() for th in table.find_all("th")] # type: ignore
        else:
            print(f"⚠️ Invalid table structure for year {year}.")
            continue
        rows = []
        for tr in table.find_all("tr")[1:]: # type: ignore
            cells = [td.text.strip() for td in tr.find_all("td")] # type: ignore
            if cells:
                rows.append(cells)

        df = pd.DataFrame(rows, columns=table_headers)

        # Timestamp for filename and column
        now = datetime.now(local_tz)
        iso_timestamp = now.isoformat()
        df["download_timestamp_iso"] = iso_timestamp

        # Safe filename formatting
        safe_timestamp = re.sub(r"[:]", "-", iso_timestamp)
        file_name = f"first-time-gx-approval-{year}-downloaded at-{safe_timestamp}.csv"
        output_path = os.path.join(output_dir, file_name)

        # Move old files (if any) to archive
        for old_file in existing_files[1:]:
            archive_path = os.path.join(archive_dir, os.path.basename(old_file))
            shutil.move(old_file, archive_path)
            print(f"📦 Archived old file: {archive_path}")

        # Save new file
        df.to_csv(output_path, index=False)
        print(f"✅ Saved new file: {output_path}")

    except Exception as e:
        print(f"❌ Error processing {year}: {e}")
