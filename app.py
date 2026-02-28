import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from flask import Flask, render_template, request
import seaborn as sns
from io import BytesIO
import base64
from werkzeug.utils import secure_filename

# Use Agg backend for thread safety in web apps (disables GUI features)
matplotlib.use('Agg')

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    stats = None
    plot_url = None
    filename = None
    error = None

    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            try:
                # Read file directly from memory without saving to disk
                if filename.lower().endswith((".xlsx", ".xls")):
                    df = pd.read_excel(file)
                elif filename.lower().endswith(".csv"):
                    df = pd.read_csv(file)
                else:
                    error = "Unsupported file type. Please upload a CSV or Excel file."
                    return render_template("index.html", error=error)
                
                # Standardize columns by stripping whitespace
                df.columns = [str(col).strip() for col in df.columns]
                
                if "Date" in df.columns and "Sales" in df.columns:
                    # Clean data and drop NA values to prevent parsing and plotting errors
                    df = df.dropna(subset=["Date", "Sales"])
                    
                    # Convert Date to datetime, coercing errors to NaT, then drop those
                    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
                    df = df.dropna(subset=["Date"])
                    
                    # Convert Sales to numeric, coercing errors to NaN, then drop those
                    df["Sales"] = pd.to_numeric(df["Sales"], errors='coerce')
                    df = df.dropna(subset=["Sales"])
                    
                    if df.empty:
                        error = "File contains no valid matching rows for 'Date' and 'Sales'."
                        return render_template("index.html", error=error)

                    df = df.sort_values(by="Date")

                    stats = df.describe().to_html(classes="table table-bordered table-hover table-striped")

                    # Use object-oriented figure and axis for concurrency safety
                    fig, ax = plt.subplots(figsize=(12, 6))
                    sns.lineplot(x=df["Date"], y=df["Sales"], marker="o", linestyle="-", color="b", markersize=4, alpha=0.7, ax=ax)

                    ax.set_xlabel("Date", fontsize=12)
                    ax.set_ylabel("Sales", fontsize=12)
                    ax.set_title("📊 Sales Trend Over Time", fontsize=14, fontweight="bold")
                    ax.tick_params(axis='x', rotation=45, labelsize=10)
                    ax.tick_params(axis='y', labelsize=10)
                    ax.grid(True, linestyle="--", alpha=0.6)

                    # Dynamic date locator based on the range of dates to avoid crowded x-axis
                    date_range = (df["Date"].max() - df["Date"].min()).days
                    if date_range > 365 * 2:
                        ax.xaxis.set_major_locator(mdates.YearLocator())
                        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
                    elif date_range > 180:
                        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
                        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
                    elif date_range > 60:
                        ax.xaxis.set_major_locator(mdates.MonthLocator())
                        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
                    else:
                        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, date_range//10)))
                        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

                    # Save plot to in-memory bytes buffer
                    img = BytesIO()
                    fig.savefig(img, format="png", bbox_inches="tight")
                    img.seek(0)
                    plt.close(fig)
                    
                    # Convert image bytes to Base64 for inline HTML rendering
                    plot_data = base64.b64encode(img.getvalue()).decode("utf8")
                    plot_url = f"data:image/png;base64,{plot_data}"

                else:
                    error = "File must contain both 'Date' and 'Sales' columns."
            except Exception as e:
                error = f"Error processing file: {str(e)}"

    return render_template("index.html", stats=stats, plot_url=plot_url, filename=filename, error=error)

if __name__ == "__main__":
    app.run(debug=True)
