import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from flask import Flask, render_template, request
import seaborn as sns

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PLOTS_FOLDER = "static/plots"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOTS_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    stats = None
    plot_url = None
    filename = None

    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            df = pd.read_excel(file_path) if filename.endswith(".xlsx") else pd.read_csv(file_path)
            df.columns = [col.strip() for col in df.columns]

            if "Date" in df.columns and "Sales" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"])
                df = df.sort_values(by="Date")

                stats = df.describe().to_html(classes="table table-bordered table-hover table-striped")

                plt.figure(figsize=(12, 6))
                sns.lineplot(x=df["Date"], y=df["Sales"], marker="o", linestyle="-", color="b", markersize=4, alpha=0.7)

                plt.xlabel("Date", fontsize=12)
                plt.ylabel("Sales", fontsize=12)
                plt.title("📊 Sales Trend Over Time", fontsize=14, fontweight="bold")
                plt.xticks(rotation=45, fontsize=10)
                plt.yticks(fontsize=10)
                plt.grid(True, linestyle="--", alpha=0.6)

                plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
                plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

                plot_path = os.path.join(PLOTS_FOLDER, "sales_trend.png")
                plt.savefig(plot_path, bbox_inches="tight")
                plt.close()
                
                plot_url = "/static/plots/sales_trend.png"

    return render_template("index.html", stats=stats, plot_url=plot_url, filename=filename)

if __name__ == "__main__":
    app.run(debug=True)
