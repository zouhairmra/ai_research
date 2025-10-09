import streamlit as st

# Example simple authentication
USERS = {
    "admin": "password123",
    "student": "econlab2025"
}

def login():
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username in USERS and USERS[username] == password:
            st.sidebar.success(f"Welcome, {username}!")
            return True
        else:
            st.sidebar.error("Invalid username or password")
            return False
    return False

