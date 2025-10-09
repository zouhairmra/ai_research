import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(title, summary):
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

def show():
    st.header("Report Generator")
    title = st.text_input("Report title", "EconLab Report")
    summary = st.text_area("Summary / Interpretation")
    if st.button("Generate PDF"):
        pdf = create_pdf(title, summary)
        st.download_button("Download Report", data=pdf, file_name="econlab_report.pdf", mime="application/pdf")
