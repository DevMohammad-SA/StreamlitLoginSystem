import os
import sqlite3 as sq

import pandas as pd  # Import pandas for DataFrame support
import streamlit as st

# Streamlit setup
st.set_page_config(page_title="Fetch Data", layout="wide")
st.header("Fetch All Data from Database")

# Path to the database
db_path = os.path.join(os.path.dirname(__file__), '..', 'streamlit.db')

# Connect to the database
try:
    conn = sq.connect(db_path, check_same_thread=False)
    cr = conn.cursor()
except sq.Error as e:
    st.error(f"Error occurred while connecting to the database: {e}")
    conn = None

# Function to fetch all data


def fetch_all_data():
    try:
        # Input table name
        table_name = st.text_input(
            "Enter the table name to fetch data:", "users")

        # Fetch data when button is clicked
        if st.button("Fetch Data"):
            if not table_name:
                st.error("Table name cannot be empty!")
                return

            # Execute SQL query
            cr.execute(f"SELECT * FROM {table_name}")
            data = cr.fetchall()

            # Get column names
            columns = [description[0] for description in cr.description]

            # Convert to pandas DataFrame
            df = pd.DataFrame(data, columns=columns)

            # Display data
            if not df.empty:
                st.success(f"Fetched {len(df)} rows from '{
                           table_name}' table.")
                st.dataframe(df)  # Display pandas DataFrame
            else:
                st.warning(f"No data found in the '{table_name}' table.")
    except sq.Error as e:
        st.error(f"An error occurred while fetching data: {e}")


# Main logic
if conn:
    fetch_all_data()

# Close the connection when done
if conn:
    conn.close()
