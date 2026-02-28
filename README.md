# 📊 Sales Analyst Pro

An analyst-grade, lightweight, and professional Flask web application for uploading and analyzing sales data. 

This app allows you to upload **Excel (`.xlsx`, `.xls`)** or **CSV** files containing your sales transactions and instantly generates an interactive dashboard with Key Performance Indicators (KPIs), performance breakdowns, and dynamic line charts.

## ✨ Features

- **Professional KPI Dashboard:** Automatically calculates Total Sales, Average Daily Sales, Best Month, and Month-over-Month Growth.
- **Data Breakdowns:** Automatically calculates and displays top-selling Products and highest-grossing Regions if columns are present.
- **Export Reports:** Download an auto-generated, ready-to-print **PDF Summary Report** or a cleansed and validated **CSV file** directly from the dashboard!
- **Fast & Secure In-Memory Processing:** Uses advanced BytesIO streams to read, analyze, and render charts or generate PDF reports without ever writing temporary files to your hard drive. 
- **Production-Ready Thread Safety:** Uses `matplotlib.use('Agg')` and modularized Object-Oriented APIs to ensure concurrency.

## 🚀 How to Run (Exact Commands)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mubs24/sales-analysis-app.git
   cd sales-analysis-app
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the exact pinned dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```

5. **Open your browser:** Navigate to `http://127.0.0.1:5000` to interact with the app.

## 📁 Required Data Format
For the app to successfully generate a chart, your CSV or Excel file **must** contain the following exact column names (case-sensitive):
- `Date` (e.g., "2024-01-01")
- `Sales` (e.g., 1500 or 1500.50)

*Optional but recommended columns for breakdowns:*
- `Product` (e.g., "Widget A")
- `Region` (e.g., "North")

> **Don't have a dataset?** You can download a perfectly formatted test file directly from the app's homepage (`sample.csv`).

## 🛠 Project Structure
To maintain professional code quality, the application logic is split into dedicated modules:

- `app.py`: The Flask wiring and routing controller.
- `data_processing.py`: Handles all data cleaning, validation, and KPI/breakdown calculations.
- `plotting.py`: Generates the Matplotlib and Seaborn visualization charts.
- `pdf_generator.py`: Generates the downloadable PDF summary reports using FPDF2.
- `requirements.txt`: Strictly pinned package versions for perfect reproducibility.
