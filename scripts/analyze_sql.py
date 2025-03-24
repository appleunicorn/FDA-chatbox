from charts import (
    plot_anda_approvals_by_year,
    plot_applicants_by_year,
    plot_top_20_applicants_pie,
    plot_top_20_applicants_pie_range,
    generate_combined_html_report
)


# === Generate individual charts ===
chart1_path = "output/anda_approvals_by_year.png"
chart2_path = "output/unique_applicants_by_year.png"
chart3_path = "output/top_applicants_2024_pie.png"


# === Generate combined HTML report ===
generate_combined_html_report(
    title="FDA First Generic Approvals Summary",
    chart_paths=[chart1_path, chart2_path, chart3_path],
    output_path="output/fda_combined_charts.html"
)


