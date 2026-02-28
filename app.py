import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from data_processing import process_data, calculate_kpis, generate_breakdowns, get_csv_b64
from plotting import generate_trend_plot
from pdf_generator import generate_pdf_b64

# Initialize Flask app
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            
            # 1. Process and Clean Data
            df, error = process_data(file, filename)
            if error:
                return render_template("index.html", error=error)
            
            # 2. Extract Analytics
            kpis = calculate_kpis(df)
            breakdowns = generate_breakdowns(df)
            
            # 3. Generate Visualizations
            plot_url = generate_trend_plot(df)
            
            # 4. Generate Export Payloads (Memory-Only)
            csv_b64 = get_csv_b64(df)
            pdf_b64 = generate_pdf_b64(kpis, plot_url, breakdowns, filename)

            # 5. Extract a quick sample view for the UI
            data_sample = df.tail(8).to_html(classes="table table-sm table-striped table-hover", index=False)

            return render_template(
                "index.html",
                filename=filename,
                kpis=kpis,
                breakdowns=breakdowns,
                plot_url=plot_url,
                data_sample=data_sample,
                csv_b64=csv_b64,
                pdf_b64=pdf_b64
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
