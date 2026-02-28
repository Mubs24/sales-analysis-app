import os
from io import BytesIO
import base64
from flask import Flask, render_template, request, Response
from werkzeug.utils import secure_filename

from data_processing import (
    process_data,
    calculate_kpis,
    generate_breakdowns,
    get_csv_b64,
)
from plotting import generate_trend_plot
from pdf_generator import generate_pdf_b64

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("file")
        if file and file.filename != "":
            filename = secure_filename(file.filename)

            df, error = process_data(file, filename)
            if error:
                return render_template("index.html", error=error)

            kpis = calculate_kpis(df)
            breakdowns = generate_breakdowns(df)
            plot_url = generate_trend_plot(df)

            csv_b64 = get_csv_b64(df)
            pdf_b64 = generate_pdf_b64(kpis, plot_url, breakdowns, filename)

            data_sample = df.tail(8).to_html(
                classes="table table-sm table-striped table-hover", index=False
            )
            stats_txt = df.describe().to_string()
            total_revenue = kpis.get("total_sales", "$0.00")
            num_records = len(df)

            return render_template(
                "index.html",
                filename=filename,
                kpis=kpis,
                breakdowns=breakdowns,
                plot_url=plot_url,
                data_sample=data_sample,
                csv_b64=csv_b64,
                pdf_b64=pdf_b64,
                stats_txt=stats_txt,
                total_revenue=total_revenue,
                num_records=num_records,
            )

    return render_template("index.html")


@app.route("/export", methods=["POST"])
def export():
    """
    Export detailed report as a .txt file entirely via an in-memory buffer.
    """
    summary = request.form.get("summary_txt", "No statistics available.")
    total_revenue = request.form.get("total_revenue", "0.00")
    num_records = request.form.get("num_records", "0")

    content = f"Sales Data Dashboard Summary\n{'=' * 30}\n\n"
    content += f"Total Revenue: {total_revenue}\n"
    content += f"Number of Records: {num_records}\n\n"
    content += f"Summary Statistics Analysis:\n{summary}\n"

    buffer = BytesIO()
    buffer.write(content.encode("utf-8"))
    buffer.seek(0)

    return Response(
        buffer,
        mimetype="text/plain",
        headers={"Content-disposition": "attachment; filename=sales_export.txt"},
    )


@app.route("/download_sample", methods=["GET"])
def download_sample():
    """
    Generate a sample CSV dynamically so we don't have to track files.
    """
    sample_csv = (
        "Date,Sales,Product,Region\n"
        "2024-01-01,150.50,Widget A,North\n"
        "2024-01-02,200.00,Widget B,South\n"
        "2024-01-05,250.00,Widget C,East\n"
        "2024-02-10,400.00,Widget A,West\n"
        "2024-03-15,300.00,Widget B,North\n"
    )
    buffer = BytesIO()
    buffer.write(sample_csv.encode("utf-8"))
    buffer.seek(0)

    return Response(
        buffer,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=sample.csv"},
    )


if __name__ == "__main__":
    is_debug = os.environ.get("FLASK_ENV") == "development"
    app.run(debug=is_debug)
