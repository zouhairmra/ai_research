# pages/6_AI_Assistant.py
import streamlit as st
from llama_cpp import Llama

def show():
    st.title("🤖 EconLab AI Assistant (Local LLaMA 2)")

    st.write("Ask anything about economics, econometrics, statistics, or data analysis!")

    question = st.text_input("Your question:")

    if question:
        st.info("💡 Generating answer… please wait.")

        try:
            # Initialize LLaMA model (make sure the path points to your .gguf file)
            llm = Llama(model_path="models/Llama-2-13B_Q4_K_M.gguf")

            # Generate response
            response = llm(
                question,
                max_tokens=512,
                stop=None,
                temperature=0.2
            )

            st.success("✅ Answer:")
            st.write(response['choices'][0]['text'])

        except Exception as e:
            st.error(f"⚠️ Error generating answer: {e}")
            st.write("Please check that your .gguf model exists and is compatible.")
