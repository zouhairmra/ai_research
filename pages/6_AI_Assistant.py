import streamlit as st
import requests
import json

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 EconLab — AI Assistant")
st.write("Ask your remote Ollama model anything about economics or data analysis.")

# -------------------------------
# Remote Ollama API URL
# -------------------------------
OLLAMA_API_URL = st.secrets.get("OLLAMA_API_URL", "http://86.36.65.70:11434/api/chat")

# Select model
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
# Chat input
# -------------------------------
user_input = st.chat_input("Ask me anything about economics or data analysis:")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            # Send to Ollama
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

            # Process stream
            for line in response.iter_lines():
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue

                # Ollama may send 'message', 'data', or partial text
                if "message" in data and "content" in data["message"]:
                    token = data["message"]["content"]
                elif "data" in data:
                    token = data["data"]
                elif "content" in data:
                    token = data["content"]
                else:
                    token = ""

                full_response += token
                placeholder.markdown(full_response + "▌")

                # Stop when done
                if data.get("done"):
                    break

            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Error connecting to Ollama: {e}")
            full_response = f"Error: could not connect to Ollama ({e})"

    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# -------------------------------
# Clear chat
# -------------------------------
if st.button("Clear chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared. You can start again!")
