import streamlit as st
import hashlib
from password_config import ADMIN_PASSWORD_HASH
from dashboard import homepage_of_cyclone
from login_page import display_login_page

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

ADMIN_USERNAME = "admin"

def verify_password(password):
    """Verify password by hashing and comparing"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return password_hash == ADMIN_PASSWORD_HASH


# Main entry point
def run_application():
    # First check if user is logged in
    if st.session_state.logged_in:
        homepage_of_cyclone()
    else:
        display_login_page()

if __name__ == "__main__":
    run_application()