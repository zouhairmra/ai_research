import streamlit as st
import requests
import json
import time
import pandas as pd
from io import StringIO

# Safe imports
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

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
    st.warning("⚠️ matplotlib not installed. Plotting disabled.")

try:
    import seaborn as sns
except ImportError:
    sns = None
    st.warning("⚠️ seaborn not installed. Advanced plotting disabled.")

try:
    import statsmodels.api as sm
except ImportError:
    sm = None
    st.warning("⚠️ statsmodels not installed. Regression analysis unavailable.")

# ==========================
# PAGE SETUP
# ==========================
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
st.title("🤖 EconLab — AI Assistant")
st.write("Ask anything about economics, econometrics, or data analysis — or upload a file for AI insights.")

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
uploaded_file = st.file_uploader("Upload PDF, CSV, or Word file", type=["pdf", "csv", "docx"])

uploaded_text = ""
df = None

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    # PDF
    if file_type == "pdf" and PdfReader:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            uploaded_text += page.extract_text() or ""
        st.success("✅ PDF text extracted successfully.")

    # CSV
    elif file_type == "csv":
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        uploaded_text = df.to_string(index=False)
        st.success("✅ CSV data extracted successfully.")

    # DOCX
    elif file_type == "docx" and Document:
        doc = Document(uploaded_file)
        uploaded_text = "\n".join([para.text for para in doc.paragraphs])
        st.success("✅ Word text extracted successfully.")

    # Show text preview
    with st.expander("📜 Preview Extracted Text"):
        st.text(uploaded_text[:2000] + ("..." if len(uploaded_text) > 2000 else ""))

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

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            headers = {
                "Authorization": f"Bearer {POE_API_KEY}",
                "Content-Type": "application/json"
            }

            # Combine file content with user query
            content = f"File content:\n{uploaded_text[:4000]}\n\nQuestion: {user_input}" if uploaded_text else user_input

            payload = {
                "model": MODEL,
                "messages": [{"role": "user", "content": content}]
            }

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
# REGRESSION ANALYSIS (if CSV and statsmodels available)
# ==========================
if df is not None and sm:
    st.markdown("### 📊 Regression Analysis")
    try:
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) >= 2:
            X = df[numeric_cols[:-1]]
            y = df[numeric_cols[-1]]
            X = sm.add_constant(X)
            model = sm.OLS(y, X).fit()
            st.write(model.summary())
        else:
            st.info("Not enough numeric columns for regression.")
    except Exception as e:
        st.error(f"Regression error: {e}")

# ==========================
# PLOTTING (if matplotlib/seaborn)
# ==========================
if df is not None and plt and sns:
    st.markdown("### 📈 Plot Data")
    try:
        numeric_cols = df.select_dtypes(include='number').columns
        if len(numeric_cols) >= 2:
            fig, ax = plt.subplots()
            sns.pairplot(df[numeric_cols])
            st.pyplot(fig)
        else:
            st.info("Not enough numeric columns to plot.")
    except Exception as e:
        st.error(f"Plotting error: {e}")

# ==========================
# EXPORT CHAT
# ==========================
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 2])

if col1.button("🧹 Clear Chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared!")

if col2.button("💾 Export Chat"):
    if st.session_state["messages"]:
        chat_data = pd.DataFrame(st.session_state["messages"])
        csv = chat_data.to_csv(index=False)
        st.download_button(
            label="Download Chat CSV",
            data=csv,
            file_name="econlab_chat.csv",
            mime="text/csv"
        )
    else:
        st.warning("No chat to export!")

# ==========================
# FOOTER
# ==========================
st.markdown("---")
st.caption("💡 EconLab AI Assistant — Powered by Poe API and Streamlit.")
