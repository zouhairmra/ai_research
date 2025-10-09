import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas




def create_pdf_report(title: str, summary_text: str) -> bytes:
buffer = BytesIO()
c = canvas.Canvas(buffer, pagesize=letter)
c.setFont("Helvetica", 12)
c.drawString(72, 720, title)
text_obj = c.beginText(72, 700)
text_obj.textLines(summary_text)
c.drawText(text_obj)
c.showPage()
c.save()
buffer.seek(0)
return buffer.read()




def show():
st.header("Report Generator")
st.write("Create a simple PDF report from text and analysis outputs.")


title = st.text_input("Report title", value="EconLab Report")
summary = st.text_area("Summary / Interpretation")


if st.button("Generate PDF"):
pdf_bytes = create_pdf_report(title, summary)
st.download_button("Download Report", data=pdf_bytes, file_name="econlab_report.pdf", mime="application/pdf")
