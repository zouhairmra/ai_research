import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 EconLab — AI Assistant")
st.write("Ask your remote Ollama model anything about economics or data analysis.")

# -------------------------------
# Remote Ollama API URL (from secrets)
# -------------------------------
OLLAMA_API_URL = st.secrets.get("OLLAMA_API_URL", "http://86.36.65.70:11434/api/chat")

# Select model if your server has multiple models
model = st.selectbox("Select model", ["llama3.2", "phi3", "mistral", "gemma2"])

# -------------------------------
# Initialize session messages
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# User input
# -------------------------------
user_input = st.chat_input("Ask me anything about economics or data analysis:")

if user_input:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------------
    # Send to Ollama API
    # -------------------------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # streaming enabled
            response = requests.post(
                OLLAMA_API_URL,
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": user_input}],
                    "stream": True
                },
                stream=True,
                timeout=60
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
# Clear chat button
# -------------------------------
if st.button("Clear chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared. You can start again!")
