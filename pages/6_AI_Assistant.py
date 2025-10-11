import streamlit as st
from openai import OpenAI
import os

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 EconLab — AI Assistant (Poe Model)")
st.write("Ask **Maztouriabot** anything about economics or data analysis — powered by Poe API.")

# -------------------------------
# API SETUP
# -------------------------------
POE_API_KEY = st.secrets.get("POE_API_KEY") or os.getenv("POE_API_KEY")

if not POE_API_KEY:
    st.error("❌ Missing Poe API key. Please add it in Streamlit secrets as `POE_API_KEY = 'your_key_here'`.")
    st.stop()

client = OpenAI(
    api_key=POE_API_KEY,
    base_url="https://api.poe.com/v1"
)

MODEL = "maztouriabot"

# -------------------------------
# CHAT HISTORY
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# USER INPUT
# -------------------------------
user_input = st.chat_input("Ask Maztouriabot anything about economics or data analysis:")

if user_input:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant reply
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⌛ Thinking...")

        try:
            chat = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": user_input}],
            )
            response = chat.choices[0].message.content
            placeholder.markdown(response)

        except Exception as e:
            st.error(f"❌ API request failed: {e}")
            response = "Error connecting to Poe API."

    # Save assistant response
    st.session_state["messages"].append({"role": "assistant", "content": response})

# -------------------------------
# CLEAR CHAT
# -------------------------------
if st.button("Clear chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared. You can start again!")
