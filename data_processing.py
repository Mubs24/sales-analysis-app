import pandas as pd
import base64
from io import BytesIO


def process_data(file, filename):
    try:
        if filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(file)
        elif filename.lower().endswith(".csv"):
            df = pd.read_csv(file)
        else:
            return None, "Unsupported file type. Please upload a CSV or Excel file."

        df.columns = [str(col).strip() for col in df.columns]

        if "Date" not in df.columns or "Sales" not in df.columns:
            return None, "File must contain both 'Date' and 'Sales' columns."

        df = df.dropna(subset=["Date", "Sales"])
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
        df = df.dropna(subset=["Sales"])

        if df.empty:
            return None, "File contains no valid matching rows after cleaning."

        df = df.sort_values(by="Date")
        return df, None

    except Exception as e:
        return None, f"Error processing file: {str(e)}"


def calculate_kpis(df):
    total_sales = df["Sales"].sum()
    days = df["Date"].nunique()
    avg_daily = total_sales / days if days > 0 else 0

    df_month = df.copy()
    df_month["Month"] = df_month["Date"].dt.to_period("M")
    monthly_sales = df_month.groupby("Month")["Sales"].sum()
    best_month = (
        monthly_sales.idxmax().strftime("%B %Y") if not monthly_sales.empty else "N/A"
    )

    if len(monthly_sales) >= 2:
        last_month = monthly_sales.iloc[-1]
        prev_month = monthly_sales.iloc[-2]
        growth = ((last_month - prev_month) / prev_month * 100) if prev_month > 0 else 0
        growth_str = f"{growth:+.1f}%"
    else:
        growth_str = "N/A"

    return {
        "total_sales": f"${total_sales:,.2f}",
        "avg_daily": f"${avg_daily:,.2f}",
        "best_month": best_month,
        "growth": growth_str,
    }


def generate_breakdowns(df):
    breakdowns = {}

    if "Product" in df.columns:
        product_sales = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        product_sales["Sales"] = product_sales["Sales"].map("${:,.2f}".format)
        breakdowns["product"] = product_sales.to_dict("records")

    if "Region" in df.columns:
        region_sales = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )
        region_sales["Sales"] = region_sales["Sales"].map("${:,.2f}".format)
        breakdowns["region"] = region_sales.to_dict("records")

    return breakdowns


def get_csv_b64(df):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return base64.b64encode(csv_buffer.getvalue()).decode("utf-8")
