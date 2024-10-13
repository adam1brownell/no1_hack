import sqlite3
import os

"""
GENERIC support for db management
"""

def get_db_path(db_name):
    return(os.path.join(os.path.dirname(__file__), 'db', f'{db_name}.db'))

def db_exists(db_name):
    db_path = get_db_path(db_name)
    return os.path.exists(db_path) 