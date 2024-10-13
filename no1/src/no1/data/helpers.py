import sqlite3
import os

"""
GENERIC support for db management
"""

def get_db_path(db_name):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'no1', 'data', 'db'))
    db_path = os.path.join(project_root, f'{db_name}.db')
    return(db_path)

def db_exists(db_name):
    db_path = get_db_path(db_name)
    return os.path.exists(db_path) 