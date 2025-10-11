# pages/6_AI_Assistant.py
import streamlit as st
import requests
import json

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 EconLab — AI Assistant")
st.write("Ask your Ollama model anything about economics or data analysis.")

# -------------------------------
# Remote Ollama API URL
# -------------------------------
# Use your public ngrok / Cloudflare / IP tunnel if hosted remotely.
# Example: "https://longname.ngrok.io/api/chat"
# When testing locally, keep: "http://localhost:11434/api/chat"
OLLAMA_API_URL = st.secrets.get("OLLAMA_API_URL", "http://localhost:11434/api/chat")

# -------------------------------
# Model selection
# -------------------------------
model = st.selectbox("Select model", ["llama3.2", "phi3", "mistral", "gemma2"])

# -------------------------------
# Initialize chat history
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# User input
# -------------------------------
user_input = st.chat_input("Ask me anything about economics or data analysis:")

if user_input:
    # Display and store user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # Send user query to Ollama API (streaming)
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": user_input}],
                    "stream": True
                },
                stream=True,
                timeout=120
            )

            # Stream and display each chunk
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Extract text content from Ollama response
                token = data.get("message", {}).get("content", "")
                full_response += token
                placeholder.markdown(full_response + "▌")

                if data.get("done"):
                    break

            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Error connecting to Ollama: {e}")
            full_response = f"Error: could not connect to Ollama ({e})"

    # Save assistant message
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# -------------------------------
# Clear chat
# -------------------------------
if st.button("🧹 Clear chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared — start again!")
