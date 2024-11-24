import hashlib
import os
import sqlite3 as sq

import streamlit as st

# Streamlit setup
st.set_page_config(page_title="Login")
st.header("Login")
# Input fields for username and password
username_input = st.text_input(label="Username").lower()
password_input = st.text_input(label="Password", type="password")
# Path to database
db_path = os.path.join(os.path.dirname(__file__), '..', 'streamlit.db')
# Connect to the database
try:
    conn = sq.connect(db_path, check_same_thread=False)
    cr = conn.cursor()
except sq.Error as e:
    st.error(f"Error occurred :{e}")
    conn = None
# Login function

is_logged_in = False


def login():
    if not username_input or not password_input:
        st.error("Please enter both username and password.")
        return
    # Fetch username from database
    cr.execute("SELECT username FROM users WHERE username = ?",
               (username_input,))
    fetch_username = cr.fetchone()
    if not fetch_username:
        st.error("username not found!")
        return

    # Hash passowrd
    hashed_password = hashlib.sha256(password_input.encode()).hexdigest()

    # Fetch the password from the database for the entered username
    cr.execute("SELECT password FROM users WHERE username = ? ",
               (username_input,))
    fetch_password = cr.fetchone()
    if fetch_password and fetch_password[0] == hashed_password:
        st.success(f"Welcome back {username_input}!")
    else:
        st.error("Incorrect password")


login_button = st.button(label="Login", on_click=login)
not_signed = st.page_link("Signup.py", label="Not signed ?")
