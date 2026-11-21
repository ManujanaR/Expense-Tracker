import csv
from pathlib import Path
import argparse

class ExpenseTracker:
    def __init__(self, csv_path: Path):
        self.csv_path = csv_path # Saves CSV file path


    def add_expense(self, amount: float, note: str):
        with self.csv_path.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([amount, note])


    def get_total(self):
        if not self.csv_path.exists():
            return 0.0
        total = 0.0
        with self.csv_path.open("r", newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row:
                    total += float(row[0])
        return total

def main():
    parser = argparse.ArgumentParser(description="Simple CLI Expense Tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", type=float, help="Expense amount")
    add_parser.add_argument("note", nargs="+", help="Expense note")

    subparsers.add_parser("total", help="Show total expenses")


    args = parser.parse_args()
    tracker = ExpenseTracker(Path("expenses.csv"))

    if args.command == "add":
        tracker.add_expense(args.amount, " ".join(args.note))
        print("Added expense.")
    elif args.command == "total":
        print(tracker.get_total())

if __name__ == "__main__":
    main()
