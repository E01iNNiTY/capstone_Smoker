import streamlit as st
import json
import os

st.set_page_config(page_title="Login", layout="centered")

SESSION_FILE = "user_session.json"

def login():
    if is_logged_in():
        return True

    st.title("🔐 Login Required")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "pass123":
            with open(SESSION_FILE, "w") as f:
                json.dump({"logged_in": True}, f)
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials")

    return False

def is_logged_in():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                return data.get("logged_in", False)
        except json.JSONDecodeError:
            # File exists but is not valid JSON (maybe empty or corrupted)
            return False
    return False

def logout():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
