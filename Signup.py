import hashlib
import re
import sqlite3 as sq

import streamlit as st

# Define the database schema


def create_database():
    conn = sq.connect("streamlit.db", check_same_thread=False)
    cr = conn.cursor()
    cr.execute("""
    CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT UNIQUE,
                password TEXT NOT NULL,
                phone_number INTEGER,
                date_of_birth DATE,
                created_at TIMESTAMP DEFAULT_CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()


# Initialize the database
create_database()

# Define the layout
col1, col2 = st.columns(2, gap="medium")
# Regular expression for basic email format validation.
email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


def validate_password(password):
    # Regular expression for password requirements
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$'

    if re.match(pattern, password):
        return True
    else:
        return False
# Sign-up logic


signup_user_name = st.text_input(label="Username").lower()
signup_email = st.text_input(label="Email", autocomplete="email").lower()
signup_password = st.text_input(
    label="Enter your password", type="password")
signup_verify_password = st.text_input(
    label="Re-enter your password", type="password")


def new_user_sign_up():
    # Ensure all fields are filled
    if not signup_user_name or not signup_email or not signup_password:
        st.error("All fields are required!")
        return
    # Validate the email format
    if not re.match(email_regex, signup_email):
        st.error("Please enter a valid email address")
        return
    # Check if passwords match
    if not validate_password(signup_password):
        st.error(
            "Password does not meet the requirements:\n"
            "1. At least 8 characters\n"
            "2. Contains both uppercase and lowercase letters\n"
            "3. Contains at least one number\n"
            "4. Contains at least one special character (!@#$%^&*)"
        )
        return

    if signup_password != signup_verify_password:
        st.error("Passwords do not match!")
        return

    # Hash the password
    hashed_password = hashlib.sha256(signup_password.encode()).hexdigest()

    # Create a new database connection in this thread
    conn = sq.connect("streamlit.db", check_same_thread=False)
    cr = conn.cursor()

    try:
        # Insert the new user into the database
        cr.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (signup_user_name, signup_email, hashed_password),
        )
        conn.commit()
        st.success("User signed up successfully!")
    except sq.IntegrityError:
        st.error("An error occurred: Email must be unique.")
    finally:
        conn.close()


# Sign-up button
st.button(label="Sign up", on_click=new_user_sign_up)
