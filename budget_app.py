import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trans_type = db.Column(db.String(50))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))
    date = db.Column(db.String(50))

@app.route('/transactions', methods=['GET'])
def get_transactions():
    transactions = Transaction.query.all()
    return jsonify([t.to_dict() for t in transactions])

@app.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    new_transaction = Transaction(
        trans_type=data['trans_type'],
        amount=data['amount'],
        category=data['category'],
        date=data['date']
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify(new_transaction.to_dict()), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


class Transaction:
    def __init__(self, trans_type, amount, category, date=None):
        self.trans_type = trans_type
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "trans_type": self.trans_type,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Transaction(data["trans_type"], data["amount"], data["category"], data["date"])

class Budget:
    import sqlite3

class Budget:
    def __init__(self, db_path='budget.db'):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    trans_type TEXT,
                    amount REAL,
                    category TEXT,
                    date TEXT
                )
            ''')

    def add_transaction(self, trans_type, amount, category, date=None):
        date = date if date else datetime.now().strftime("%Y-%m-%d")
        with self.conn:
            self.conn.execute('''
                INSERT INTO transactions (trans_type, amount, category, date)
                VALUES (?, ?, ?, ?)
            ''', (trans_type, amount, category, date))

    def get_transactions(self):
        with self.conn:
            return self.conn.execute('SELECT * FROM transactions').fetchall()

    def delete_transaction(self, trans_id):
        with self.conn:
            self.conn.execute('DELETE FROM transactions WHERE id = ?', (trans_id,))


    def __init__(self):
        self.transactions = []

    def add_income(self, amount, category, date=None):
        if amount <= 0:
            raise ValueError("Income amount must be positive.")
        self.transactions.append(Transaction("income", amount, category, date))

    def add_expense(self, amount, category, date=None):
        if amount <= 0:
            raise ValueError("Expense amount must be positive.")
        self.transactions.append(Transaction("expense", amount, category, date))

    def delete_transaction(self, index):
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
        else:
            raise IndexError("Transaction index out of range")

    def view_status(self):
        total_income = sum(t.amount for t in self.transactions if t.trans_type == "income")
        total_expense = sum(t.amount for t in self.transactions if t.trans_type == "expense")
        balance = total_income - total_expense
        return total_income, total_expense, balance

    def view_history(self):
        return [(i, t.date, t.trans_type, t.amount, t.category) for i, t in enumerate(self.transactions)]

    def save_to_file(self, file_path):
        with open(file_path, "w") as file:
            json.dump([t.to_dict() for t in self.transactions], file)

    def load_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                self.transactions = [Transaction.from_dict(t) for t in json.load(file)]
        except FileNotFoundError:
            pass

    def category_report(self):
        report = {}
        for t in self.transactions:
            if t.trans_type == "expense":
                if t.category in report:
                    report[t.category] += t.amount
                else:
                    report[t.category] = t.amount
        return report
        class Budget:
    

    def add_category(self, category):
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category):
        if category in self.categories:
            self.categories.remove(category)


class BudgetApp:
    def __init__(self, root):
        self.budget = Budget()
        self.budget.load_from_file("budget.json")
        self.root = root
        self.root.title("Budget Manager")

        # Frames
        self.setup_frames()

        # Input Widgets
        self.setup_input_widgets()

        # Transaction Table
        self.setup_transaction_table()

        # Buttons
        self.setup_buttons()

    def setup_frames(self):
        self.input_frame = ttk.Frame(self.root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky="ew")

        self.table_frame = ttk.Frame(self.root, padding="10")
        self.table_frame.grid(row=1, column=0, sticky="nsew")

        self.output_frame = ttk.Frame(self.root, padding="10")
        self.output_frame.grid(row=2, column=0, sticky="nsew")

    def setup_input_widgets(self):
        self.amount_label = ttk.Label(self.input_frame, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.input_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        self.category_label = ttk.Label(self.input_frame, text="Category:")
        self.category_label.grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.input_frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        self.date_label = ttk.Label(self.input_frame, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.input_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

    def setup_transaction_table(self):
        self.transaction_tree = ttk.Treeview(self.table_frame, columns=("Date", "Type", "Amount", "Category"), show='headings')
        self.transaction_tree.heading("Date", text="Date")
        self.transaction_tree.heading("Type", text="Type")
        self.transaction_tree.heading("Amount", text="Amount")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

    def setup_buttons(self):
        self.income_button = ttk.Button(self.input_frame, text="Add Income", command=self.add_income)
        self.income_button.grid(row=3, column=0, padx=5, pady=5)

        self.expense_button = ttk.Button(self.input_frame, text="Add Expense", command=self.add_expense)
        self.expense_button.grid(row=3, column=1, padx=5, pady=5)

        self.status_button = ttk.Button(self.input_frame, text="View Status", command=self.view_status)
        self.status_button.grid(row=4, column=0, padx=5, pady=5)

        self.history_button = ttk.Button(self.input_frame, text="View History", command=self.view_history)
        self.history_button.grid(row=4, column=1, padx=5, pady=5)

        self.report_button = ttk.Button(self.input_frame, text="Category Report", command=self.view_category_report)
        self.report_button.grid(row=5, column=0, padx=5, pady=5)

        self.save_button = ttk.Button(self.input_frame, text="Save", command=self.save_budget)
        self.save_button.grid(row=5, column=1, padx=5, pady=5)

        self.delete_button = ttk.Button(self.input_frame, text="Delete Selected", command=self.delete_transaction)
        self.delete_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def add_income(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            date = self.date_entry.get() or None
            self.budget.add_income(amount, category, date)
            self.show_message(f"Added income: ${amount} in {category} category.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get()
            date = self.date_entry.get() or None
            self.budget.add_expense(amount, category, date)
            self.show_message(f"Added expense: ${amount} in {category} category.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def view_status(self):
        total_income, total_expense, balance = self.budget.view_status()
        status_message = f"Total Income: ${total_income}\nTotal Expense: ${total_expense}\nBalance: ${balance}"
        self.show_message(status_message)

    def view_history(self):
        history = self.budget.view_history()
        self.transaction_tree.delete(*self.transaction_tree.get_children())
        for index, date, trans_type, amount, category in history:
            self.transaction_tree.insert("", "end", iid=index, values=(date, trans_type, amount, category))
        history_message = "\n".join([f"{date}: {trans_type} - ${amount} ({category})" for _, date, trans_type, amount, category in history])
        self.show_message(history_message)

    def view_category_report(self):
        report = self.budget.category_report()
        if not report:
            self.show_message("No expenses to report.")
            return
        report_message = "\nCategory-wise Expense Report:\n" + "\n".join([f"{category}: ${amount}" for category, amount in report.items()])
        self.show_message(report_message)

    def save_budget(self):
        self.budget.save_to_file("budget.json")
        self.show_message("Budget saved successfully.")

    def delete_transaction(self):
        try:
            selected_item = self.transaction_tree.selection()[0]
            index = int(selected_item)
            self.budget.delete_transaction(index)
            self.view_history()
            self.show_message(f"Deleted transaction at index {index}.")
        except IndexError as e:
            messagebox.showerror("Error", "No transaction selected.")

    def show_message(self, message):
        self.output_frame.config(state=tk.NORMAL)
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        label = tk.Label(self.output_frame, text=message, justify=tk.LEFT)
        label.grid(row=0, column=0, padx=5, pady=5)
        self.output_frame.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
