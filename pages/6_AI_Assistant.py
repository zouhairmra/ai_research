import streamlit as st
import pandas as pd
import openai
import io
from PyPDF2 import PdfReader
from docx import Document

st.title("AI Tools – Smart File Analyzer")

st.write("Upload a PDF, CSV, or Word file and let the AI extract insights or summarize it.")

# === File upload ===
uploaded_file = st.file_uploader("Upload your file", type=["pdf", "csv", "docx"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1].lower()

    if file_type == "pdf":
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        st.success("✅ PDF loaded successfully.")
    
    elif file_type == "csv":
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV loaded successfully.")
        st.dataframe(df.head())
        text = df.to_string(index=False)
    
    elif file_type == "docx":
        doc = Document(uploaded_file)
        text = "\n".join([para.text for para in doc.paragraphs])
        st.success("✅ Word document loaded successfully.")
    
    else:
        st.error("Unsupported file type.")
        text = ""

    # === AI Analysis ===
    if text:
        st.subheader("🔍 AI Analysis")
        question = st.text_area("Ask the AI a question about your file:", "Summarize the content.")

        if st.button("Analyze with AI"):
            with st.spinner("AI is analyzing..."):
                try:
                    response = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are an AI assistant that analyzes files and provides insights."},
                            {"role": "user", "content": f"File content:\n{text[:5000]}\n\nQuestion: {question}"}
                        ]
                    )
                    answer = response.choices[0].message.content
                    st.markdown("### 💡 AI Result")
                    st.write(answer)
                except Exception as e:
                    st.error(f"Error: {e}")
