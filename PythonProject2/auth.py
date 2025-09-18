import streamlit as st
import sqlite3
import bcrypt
from db import add_user, DB_PATH

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    data = c.fetchone()
    conn.close()
    if data:
        stored_hash = data[2]
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return data
    return None

def signup_page():
    st.subheader("🆕 Create a New Account")
    username = st.text_input("Username", key="signup_user")
    password = st.text_input("Password", type="password", key="signup_pass")
    role = st.selectbox("Role", ["Doctor", "Admin"], key="signup_role")

    if st.button("Sign Up"):
        if username and password:
            success = add_user(username, password, role)
            if success:
                st.success("✅ Account created successfully! You can now log in.")
            else:
                st.error("❌ Username already exists. Try another.")
        else:
            st.warning("⚠️ Please fill all fields")