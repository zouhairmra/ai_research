import streamlit as st
from utils import report

def show():
    st.header("Report Generator")
    title = st.text_input("Report title", "EconLab Report")
    summary = st.text_area("Summary / Interpretation")
    if st.button("Generate PDF"):
        pdf = report.create_pdf(title, summary)
        st.download_button("Download Report", data=pdf, file_name="econlab_report.pdf", mime="application/pdf")
