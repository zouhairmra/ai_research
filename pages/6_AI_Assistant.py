# pages/6_AI_Assistant.py
import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="AI Assistant (Poe via HTTP)", page_icon="🤖", layout="centered")
st.title("🤖 EconLab — AI Assistant (Poe via HTTP)")
st.write("Ask your Poe-hosted model (maztouriabot). This version uses plain HTTP (no `openai` package).")

# Get API key from Streamlit secrets or env
POE_API_KEY = st.secrets.get("POE_API_KEY") or os.getenv("POE_API_KEY")
if not POE_API_KEY:
    st.error("Missing POE_API_KEY. Add it to Streamlit Secrets or set POE_API_KEY env var.")
    st.stop()

# Poe endpoint (official base)
POE_BASE = "https://api.poe.com/v1"
POE_CHAT_ENDPOINT = POE_BASE + "/chat/completions"

# Model
model = st.selectbox("Select Poe model", ["maztouriabot", "gpt-4o-mini", "claude-instant"])

# session messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# show chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input
user_input = st.chat_input("Ask Maztouriabot anything about economics or data analysis:")

def call_poe_http(model_name: str, messages: list):
    """
    Call Poe via HTTP POST. Uses simple POST to /v1/chat/completions with messages.
    Returns the assistant text or raises an Exception.
    """
    headers = {
        "Authorization": f"Bearer {POE_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": messages
    }
    resp = requests.post(POE_CHAT_ENDPOINT, headers=headers, json=payload, timeout=60)
    # Raise on non-2xx
    resp.raise_for_status()
    data = resp.json()
    # Poe response format should include choices[0].message.content
    # handle common variations defensively:
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        # Try fallback keys
        if "output" in data:
            return data["output"]
        return json.dumps(data)  # return raw for debugging

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⌛ Thinking...")

        try:
            # build messages in simple OpenAI-like form
            messages = st.session_state["messages"]
            # call Poe via HTTP
            answer = call_poe_http(model, messages)
            placeholder.markdown(answer)
        except requests.HTTPError as http_e:
            st.error(f"HTTP error when calling Poe: {http_e} — {http_e.response.text if http_e.response is not None else ''}")
            answer = f"Error: {http_e}"
        except Exception as e:
            st.error(f"Error calling Poe API: {e}")
            answer = f"Error: {e}"

    st.session_state["messages"].append({"role": "assistant", "content": answer})

# clear chat
if st.button("🧹 Clear chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared. You can start again!")
