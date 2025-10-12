import streamlit as st
import requests
import json
import time
import pandas as pd
from io import StringIO

# ==========================
# PAGE SETUP
# ==========================
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
st.title("🤖 EconLab — AI Assistant")
st.write("Ask anything about economics, econometrics, or data analysis.")

# ==========================
# API CONFIGURATION (POE)
# ==========================
POE_API_URL = "https://api.poe.com/v1/chat/completions"
POE_API_KEY = st.secrets.get("POE_API_KEY", "YOUR_POE_API_KEY_HERE")

MODEL = st.selectbox("Select model", ["maztouriabot", "gpt-4o-mini", "claude-3-haiku"])

# ==========================
# EXPERT PROMPTS
# ==========================
st.markdown("#### 🧠 Quick Expert Prompts")
cols = st.columns(4)
prompts = {
    "Economic Growth": "Explain the Solow growth model in simple terms.",
    "Econometrics": "What is the difference between fixed and random effects models?",
    "Statistics": "Explain hypothesis testing with an example.",
    "Data Analysis": "How can I detect multicollinearity in regression models?",
}

for i, (label, prompt) in enumerate(prompts.items()):
    if cols[i].button(label):
        st.session_state["prompt"] = prompt
    else:
        st.session_state.setdefault("prompt", "")

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
# USER INPUT
# ==========================
user_input = st.chat_input("Type your question or select a quick prompt above...") or st.session_state.get("prompt", "")

if user_input:
    st.session_state["prompt"] = ""  # reset quick prompt
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

            payload = {
                "model": MODEL,
                "messages": [{"role": "user", "content": user_input}]
            }

            res = requests.post(POE_API_URL, headers=headers, json=payload, timeout=60)
            res.raise_for_status()
            data = res.json()

            # Extract assistant message
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
