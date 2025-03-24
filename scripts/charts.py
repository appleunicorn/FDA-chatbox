import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import webbrowser

#%% chart 1: number of anda approvals by year

def plot_anda_approvals_by_year(
    db_path="fda_first_generic_approvals.db",
    table_name="fda_approvals",
    start_year=None,
    end_year=None,
    title="Number of ANDA approvals for first Gx only",
    save_path=None,
    show=True
):
    """
    Creates a bar chart of ANDA approvals by year (from 'year' column), with counts on bars.
    Also optionally saves the plot and opens it in a simple HTML page.
    """

    # Connect to DB
    conn = sqlite3.connect(db_path)

    # If no year range specified, detect from data
    year_range_query = f"SELECT MIN(year), MAX(year) FROM {table_name};"
    min_year, max_year = conn.execute(year_range_query).fetchone()

    start_year = start_year or min_year
    end_year = end_year or max_year

    print(f"📆 Plotting approvals from {start_year} to {end_year}")

    # Query approvals by year
    query = f"""
        SELECT year, COUNT(*) AS approvals
        FROM {table_name}
        WHERE year BETWEEN {start_year} AND {end_year}
        GROUP BY year
        ORDER BY year;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("⚠️ No data found for that year range.")
        return pd.DataFrame()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['year'].astype(str), df['approvals'], color="limegreen")

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1, str(height),
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Number of approvals", fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save and HTML preview
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"✅ Chart saved to {save_path}")

        # Open in browser
        html_path = save_path.replace(".png", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(f"""
            <html>
            <head><title>ANDA Approvals Chart</title></head>
            <body style="text-align: center;">
                <h2>{title}</h2>
                <img src="{os.path.basename(save_path)}" style="max-width:90%;">
            </body>
            </html>
            """)
        webbrowser.open(f"file://{os.path.abspath(html_path)}")
        print(f"🌐 HTML preview opened: {html_path}")

    if show:
        plt.show()

    return df

#%% chart 2: number of anda applicants by year

def plot_applicants_by_year(
    db_path="fda_first_generic_approvals.db",
    table_name="fda_approvals",
    start_year=None,
    end_year=None,
    title="Number of First Generic Applicants by Year",
    save_path=None,
    show=True
):
    """
    Creates a bar chart of unique ANDA applicants by year.
    """

    # Connect to DB
    conn = sqlite3.connect(db_path)

    # Detect year range if not specified
    year_range_query = f"SELECT MIN(year), MAX(year) FROM {table_name};"
    min_year, max_year = conn.execute(year_range_query).fetchone()

    start_year = start_year or min_year
    end_year = end_year or max_year

    print(f"📆 Plotting applicant counts from {start_year} to {end_year}")

    # Query: count of unique applicants by year
    query = f"""
        SELECT year, COUNT(DISTINCT anda_applicant) AS num_applicants
        FROM {table_name}
        WHERE year BETWEEN {start_year} AND {end_year}
        GROUP BY year
        ORDER BY year;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("⚠️ No applicant data found for that year range.")
        return pd.DataFrame()

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(df['year'].astype(str), df['num_applicants'], color="dodgerblue")

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, str(height),
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel("Year", fontsize=12)
    ax.set_ylabel("Number of Unique Applicants", fontsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=0)
    plt.tight_layout()

    # Save and HTML preview
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"✅ Chart saved to {save_path}")

        # HTML viewer
        html_path = save_path.replace(".png", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(f"""
            <html>
            <head><title>{title}</title></head>
            <body style="text-align: center;">
                <h2>{title}</h2>
                <img src="{os.path.basename(save_path)}" style="max-width:90%;">
            </body>
            </html>
            """)
        webbrowser.open(f"file://{os.path.abspath(html_path)}")
        print(f"🌐 HTML preview opened: {html_path}")

    if show:
        plt.show()

    return df


#%% chart 3: generate pie charts for each year



import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os
import webbrowser


def plot_top_20_applicants_pie(
    db_path="fda_first_generic_approvals.db",
    table_name="fda_approvals",
    year=2024,
    top_n=20,
    save_dir="output",
    show=True
):
    """
    Plots a pie chart of top N applicants for a given year.
    Groups the rest as 'Others'. Saves both PNG and HTML versions.
    """

    # Connect to database
    conn = sqlite3.connect(db_path)
    query = f"""
        SELECT anda_applicant, COUNT(*) as approvals
        FROM {table_name}
        WHERE year = ?
        GROUP BY anda_applicant
        ORDER BY approvals DESC;
    """
    df = pd.read_sql(query, conn, params=(year,))
    conn.close()

    if df.empty:
        print(f"⚠️ No data found for year {year}")
        return

    # Separate top N and "Others"
    top_df = df.head(top_n).copy()
    others_total = df["approvals"][top_n:].sum()

    if others_total > 0:
        top_df = pd.concat([
            top_df,
            pd.DataFrame([{"anda_applicant": "Others", "approvals": others_total}])
        ], ignore_index=True)

    total_approvals = top_df["approvals"].sum()

    # Labels with count and percent
    labels = [
        f"{row['anda_applicant']}\n{row['approvals']} ({row['approvals'] / total_approvals:.0%})"
        for _, row in top_df.iterrows()
    ]

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 10))
    wedges, _ = ax.pie(
        top_df["approvals"],
        labels=labels,
        startangle=90,
        textprops={'fontsize': 8},
        wedgeprops={'edgecolor': 'white'}
    )
    ax.set_title(f"Top 20 First Generic Applicants ({year})", fontsize=14, fontweight="bold")
    plt.tight_layout()

    # Save files
    os.makedirs(save_dir, exist_ok=True)
    png_path = os.path.join(save_dir, f"top_20_applicants_{year}_pie.png")
    html_path = png_path.replace(".png", ".html")

    plt.savefig(png_path, dpi=300)
    print(f"✅ Saved pie chart: {png_path}")

    # Generate HTML file
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head><title>Top 20 First Generic Applicants ({year})</title></head>
        <body style="text-align: center;">
            <h2>Top 20 First Generic Applicants ({year})</h2>
            <img src="{os.path.basename(png_path)}" style="max-width:90%;">
        </body>
        </html>
        """)
    print(f"🌐 Opening HTML preview: {html_path}")
    webbrowser.open(f"file://{os.path.abspath(html_path)}")

    if show:
        plt.show()




#%% chart 4: top 20 applicants for range of years

def plot_top_20_applicants_pie_range(
    start_year,
    end_year,
    db_path="fda_first_generic_approvals.db",
    table_name="fda_approvals",
    top_n=20,
    save_dir="output",
    show=True
):
    """
    Plots a pie chart for the top N applicants across a range of years.
    Groups the rest as 'Others'.
    """
    conn = sqlite3.connect(db_path)

    # Query total approvals across range
    query = f"""
        SELECT anda_applicant, COUNT(*) AS approvals
        FROM {table_name}
        WHERE year BETWEEN ? AND ?
        GROUP BY anda_applicant
        ORDER BY approvals DESC;
    """
    df = pd.read_sql(query, conn, params=(start_year, end_year))
    conn.close()

    if df.empty:
        print(f"⚠️ No data found for {start_year}–{end_year}")
        return

    # Top N + "Others"
    top_df = df.head(top_n).copy()
    others_sum = df["approvals"][top_n:].sum()
    if others_sum > 0:
        top_df = pd.concat([
            top_df,
            pd.DataFrame([{"anda_applicant": "Others", "approvals": others_sum}])
        ], ignore_index=True)

    total = top_df["approvals"].sum()

    # Labels: Name + Count + Percent
    labels = [
        f"{row['anda_applicant']}\n{row['approvals']} ({row['approvals'] / total:.0%})"
        for _, row in top_df.iterrows()
    ]

    # Title and paths
    year_label = f"{start_year}-{end_year}"
    title = f"Top {top_n} First Generic Applicants ({year_label})"
    os.makedirs(save_dir, exist_ok=True)
    png_path = os.path.join(save_dir, f"top_applicants_{year_label}_pie.png")
    html_path = png_path.replace(".png", ".html")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    wedges, _ = ax.pie(
        top_df["approvals"],
        labels=labels,
        startangle=90,
        textprops={'fontsize': 8},
        wedgeprops={'edgecolor': 'white'}
    )
    ax.set_title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()

    # Save
    plt.savefig(png_path, dpi=300)
    print(f"✅ Saved pie chart: {png_path}")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f"""
        <html>
        <head><title>{title}</title></head>
        <body style="text-align: center;">
            <h2>{title}</h2>
            <img src="{os.path.basename(png_path)}" style="max-width:90%;">
        </body>
        </html>
        """)
    print(f"🌐 Opened HTML preview: {html_path}")
    webbrowser.open(f"file://{os.path.abspath(html_path)}")

    if show:
        plt.show()

    return top_df



#%% Finally: generate combined html report


import webbrowser

def generate_combined_html_report(title, chart_paths, output_path="output/fda_combined_charts.html"):
    """
    Generates an HTML page that includes multiple PNG charts on one page.

    Args:
        title (str): Title of the report page.
        chart_paths (list): List of image file paths.
        output_path (str): Output HTML file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Generate HTML body with all images
    images_html = "\n".join(
        f'<div style="margin:20px;"><img src="{os.path.basename(p)}" style="max-width:90%;"></div>'
        for p in chart_paths
    )

    html = f"""
    <html>
    <head>
        <title>{title}</title>
    </head>
    <body style="text-align: center;">
        <h1>{title}</h1>
        {images_html}
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open(f"file://{os.path.abspath(output_path)}")
    print(f"🌐 Combined HTML report opened: {output_path}")

