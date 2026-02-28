import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from io import BytesIO
import base64

matplotlib.use('Agg')

def generate_trend_plot(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Aggregate sales by date in case there are multiple entries per day
    daily_df = df.groupby("Date")["Sales"].sum().reset_index()
    
    sns.lineplot(x=daily_df["Date"], y=daily_df["Sales"], marker="o", linestyle="-", color="#0d6efd", markersize=6, alpha=0.8, ax=ax, linewidth=2)

    ax.set_xlabel("Date", fontsize=11, fontweight='bold', color='#495057')
    ax.set_ylabel("Sales ($)", fontsize=11, fontweight='bold', color='#495057')
    ax.set_title("Sales Trend Over Time", fontsize=14, fontweight="bold", pad=15, color='#212529')
    
    ax.tick_params(axis='x', rotation=45, labelsize=9)
    ax.tick_params(axis='y', labelsize=9)
    
    ax.grid(True, linestyle="--", alpha=0.3, color='#adb5bd')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    date_range = (daily_df["Date"].max() - daily_df["Date"].min()).days
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

    # Add fill under the line for a modern look
    ax.fill_between(daily_df["Date"], daily_df["Sales"], alpha=0.1, color="#0d6efd")

    img = BytesIO()
    fig.savefig(img, format="png", bbox_inches="tight", dpi=150)
    img.seek(0)
    plt.close(fig)
    
    plot_data = base64.b64encode(img.getvalue()).decode("utf8")
    return f"data:image/png;base64,{plot_data}"
