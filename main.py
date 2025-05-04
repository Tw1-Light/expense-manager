import os
from db.database import create_tables
from core.expense_manager import ExpenseManager

# Ensure 'data' folder exists and create tables if they don't exist
os.makedirs("expense_manager/data", exist_ok=True)
create_tables()  # Call create_tables() to ensure tables are created

# Initialize ExpenseManager instance
manager = ExpenseManager()

# Example: Add a test expense (optional)
# manager.add_expense("2025-04-21", "Grocery shopping", 85.50, "Groceries", "Walmart")

# Fetch and display all expenses
print("Expenses:")
expenses = manager.list_expenses()
for e in expenses:
    print(e)

# Display budget for a category (if set)
category = "Groceries"
budget = manager.get_budget(category)
if budget:
    print(f"Budget for {category}: {budget}")
