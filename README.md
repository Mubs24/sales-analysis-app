# 📊 Sales Analyst Portfolio Project

This is a portfolio project demonstrating data cleaning, visualization, and Flask web deployment. It takes uploaded sales datasets (CSV/Excel) and processes them into analytical insights and visual trends.

## ✨ Features

- **Data Processing:** Cleans uploaded data using `pandas`, handling missing values and invalid types.
- **Data Visualization:** Employs `matplotlib` and `seaborn` to render clear line plots showing sales trends over time.
- **Modular Code Base:** Code is structurally isolated into specific domains (cleaning, routing, visualization).
- **Exporting Options:** Generate and download summarized `.txt` insights straight from the Flask backend, along with PDF and CSV exports.

## 🚀 How to Run (Exact Commands)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mubs24/sales-analysis-app.git
   cd sales-analysis-app
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   # Enable development mode (optional) to see debug logs
   # export FLASK_ENV=development 
   python app.py
   ```

5. **Open your browser:** Navigate to `http://127.0.0.1:5000`

## 📁 Required Data Format
For the app to successfully generate a chart, your CSV or Excel file **must** contain exactly:
- `Date` (e.g., "2024-01-01")
- `Sales` (e.g., 1500 or 1500.50)

> Don't have a dataset? You can click "Download sample.csv" directly on the web app to trigger the dynamic sample generation route.

## 🛠 Project Structure
- `app.py`: Flask framework routing logic and controller.
- `data_processing.py`: Module for reading, cleaning, and validating data.
- `plotting.py`: Module for generating analytical graphics using Matplotlib.
- `pdf_generator.py`: Generates the downloadable PDF summary reports using FPDF2.

## 🔒 Security Considerations & Technical Notes
As a portfolio project, this application is designed to demonstrate data manipulation and web serving capabilities. It requires configuration before any real production deployment:
- **File Validation:** Files are verified for `.csv` or `.xlsx` extension signatures before parsing. 
- **Temporary Files (PDF Generation):** While data processing and CSV/TXT exports happen statelessly via in-memory `BytesIO` buffers, the PDF generation module uses Python's `tempfile.NamedTemporaryFile` to securely and ephemerally write bytes to disk before deleting them, due to native FPDF2 constraints.
- **CSRF Protection:** There is currently no cross-site request forgery safeguard applied to the interface forms. 
- **Debug Mode:** By default, Flask's debug mode is disabled based on the environment flag. It should remain disabled in deployment environments to prevent stack trace disclosures.
