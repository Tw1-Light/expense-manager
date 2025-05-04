import os
import sqlite3

def get_db_path(custom_path=None):
    if custom_path:
        db_path = custom_path
    else:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        db_path = os.path.join(base_dir, 'data', 'expenses.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return db_path

def connect_db(custom_path=None):
    return sqlite3.connect(get_db_path(custom_path), check_same_thread=False)

def create_tables(custom_path=None):
    conn = connect_db(custom_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            vendor TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            category TEXT PRIMARY KEY,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()