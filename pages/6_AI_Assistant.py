import streamlit as st
from openai import OpenAI

# ==============================
# Streamlit Page Config
# ==============================
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 EconLab — AI Assistant (Poe API)")
st.write("Ask your Poe-hosted AI (e.g., maztouriabot) anything about economics or data analysis.")

# ==============================
# Poe API Setup
# ==============================
try:
    client = OpenAI(
        api_key=st.secrets["POE_API_KEY"],   # Add this to Streamlit secrets
        base_url="https://api.poe.com/v1"
    )
except Exception as e:
    st.error(f"⚠️ Poe API client initialization failed: {e}")
    st.stop()

# ==============================
# Select Model
# ==============================
model = st.selectbox("Select your Poe model", ["maztouriabot", "claude-instant", "gpt-4o-mini"])

# ==============================
# Chat History
# ==============================
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ==============================
# Chat Input
# ==============================
user_input = st.chat_input("Ask me anything about economics or data analysis:")

if user_input:
    # Store user message
    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant reply
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        try:
            response = client.chat.completions.create(
                model=model,
                messages=st.session_state["messages"]
            )
            full_response = response.choices[0].message.content
            placeholder.markdown(full_response)

        except Exception as e:
            st.error(f"❌ Error communicating with Poe API: {e}")
            full_response = f"Error: {e}"

    # Save assistant response
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# ==============================
# Clear Chat Button
# ==============================
if st.button("Clear chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared. You can start again!")
