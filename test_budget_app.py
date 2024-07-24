import unittest
from budget_app_gui import Budget, Transaction

class TestTransaction(unittest.TestCase):
    def test_transaction_creation(self):
        transaction = Transaction("income", 1000, "Salary", "2024-07-24")
        self.assertEqual(transaction.trans_type, "income")
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.category, "Salary")
        self.assertEqual(transaction.date, "2024-07-24")

    def test_transaction_to_dict(self):
        transaction = Transaction("expense", 50, "Groceries", "2024-07-24")
        self.assertEqual(transaction.to_dict(), {
            "trans_type": "expense",
            "amount": 50,
            "category": "Groceries",
            "date": "2024-07-24"
        })

    def test_transaction_from_dict(self):
        data = {
            "trans_type": "income",
            "amount": 200,
            "category": "Freelance",
            "date": "2024-07-24"
        }
        transaction = Transaction.from_dict(data)
        self.assertEqual(transaction.trans_type, "income")
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.category, "Freelance")
        self.assertEqual(transaction.date, "2024-07-24")

class TestBudget(unittest.TestCase):
    def setUp(self):
        self.budget = Budget()

    def test_add_income(self):
        self.budget.add_income(1000, "Salary", "2024-07-24")
        self.assertEqual(len(self.budget.transactions), 1)
        self.assertEqual(self.budget.transactions[0].trans_type, "income")
        self.assertEqual(self.budget.transactions[0].amount, 1000)

    def test_add_expense(self):
        self.budget.add_expense(100, "Groceries", "2024-07-24")
        self.assertEqual(len(self.budget.transactions), 1)
        self.assertEqual(self.budget.transactions[0].trans_type, "expense")
        self.assertEqual(self.budget.transactions[0].amount, 100)

    def test_view_status(self):
        self.budget.add_income(1000, "Salary", "2024-07-24")
        self.budget.add_expense(200, "Groceries", "2024-07-24")
        total_income, total_expense, balance = self.budget.view_status()
        self.assertEqual(total_income, 1000)
        self.assertEqual(total_expense, 200)
        self.assertEqual(balance, 800)

    def test_save_and_load(self):
        self.budget.add_income(1000, "Salary", "2024-07-24")
        self.budget.add_expense(200, "Groceries", "2024-07-24")
        self.budget.save_to_file("test_budget.json")
        new_budget = Budget()
        new_budget.load_from_file("test_budget.json")
        self.assertEqual(len(new_budget.transactions), 2)
        self.assertEqual(new_budget.transactions[0].trans_type, "income")
        self.assertEqual(new_budget.transactions[1].trans_type, "expense")

if __name__ == "__main__":
    unittest.main()
