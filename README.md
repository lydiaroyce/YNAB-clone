# YNAB-clone
# YNAB Clone

This project is a clone of the popular budgeting application YNAB (You Need A Budget). It provides functionality for managing personal finances, including adding income and expenses, viewing transaction history, generating category-wise expense reports, and viewing the overall financial status.

## Features

- **Add Income**: Record your income sources with amounts and categories.
- **Add Expense**: Track your expenses with detailed categories.
- **View Transaction History**: See a list of all recorded transactions.
- **Category-wise Expense Report**: Get a detailed report of expenses by category.
- **View Financial Status**: View total income, total expenses, and current balance.

## Technology Stack

- **Frontend**: `tkinter` (Python)
- **Backend**: Flask (Python)
- **Database**: SQLite (via SQLAlchemy)
- **API Communication**: `requests` (Python)

## Setup

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- Git (for cloning the repository)

### Installation

1. **Clone the Repository**

    ```sh
    git clone https://github.com/lydiaroyce/YNAB-clone.git
    cd YNAB-clone
    ```

2. **Create a Virtual Environment**

    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

    If `requirements.txt` is not present, you can manually install the dependencies:

    ```sh
    pip install Flask Flask-SQLAlchemy requests
    ```

### Running the Application

1. **Start the Flask Server**

    ```sh
    python3 app.py
    ```

    The server will start running at `http://127.0.0.1:5000`.

2. **Run the `tkinter` GUI Application**

    Open a new terminal window while the Flask server is running and execute:

    ```sh
    python3 budget_app_gui.py
    ```

### Usage

- **Add Income/Expense**: Use the input fields and buttons in the GUI to add income and expense records.
- **View Transaction History**: Click the "View History" button to see all transactions.
- **Category-wise Expense Report**: Click the "Category Report" button to generate a report of expenses by category.
- **View Financial Status**: Click the "View Status" button to see the total income, total expenses, and current balance.
- **Save Budget**: Click the "Save" button to save the current state of the budget to a file.
- **Delete Transaction**: Select a transaction from the history and click the "Delete Selected" button to remove it.

### Project Structure

YNAB-clone/
├── app.py # Flask backend application
├── budget_app.py # Core budget application logic
├── budget_app_gui.py # tkinter frontend application
├── commandline.py # Command line interface (optional)
├── test_budget_app.py # Unit tests
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── budget.json # Example data file (if present)


### Contributing

Contributions are welcome! Please fork this repository and submit pull requests with your improvements.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.

### Acknowledgements

- Inspired by the functionality of YNAB (You Need A Budget).

