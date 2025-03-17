import streamlit as st
import hashlib
from password_config import ADMIN_PASSWORD_HASH

# Setup session state to track login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

ADMIN_USERNAME = "admin"

def verify_password(password):
    """Verify password by hashing and comparing"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == ADMIN_PASSWORD_HASH

def display_login_page():
    """Display the login form"""
    st.title("Admin Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username == ADMIN_USERNAME and verify_password(password):
                st.session_state.logged_in = True
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")
