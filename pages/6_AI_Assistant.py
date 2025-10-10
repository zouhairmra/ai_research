import streamlit as st
import requests
import json

# -------------------------------
# ✅ Page setup
# -------------------------------
st.set_page_config(page_title="AI Assistant", page_icon="🤖")
st.title("🤖 Local AI Assistant (Ollama)")
st.write("Chat with a local or remote model powered by Ollama!")

# -------------------------------
# ⚙️ Ollama settings
# -------------------------------
OLLAMA_API_URL = st.secrets.get("OLLAMA_API_URL", "http://localhost:11434/api/chat")

# Model options
model = st.selectbox("Select model", ["llama3.2", "phi3", "mistral", "gemma2"])

# -------------------------------
# 💬 Chat interface
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask me anything about your research or data...")

if user_input:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to Ollama API
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": user_input}],
                    "stream": True
                },
                stream=True,
            )

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    token = data.get("message", {}).get("content", "")
                    full_response += token
                    placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Error connecting to Ollama: {e}")
            full_response = "Error: could not connect to Ollama."

    # Save assistant response
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# -------------------------------
# 🧹 Reset chat
# -------------------------------
if st.button("Clear chat"):
    st.session_state["messages"] = []
    st.experimental_rerun()
