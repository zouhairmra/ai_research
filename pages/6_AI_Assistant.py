import streamlit as st
from llama_cpp import Llama

st.set_page_config(page_title="EconLab — Local AI Assistant", layout="centered")

st.title("🤖 EconLab — Local AI Assistant")
st.caption("Ask your local AI model (Llama-2-13B_Q4_K_M.gguf) about economics or data analysis.")

# Path to your local model
MODEL_PATH = "./models/Llama-2-13B_Q4_K_M.gguf"

# Load model (only once)
@st.cache_resource
def load_model():
    return Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,
        n_threads=8,  # adjust based on your CPU
        n_gpu_layers=35  # 0 = CPU only, increase if you have GPU
    )

llm = load_model()

# Chat interface
st.subheader("💬 Chat with your local model")

user_input = st.text_area("Your question:", placeholder="e.g., Explain inflation in simple economic terms")

if st.button("Generate Answer"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            output = llm.create_completion(
                prompt=f"The following is a question about economics or data analysis:\n\n{user_input}\n\nAnswer clearly and concisely:",
                max_tokens=512,
                temperature=0.7,
                top_p=0.9
            )
            response = output["choices"][0]["text"].strip()
            st.markdown(f"### 🧠 Answer:\n{response}")
    else:
        st.warning("Please enter a question first.")
