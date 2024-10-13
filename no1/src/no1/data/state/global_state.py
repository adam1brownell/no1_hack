"""
GLOBAL STATE
contains:
 - api keys
 - last pulls
 - user info
"""
import sqlite3
import os
from no1.data.helpers import get_db_path


# Initialize the global state database
def init_global_state():
    # Set the path for the global_state.db file inside data/db folder
    gs_path = get_db_path("global_state")

    # Ensure the db folder exists, create it if not
    if not os.path.exists(os.path.dirname(gs_path)):
        os.makedirs(os.path.dirname(gs_path))

    # Connect to the SQLite database (this will create the file if it doesn't exist)
    conn = sqlite3.connect(gs_path)

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Create the global_state table if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS global_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usr_name TEXT NULL,
            oura_key TEXT NULL,
            oura_pull_date DATE NULL
        )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Function to check if a column (e.g., 'oura_key') is NULL or has been set
def is_saved(var_name):
    conn = sqlite3.connect(get_db_path("global_state"))
    cursor = conn.cursor()

    # Query the value of the given column
    cursor.execute(f'SELECT {var_name} FROM global_state WHERE id=1')
    result = cursor.fetchone()

    conn.close()

    # Return True if the column has a value, False if it's NULL or empty
    return result is not None and result[0] is not None

# Function to set a value in a specific column (e.g., 'oura_key')
def save_state(var_name, value):
    conn = sqlite3.connect(get_db_path("global_state"))
    cursor = conn.cursor()

    # Insert the row if it doesn't exist, otherwise update the column value
    cursor.execute(f'''
        INSERT INTO global_state (id, {var_name}) 
        VALUES (1, ?) 
        ON CONFLICT(id) DO UPDATE SET {var_name} = excluded.{var_name}
    ''', (value,))

    conn.commit()
    conn.close()

def get_state(var_name):
    conn = sqlite3.connect(get_db_path("global_state"))
    cursor = conn.cursor()

    # Query the value of the given column
    cursor.execute(f'SELECT {var_name} FROM global_state WHERE id=1')
    result = cursor.fetchone()

    conn.close()

    # Return the value, or None if not set
    return result[0] if result else None
