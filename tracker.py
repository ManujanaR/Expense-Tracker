import argparse
import csv
from pathlib import Path


class ExpenseTracker:
    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)

    def add_expense(self, amount, note):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        if not note.strip():
            raise ValueError("Note cannot be empty.")

        with self.csv_path.open("a", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow([amount, note])

    def get_expenses(self):
        if not self.csv_path.exists():
            return []

        with self.csv_path.open(newline="", encoding="utf-8") as file:
            return [{"amount": float(row[0]), "note": row[1]} for row in csv.reader(file) if row]

    def get_total(self):
        return sum(expense["amount"] for expense in self.get_expenses())


def main():
    parser = argparse.ArgumentParser(description="Simple CLI Expense Tracker")
    parser.add_argument("--file", "-f", default="expenses.csv", help="CSV file path")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Add an expense")
    add.add_argument("amount", type=float)
    add.add_argument("note", nargs="+")
    commands.add_parser("total", help="Show total expenses")
    commands.add_parser("list", help="List expenses")
    args = parser.parse_args()
    tracker = ExpenseTracker(args.file)

    try:
        if args.command == "add":
            tracker.add_expense(args.amount, " ".join(args.note))
            print("Added expense.")
        elif args.command == "total":
            print(tracker.get_total())
        else:
            expenses = tracker.get_expenses()
            if not expenses:
                print("No expenses found.")
            for index, expense in enumerate(expenses, start=1):
                print(f"{index}. {expense['amount']} - {expense['note']}")
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
