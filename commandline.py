import json
from datetime import datetime

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
    def __init__(self):
        self.transactions = []

    def add_income(self, amount, category, date=None):
        if amount <= 0:
            print("Income amount must be positive.")
            return
        self.transactions.append(Transaction("income", amount, category, date))
        print(f"Added income: ${amount} in {category} category on {date if date else datetime.now().strftime('%Y-%m-%d')}")

    def add_expense(self, amount, category, date=None):
        if amount <= 0:
            print("Expense amount must be positive.")
            return
        self.transactions.append(Transaction("expense", amount, category, date))
        print(f"Added expense: ${amount} in {category} category on {date if date else datetime.now().strftime('%Y-%m-%d')}")

    def view_status(self):
        total_income = sum(t.amount for t in self.transactions if t.trans_type == "income")
        total_expense = sum(t.amount for t in self.transactions if t.trans_type == "expense")
        balance = total_income - total_expense
        print(f"Total Income: ${total_income}")
        print(f"Total Expense: ${total_expense}")
        print(f"Balance: ${balance}")

    def view_history(self):
        if not self.transactions:
            print("No transactions available.")
            return
        for t in self.transactions:
            print(f"{t.date}: {t.trans_type} - ${t.amount} ({t.category})")

    def save_to_file(self, file_path):
        with open(file_path, "w") as file:
            json.dump([t.to_dict() for t in self.transactions], file)
        print(f"Budget saved to {file_path}")

    def load_from_file(self, file_path):
        try:
            with open(file_path, "r") as file:
                self.transactions = [Transaction.from_dict(t) for t in json.load(file)]
            print(f"Budget loaded from {file_path}")
        except FileNotFoundError:
            print("File not found. Starting with an empty budget.")

def main():
    budget = Budget()
    budget.load_from_file("budget.json")

    while True:
        print("\n1. Add Income\n2. Add Expense\n3. View Status\n4. View History\n5. Save and Exit\n")
        choice = input("Choose an option: ")

        if choice == '1':
            try:
                amount = float(input("Enter income amount: "))
                category = input("Enter category: ")
                date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
                budget.add_income(amount, category, date if date else None)
            except ValueError:
                print("Invalid amount entered. Please enter a numerical value.")
        elif choice == '2':
            try:
                amount = float(input("Enter expense amount: "))
                category = input("Enter category: ")
                date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
                budget.add_expense(amount, category, date if date else None)
            except ValueError:
                print("Invalid amount entered. Please enter a numerical value.")
        elif choice == '3':
            budget.view_status()
        elif choice == '4':
            budget.view_history()
        elif choice == '5':
            budget.save_to_file("budget.json")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
