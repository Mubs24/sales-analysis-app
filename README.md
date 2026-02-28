# 📊 Sales Analysis App

A lightweight, robust, secure, and intuitive Flask web application for uploading and analyzing sales data. 

This app allows you to upload **Excel (`.xlsx`, `.xls`)** or **CSV** files containing your sales transactions and instantly generates detailed statistical summaries and an interactive line chart.

## ✨ Features

- **Upload Flexibility:** Supports multiple file extensions (CSV, XLSX, XLS).
- **Fast In-Memory Processing:** Uses the `io.BytesIO` module to read, analyze, and render charts without ever writing temporary files to your hard drive. 
- **Production-Ready Thread Safety:** Uses `matplotlib.use('Agg')` and Object-Oriented APIs to ensure multiple users can analyze files concurrently without overlapping or crashing.
- **Robust Error Handling:** Checks for valid file types and data structures. If a file is missing the `Date` or `Sales` columns, an error message is safely fed back directly to the Web UI instead of crashing the server.
- **Dynamic Chart Timeframes:** Intelligently scales X-axis dates depending on if the data represents days, months, or years.
- **Export Data:** Securely export generated statistics from the dashboard context as `.txt`.

## 🚀 Quick Start

Ensure you have Python 3 installed.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mubs24/sales-analysis-app.git
   cd sales-analysis-app
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```

4. **Open your browser:** Navigate to `http://127.0.0.1:5000` to interact with the app.

## 📁 Required Data Format
For the app to successfully generate a chart, your CSV or Excel file **must** contain the following exact column names (case-sensitive):
- `Date` (e.g., "2024-01-01")
- `Sales` (e.g., 1500 or 1500.50)

Any empty rows or malformed dates/sales entries will be safely dropped during processing.

## 🛠 Tech Stack
- **Backend:** Python, Flask, Werkzeug
- **Data processing:** Pandas
- **Visualization:** Matplotlib, Seaborn
- **Frontend Design:** Vanilla HTML, Bootstrap 5
