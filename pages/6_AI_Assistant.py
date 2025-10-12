import streamlit as st
import requests
import json
import time
import pandas as pd

# ==========================
# OPTIONAL LIBRARIES
# ==========================
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None
    st.warning("⚠️ PyPDF2 not found. PDF upload disabled.")

try:
    from docx import Document
except ImportError:
    Document = None
    st.warning("⚠️ python-docx not found. Word file upload disabled.")

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    st.warning("⚠️ matplotlib not found. Plotting disabled.")

try:
    import seaborn as sns
except ImportError:
    sns = None
    st.warning("⚠️ seaborn not found. Advanced plotting disabled.")

try:
    import statsmodels.api as sm
except ImportError:
    sm = None
    st.warning("⚠️ statsmodels not found. Regression analysis unavailable.")

# ==========================
# PAGE SETUP
# ==========================
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
st.title("🤖 EconLab — AI Assistant")
st.write("Ask anything about economics, econometrics, or data analysis — or upload a file for AI-powered insights.")

# ==========================
# POE API CONFIG
# ==========================
POE_API_URL = "https://api.poe.com/v1/chat/completions"
POE_API_KEY = st.secrets.get("POE_API_KEY", "YOUR_POE_API_KEY_HERE")
MODEL = st.selectbox("Select model", ["maztouriabot", "gpt-4o-mini", "claude-3-haiku"])

# ==========================
# FILE UPLOAD
# ==========================
st.markdown("### 📂 Upload a file for AI analysis")
uploaded_file = st.file_uploader("Upload PDF, CSV, or Word", type=["pdf", "csv", "docx"])
uploaded_text = ""
df = None

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    
    # PDF
    if file_ext == "pdf" and PdfReader:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            uploaded_text += page.extract_text() or ""
        st.success("✅ PDF text extracted.")
    
    # Word
    elif file_ext == "docx" and Document:
        doc = Document(uploaded_file)
        uploaded_text = "\n".join([p.text for p in doc.paragraphs])
        st.success("✅ Word text extracted.")
    
    # CSV
    elif file_ext == "csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        uploaded_text = df.to_string(index=False)
        st.success("✅ CSV data loaded.")

    with st.expander("📜 Preview Extracted Text"):
        st.text(uploaded_text[:2000] + ("..." if len(uploaded_text) > 2000 else ""))

# ==========================
# AUTOMATIC DATA INSIGHTS
# ==========================
if df is not None:
    st.markdown("### 📊 Suggested Data Insights")
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    
    if numeric_cols:
        st.markdown(f"Detected numeric columns: {', '.join(numeric_cols)}")

        # Auto pairplot
        if sns and plt:
            st.write("Generating auto pairplot...")
            fig = sns.pairplot(df[numeric_cols])
            st.pyplot(fig)

        # Auto regression suggestion
        if sm and len(numeric_cols) >= 2:
            st.write("You can run regression analysis on numeric columns.")
            y_col = st.selectbox("Select dependent variable", numeric_cols)
            X_cols = st.multiselect("Select independent variables", [c for c in numeric_cols if c != y_col])
            if X_cols:
                X = sm.add_constant(df[X_cols])
                y = df[y_col]
                model = sm.OLS(y, X).fit()
                st.write(model.summary())

# ==========================
# CHAT MEMORY
# ==========================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================
# USER INPUT
# ==========================
default_prompt = "Summarize the uploaded document." if uploaded_text else ""
user_input = st.chat_input("Type your question or ask about your uploaded file...") or default_prompt

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("_
