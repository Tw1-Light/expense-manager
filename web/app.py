import os
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash
from core.expense_manager import ExpenseManager
from PIL import Image
import pytesseract
import re
import datetime

# Set the path to Tesseract manually
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
manager = ExpenseManager()

@app.route('/')
def index():
    expenses = manager.list_expenses()
    budgets = manager.list_budgets()
    total_by_category = {
        category: manager.get_total_expense_by_category(category)
        for category, _ in budgets
    }
    return render_template('index.html', expenses=expenses, budgets=budgets, total_by_category=total_by_category)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    date = request.form['date']
    description = request.form['description']
    amount = float(request.form['amount'])
    category = request.form['category']
    vendor = request.form.get('vendor', '')  # optional vendor
    manager.add_expense(date, description, amount, category, vendor)
    return redirect(url_for('index'))

@app.route('/set_budget', methods=['POST'])
def set_budget():
    category = request.form['category']
    amount = float(request.form['amount'])
    manager.set_budget(category, amount)
    return redirect(url_for('index'))

@app.route('/upload_bill', methods=['POST'])
def upload_bill():

    file = request.files['bill']
    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            file.save(tmp.name)
            try:
                text = pytesseract.image_to_string(Image.open(tmp.name))
            except Exception as e:
                flash("Failed to process the image. Please upload a valid bill image.", "danger")
                return redirect(url_for('index'))

        predicted_category = predict_category_from_text(text)

        # For demonstration, extract dummy values from the OCR text
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        description = "Auto-scanned bill"
        vendor = "Unknown Vendor"
        amount = 0.0

        # Try to extract some amount from the text
        amounts = re.findall(r'\d+\.\d{2}', text)
        if amounts:
            amount = float(amounts[0])

        # Save to DB
        manager.add_expense(today, description, amount, predicted_category, vendor)

        flash(f"Bill scanned and saved under category: {predicted_category}", "success")
    else:
        flash("No file selected!", "warning")
    return redirect(url_for('index'))

def predict_category_from_text(text):
    text = text.lower()
    if "medicine" in text or "pharmacy" in text:
        return "Medical"
    elif "grocery" in text or "supermarket" in text:
        return "Groceries"
    elif "uber" in text or "bus" in text or "taxi" in text:
        return "Transportation"
    elif "electricity" in text or "water bill" in text:
        return "Utilities"
    elif "movie" in text or "netflix" in text or "entertainment" in text:
        return "Entertainment"
    else:
        return "Others"

if __name__ == '__main__':
    app.run(debug=True)
