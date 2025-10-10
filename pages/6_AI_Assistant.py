import streamlit as st
import os

st.title("🤖 AI Economics Assistant")
st.write("Ask EconLab anything about economics or data analysis — powered by a local or cloud AI model.")

# --- Try to import local model first ---
try:
    from llama_cpp import Llama
    LOCAL_LLAMA = True
except ModuleNotFoundError:
    LOCAL_LLAMA = False
    from openai import OpenAI

# --- Prompt input ---
prompt = st.text_area("💬 Your question:", placeholder="e.g. Explain the relationship between inflation and interest rates...")

# --- Response section ---
if st.button("Generate Answer"):
    if not prompt.strip():
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):

            # ===== LOCAL LLaMA PATH =====
            model_path = "models/Llama-2-13B_Q4_K_M.gguf"

            if LOCAL_LLAMA and os.path.exists(model_path):
                st.info("Using local model: Llama-2-13B_Q4_K_M.gguf")
                llm = Llama(
                    model_path=model_path,
                    n_ctx=4096,
                    n_threads=6,
                    n_gpu_layers=20,
                    verbose=False
                )
                response = llm.create_completion(
                    prompt=f"Answer the following economics question clearly and concisely:\n{prompt}\nAnswer:",
                    max_tokens=400,
                    temperature=0.6,
                )
                answer = response["choices"][0]["text"].strip()

            else:
                # ===== FALLBACK: GPT via API =====
                st.warning("Using cloud GPT model (local model not available).")
                client = OpenAI()
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an expert in economics and data analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    tempe
