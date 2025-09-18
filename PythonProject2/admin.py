import streamlit as st
from db import get_all_users, delete_user, add_user
import bcrypt
import pandas as pd

def admin_user_management():
    st.title("🛠 Admin User Management")
    users = get_all_users()
    if users:
        df = pd.DataFrame(users, columns=["ID", "Username", "Role"])
        def color_role(val):
            return 'background-color: #ffd966; font-weight:bold;' if val=="Admin" else 'background-color:#b6d7a8;'
        st.dataframe(df.style.applymap(color_role, subset=['Role']), use_container_width=True)

        st.markdown("### Delete Users")
        for user in users:
            col1, col2 = st.columns([3,1])
            with col1:
                st.write(f"{user[1]} ({user[2]})")
            with col2:
                if st.button("❌ Delete", key=f"del{user[0]}"):
                    delete_user(user[0])
                    st.success(f"User {user[1]} deleted ✅")
                    st.rerun()
    else:
        st.info("No users found.")

    st.markdown("---")
    st.subheader("➕ Add New User")
    col1, col2 = st.columns(2)
    with col1:
        new_username = st.text_input("Username", key="new_user")
    with col2:
        new_password = st.text_input("Password", type="password", key="new_pass")
    new_role = st.selectbox("Role", ["Doctor", "Admin"], key="new_role")

    if st.button("Add User"):
        if new_username and new_password:
            hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            success = add_user(new_username, hashed_pw.decode('utf-8'), new_role)
            if success:
                st.success(f"User {new_username} added successfully ✅")
                st.rerun()
            else:
                st.error("Username already exists ❌")
        else:
            st.warning("Please fill all fields ⚠️")