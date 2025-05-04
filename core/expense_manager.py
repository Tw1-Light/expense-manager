import sqlite3
import os

def get_db_path():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(base_dir, 'data', 'expenses.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return db_path

def connect_db():
    return sqlite3.connect(get_db_path(), check_same_thread=False)

def create_tables():
    conn = connect_db()
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

class ExpenseManager:
    def __init__(self, db_path=None):
        self.conn = connect_db()
        self.cursor = self.conn.cursor()
        create_tables()

    def add_expense(self, date, description, amount, category, vendor=None):
        self.cursor.execute("""
            INSERT INTO expenses (date, description, amount, category, vendor)
            VALUES (?, ?, ?, ?, ?)
        """, (date, description, amount, category, vendor))
        self.conn.commit()

    def set_budget(self, category, amount):
        self.cursor.execute("""
            INSERT INTO budgets (category, amount)
            VALUES (?, ?)
            ON CONFLICT(category) DO UPDATE SET amount = ?
        """, (category, amount, amount))
        self.conn.commit()

    def list_expenses(self):
        self.cursor.execute("SELECT * FROM expenses")
        return self.cursor.fetchall()

    def list_budgets(self):
        self.cursor.execute("SELECT * FROM budgets")
        return self.cursor.fetchall()

    def get_budget(self, category):
        self.cursor.execute("SELECT amount FROM budgets WHERE category = ?", (category,))
        return self.cursor.fetchone()

    def get_total_expense_by_category(self, category):
        self.cursor.execute("SELECT SUM(amount) FROM expenses WHERE category = ?", (category,))
        result = self.cursor.fetchone()[0]
        return result or 0.0
