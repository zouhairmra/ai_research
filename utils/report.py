from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(title: str, summary: str):
    """
    Create a simple PDF report with title and summary.
    Returns PDF as bytes object.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(72, 720, title)
    text_obj = c.beginText(72, 700)
    text_obj.textLines(summary)
    c.drawText(text_obj)
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

