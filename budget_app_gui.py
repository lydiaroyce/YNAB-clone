import json
import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

class BudgetApp:
    def __init__(self, root):
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

        # Load transactions from the backend
        self.load_transactions()

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

    def load_transactions(self):
        response = requests.get('http://127.0.0.1:5000/transactions')
        transactions = response.json()
        for transaction in transactions:
            self.transaction_tree.insert("", "end", iid=transaction['id'], values=(
                transaction['date'], transaction['trans_type'], transaction['amount'], transaction['category']
            ))

    def add_income(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get() or datetime.now().strftime("%Y-%m-%d")

        if not amount or not category:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        data = {
            "trans_type": "income",
            "amount": amount,
            "category": category,
            "date": date
        }
        response = requests.post('http://127.0.0.1:5000/transactions', json=data)
        if response.status_code == 201:
            transaction = response.json()
            self.transaction_tree.insert("", "end", iid=transaction['id'], values=(
                transaction['date'], transaction['trans_type'], transaction['amount'], transaction['category']
            ))
            self.show_message(f"Added income: ${amount} in {category} category.")
        else:
            messagebox.showerror("Error", "Failed to add income.")

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get() or datetime.now().strftime("%Y-%m-%d")

        if not amount or not category:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        data = {
            "trans_type": "expense",
            "amount": amount,
            "category": category,
            "date": date
        }
        response = requests.post('http://127.0.0.1:5000/transactions', json=data)
        if response.status_code == 201:
            transaction = response.json()
            self.transaction_tree.insert("", "end", iid=transaction['id'], values=(
                transaction['date'], transaction['trans_type'], transaction['amount'], transaction['category']
            ))
            self.show_message(f"Added expense: ${amount} in {category} category.")
        else:
            messagebox.showerror("Error", "Failed to add expense.")

    def view_status(self):
        total_income = sum(float(self.transaction_tree.item(item, 'values')[2]) for item in self.transaction_tree.get_children() if self.transaction_tree.item(item, 'values')[1] == 'income')
        total_expense = sum(float(self.transaction_tree.item(item, 'values')[2]) for item in self.transaction_tree.get_children() if self.transaction_tree.item(item, 'values')[1] == 'expense')
        balance = total_income - total_expense
        status_message = f"Total Income: ${total_income}\nTotal Expense: ${total_expense}\nBalance: ${balance}"
        self.show_message(status_message)

    def view_history(self):
        self.load_transactions()

    def view_category_report(self):
        expenses = [self.transaction_tree.item(item, 'values') for item in self.transaction_tree.get_children() if self.transaction_tree.item(item, 'values')[1] == 'expense']
        report = {}
        for expense in expenses:
            category = expense[3]
            amount = float(expense[2])
            if category in report:
                report[category] += amount
            else:
                report[category] = amount
        report_message = "\nCategory-wise Expense Report:\n" + "\n.join([f"{category}: ${amount}" for category, amount in report.items()])
        self.show_message(report_message)

    def save_budget(self):
        # Save to backend not needed, handled on the fly
        self.show_message("Budget saved successfully.")

    def delete_transaction(self):
        try:
            selected_item = self.transaction_tree.selection()[0]
            transaction_id = int(selected_item)
            response = requests.delete(f'http://127.0.0.1:5000/transactions/{transaction_id}')
            if response.status_code == 204:
                self.transaction_tree.delete(selected_item)
                self.show_message(f"Deleted transaction with id {transaction_id}.")
        except IndexError:
            messagebox.showerror("Error", "No transaction selected.")

    def show_message(self, message):
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        label = tk.Label(self.output_frame, text=message, justify=tk.LEFT)
        label.grid(row=0, column=0, padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
