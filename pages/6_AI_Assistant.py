import streamlit as st

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 EconLab — AI Assistant (Poe)")
st.write("Ask your Poe-hosted AI anything about economics or data analysis.")

# -------------------------------
# Try importing OpenAI client
# -------------------------------
try:
    from openai import OpenAI
except ModuleNotFoundError:
    st.error("⚠️ Missing library: `openai`. Please add `openai` to requirements.txt and redeploy.")
    st.stop()

# -------------------------------
# Initialize Poe client
# -------------------------------
try:
    client = OpenAI(
        api_key=st.secrets["POE_API_KEY"],  # Add this to Streamlit Secrets
        base_url="https://api.poe.com/v1"
    )
except Exception as e:
    st.error(f"⚠️ Failed to initialize Poe client: {e}")
    st.stop()

# -------------------------------
# Model selection
# -------------------------------
model = st.selectbox("Select Poe model", ["maztouriabot", "claude-instant", "gpt-4o-mini"])

# -------------------------------
# Chat history in session
# -------------------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Chat input
# -------------------------------
user_input = st.chat_input("Ask me anything about economics or data analysis:")

if user_input:
    # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response
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

# -------------------------------
# Clear chat button
# -------------------------------
if st.button("Clear chat"):
    st.session_state["messages"] = []
    st.toast("Chat cleared. You can start again!")
