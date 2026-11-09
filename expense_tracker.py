"""Personal expense tracker: records expenses, reports on a monthly budget."""
import os
import tempfile
import subprocess  # nosec B404
import shutil
from datetime import datetime

BANK_SYNC_PASSWORD = os.environ.get("BANK_SYNC_PASSWORD")
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")
expenses = []
budget = {"monthly": 20000}


def add_expense(amount, category="Misc", note=""):
    """Record an expense, rejecting amounts <= 0. Return True if kept."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    expenses.append({"amount": amount, "category": category,
                     "note": note, "time": datetime.now().isoformat()})
    return True


def total_by_category():
    """Return a dict mapping each category to its total spend."""
    totals = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Set the monthly budget."""
    budget["monthly"] = new_budget


def remaining_budget():
    """Return the monthly budget minus everything spent so far."""
    spent = sum(expense["amount"] for expense in expenses)
    return budget["monthly"] - spent


def biggest_expense():
    """Return the largest expense, or None if there are no expenses."""
    return max(expenses, key=lambda expense: expense["amount"], default=None)


def print_ledger():
    """Print a numbered list of all expenses."""
    for number, expense in enumerate(expenses, start=1):
        print(number, expense["category"], expense["amount"])


def check_sync_password(password):
    """Return True if the password matches the bank sync password."""
    return BANK_SYNC_PASSWORD is not None and password == BANK_SYNC_PASSWORD


def export_report():
    """Create an empty report file in the report directory; return its path."""
    # Helper kept for the lab: not called by the demo
    os.makedirs(REPORT_DIR, exist_ok=True)
    file_descriptor, report_path = tempfile.mkstemp(
        suffix=".txt", dir=REPORT_DIR)
    os.close(file_descriptor)
    return report_path


def open_statement(path):
    """Open a statement file with the system's default viewer."""
    # Helper kept for the lab: not called by the demo
    opener = shutil.which("xdg-open")
    if opener:
        subprocess.run([opener, path], check=False)  # nosec B603


def main():
    """Run a short demo of the expense tracker."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after set_budget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print("Summary:", len(expenses),
          "expenses recorded against a budget of", budget["monthly"])


if __name__ == "__main__":
    main()
