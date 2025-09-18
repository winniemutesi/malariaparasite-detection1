import streamlit as st
from db import init_db
from detection import detection_page
from dashboard import dashboard_page
from auth import login_user, signup_page
from admin import admin_user_management

init_db()
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Load CSS and insert app bar
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown('<div class="appbar"><span class="appbar-title">Malaria Detection</span></div>', unsafe_allow_html=True)
st.markdown('<div class="datetime-banner"><div id="date-line"></div></div>', unsafe_allow_html=True)
st.markdown("""
<script>
  const dateEl = document.getElementById('date-line');
  function updateClock(){
    try {
      const now = new Date();
      const fmtDate = new Int1.DateTimeFormat('en-GB', { year: 'numeric', month: '2-digit', day: '2-digit' }).format(now);
      dateEl.textContent = fmtDate;
    } catch(e) {}
  }
  updateClock();
  setInterval(updateClock, 1000);
</script>
""", unsafe_allow_html=True)


def home_page():
    st.markdown("""
    <div class="background"></div>
    <div class="overlay">Fast Malaria Detection Using AI Models</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    option = st.radio("Select Action", ["🔑 Login", "🆕 Signup"], horizontal=True)

    if option=="🔑 Login":
        st.subheader("🔑 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state["logged_in"]=True
                st.session_state["username"]=user[1]
                st.session_state["role"]=user[3]
                st.success(f"✅ Welcome {user[3]}: {user[1]}")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
    elif option=="🆕 Signup":
        signup_page()
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state["logged_in"]:
    home_page()
else:
    st.sidebar.markdown(f"## 👋 {st.session_state['username']} ({st.session_state['role']})")
    nav_options = ["🔍 Detection", "📊 Dashboard", "🚪 Logout"]
    if st.session_state["role"]=="Admin":
        nav_options.insert(1, "👤 User Management")
    choice = st.sidebar.radio("Navigate", nav_options, label_visibility="collapsed")
    if choice=="🔍 Detection":
        detection_page()
    elif choice=="📊 Dashboard":
        dashboard_page()
    elif choice=="👤 User Management":
        admin_user_management()
    elif choice=="🚪 Logout":
        st.session_state["logged_in"]=False
        st.rerun()