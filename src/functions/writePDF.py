from weasyprint import HTML

def write_pdf_report(html_content, carrera):
    HTML(string=html_content).write_pdf(f"../output/informe_pdf/Informe_{carrera}.pdf")
