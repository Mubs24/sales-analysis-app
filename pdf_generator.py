from fpdf import FPDF
import base64
import tempfile
import os

def generate_pdf_b64(kpis, plot_b64, breakdowns, filename):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Helvetica", 'B', 20)
    pdf.cell(0, 15, text=f"Sales Analysis Report", align='C')
    pdf.ln(10)
    pdf.set_font("Helvetica", 'I', 12)
    pdf.cell(0, 10, text=f"Generated from: {filename}", align='C')
    pdf.ln(15)
    
    # KPIs
    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, text="Key Performance Indicators (KPIs)")
    pdf.ln(10)
    pdf.set_font("Helvetica", '', 12)
    
    kpi_lines = [
        f"Total Sales: {kpis.get('total_sales', '')}",
        f"Average Daily Sales: {kpis.get('avg_daily', '')}",
        f"Best Month: {kpis.get('best_month', '')}",
        f"Recent Growth: {kpis.get('growth', '')}"
    ]
    
    for line in kpi_lines:
        pdf.cell(0, 8, text=line)
        pdf.ln(8)
    pdf.ln(10)
    
    # Render Image from b64
    if plot_b64:
        # Extract pure base64 string
        img_data = base64.b64decode(plot_b64.split(",")[1])
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_img:
            temp_img.write(img_data)
            temp_img_path = temp_img.name
            
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, text="Sales Trend")
        pdf.ln(10)
        # Add image. Adjust width to fit nicely (A4 width is 210mm, minus margins ~190)
        pdf.image(temp_img_path, w=180)
        os.remove(temp_img_path)
        pdf.ln(10)

    # Breakdowns
    if breakdowns:
        pdf.add_page("P") # Added new page for break downs if present
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, text="Data Breakdowns")
        pdf.ln(10)
        
        for key, records in breakdowns.items():
            pdf.set_font("Helvetica", 'B', 12)
            pdf.cell(0, 10, text=f"Top {key.capitalize()}:")
            pdf.ln(8)
            pdf.set_font("Helvetica", '', 11)
            
            # Show top 10 max
            for rec in records[:10]:
                name = rec.get(key.capitalize(), 'Unknown')
                val = rec.get('Sales', '$0.00')
                pdf.cell(0, 8, text=f"  - {name}: {val}")
                pdf.ln(6)
            pdf.ln(5)

    # Output to b64 securely via temp file to avoid byte encoding issues on different python/fpdf versions
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
        temp_pdf_path = temp_pdf.name
        
    pdf.output(temp_pdf_path)
    
    with open(temp_pdf_path, 'rb') as f:
        pdf_bytes = f.read()
        
    os.remove(temp_pdf_path)
    return base64.b64encode(pdf_bytes).decode('utf-8')
