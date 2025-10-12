import streamlit as st
import requests
import json
import time
import pandas as pd
import numpy as np
# Safe import of matplotlib and seaborn
try:
    import matplotlib
    matplotlib.use("Agg")  # Safe backend for Streamlit Cloud
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    st.warning("⚠️ Matplotlib not installed. Plots will be disabled.")

try:
    import seaborn as sns
except ImportError:
    sns = None
    st.warning("⚠️ Seaborn not installed. Advanced plots will be disabled.")
# Optional imports for file processing
try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None
    st.warning("⚠️ PyPDF2 not found. PDF upload will be disabled.")

try:
    from docx import Document
except ImportError:
    Document = None
    st.warning("⚠️ python-docx not found. Word file upload will be disabled.")

# Regression library
try:
    import statsmodels.api as sm
except ImportError:
    sm = None
    st.warning("⚠️ statsmodels not found. Regression analysis disabled.")

# ==========================
# PAGE SETUP
# ==========================
st.set_page_config(page_title="AI Assistant & Data Analyzer", page_icon="🤖", layout="wide")
st.title("🤖 EconLab — AI Assistant & Data Analyzer")
st.write("Ask questions, upload files, or analyze CSV data with AI-powered insights and visualizations.")

# ==========================
# POE API CONFIGURATION
# ==========================
POE_API_URL = "https://api.poe.com/v1/chat/completions"
POE_API_KEY = st.secrets.get("POE_API_KEY", "YOUR_POE_API_KEY_HERE")
MODEL = st.selectbox("Select AI model", ["maztouriabot", "gpt-4o-mini", "claude-3-haiku"])

# ==========================
# FILE UPLOAD & ANALYSIS
# ==========================
st.markdown("### 📂 Upload a file (CSV, PDF, or Word)")
uploaded_file = st.file_uploader("Choose a file", type=["csv", "pdf", "docx"])
uploaded_text = ""
df = None

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        uploaded_text = df.to_string(index=False)
        st.success("✅ CSV loaded successfully.")

    elif file_type == "pdf" and PdfReader:
        reader = PdfReader(uploaded_file)
        uploaded_text = "".join([page.extract_text() or "" for page in reader.pages])
        st.success("✅ PDF text extracted successfully.")

    elif file_type == "docx" and Document:
        doc = Document(uploaded_file)
        uploaded_text = "\n".join([para.text for para in doc.paragraphs])
        st.success("✅ Word text extracted successfully.")

    if uploaded_text:
        with st.expander("📜 Preview Extracted Text"):
            st.text(uploaded_text[:2000] + ("..." if len(uploaded_text) > 2000 else ""))

# ==========================
# CSV ANALYSIS OPTIONS
# ==========================
if df is not None:
    st.markdown("### 📊 CSV Data Analysis Options")
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols and sm:
        x_col = st.selectbox("Select independent variable (X)", numeric_cols)
        y_col = st.selectbox("Select dependent variable (Y)", numeric_cols)
        if st.button("Run Linear Regression & Plot"):
            X = sm.add_constant(df[x_col])
            y = df[y_col]
            model = sm.OLS(y, X).fit()
            st.write(model.summary())

            # Plot scatter + regression line
            fig, ax = plt.subplots()
            sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax)
            ax.plot(df[x_col], model.predict(X), color='red')
            ax.set_title(f"{y_col} vs {x_col} Regression")
            st.pyplot(fig)
    elif not numeric_cols:
        st.info("No numeric columns found in CSV for regression.")
    else:
        st.info("Statsmodels not installed. Regression analysis unavailable.")

# ==========================
# CHAT MEMORY
# ==========================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==========================
# USER INPUT & AI QUERY
# ==========================
default_prompt = "Summarize the uploaded document." if uploaded_text else ""
user_input = st.chat_input("Ask AI anything or about your uploaded file...") or default_prompt

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            headers = {
                "Authorization": f"Bearer {POE_API_KEY}",
                "Content-Type": "application/json"
            }

            content = f"File content:\n{uploaded_text[:4000]}\n\nQuestion: {user_input}" if uploaded_text else user_input

            payload = {"model": MODEL, "messages": [{"role": "user", "content": content}]}
            res = requests.post(POE_API_URL, headers=headers, json=payload, timeout=60)
            res.raise_for_status()
            data = res.json()
            response_text = data["choices"][0]["message"]["content"]

            # Typing animation
            for token in response_text.split():
                full_response += token + " "
                placeholder.markdown(full_response + "▌")
                time.sleep(0.03)
            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Error fetching response: {e}")
            full_response = f"Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# ==========================
# EXPORT CHAT
# ==========================
st.markdown("---")
col1, col2 = st.columns([1, 1])

if col1.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared!")

if col2.button("💾 Export Chat"):
    if st.session_state["messages"]:
        chat_data = pd.DataFrame(st.session_state["messages"])
        csv = chat_data.to_csv(index=False)
        st.download_button("Download Chat CSV", csv, file_name="econlab_chat.csv", mime="text/csv")
    else:
        st.warning("No chat to export!")

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("💡 EconLab AI Assistant & Data Analyzer — Powered by Poe API and Streamlit.")
