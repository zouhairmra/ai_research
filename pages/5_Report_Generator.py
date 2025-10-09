# pages/5_Report_Generator.py
import streamlit as st

def show():
    st.title("📄 Report Generator")

    try:
        from utils import report
    except ModuleNotFoundError:
        st.error("⚠️ Missing dependency: `reportlab`. Please install it with `pip install reportlab`.")
        return

    st.write("Generate your customized economic report here.")
    st.write("Coming soon: dynamic PDF report creation with charts and summaries.")
