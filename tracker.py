import argparse  # Terminal commands saha arguments kiyawanna
import csv  # CSV files liyanna saha kiyawanna
from pathlib import Path  # File paths lesiyen handle karanna


class ExpenseTracker:
    """CSV file ekaka expenses save karana saha total hoyana class eka."""

    def __init__(self, csv_path: Path):
        # Object eka hadenakota dena CSV path eka object ekata save karanawa
        self.csv_path = csv_path

    def add_expense(self, amount: float, note: str):
        # "a" (append) mode eken open karanne parana rows makannathuwa agata add karanna
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        with self.csv_path.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([amount, note])  # [amount, note] row ekak liyanawa

    def get_total(self) -> float:
        # CSV file eka thama hadila naththam 0.0 return karanawa
        if not self.csv_path.exists():
            return 0.0

        total = 0.0  # Mulika ekathuwa (float)

        # "r" (read) mode eken open karala hama row ekakama amount eka ekathu karanawa
        with self.csv_path.open("r", newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row:  # His (empty) rows thibunoth skip karanawa
                    total += float(row[0])  # Patham column eka (amount) float karala ekathu karanawa

        return total  # Loop eka iwara wunata passe thamai total return karanne


def main():
    # Main CLI parser eka hadanawa
    parser = argparse.ArgumentParser(description="Simple CLI Expense Tracker")
    # `add` saha `total` wage subcommands hadanna subparsers gananawa
    subparsers = parser.add_subparsers(dest="command", required=True)

    # `add` command ekata `amount` (number) saha `note` (words ekak ho godak) denawa
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("amount", type=float, help="Expense amount")
    add_parser.add_argument("note", nargs="+", help="Expense note")

    # `total` command eka hadanawa
    subparsers.add_parser("total", help="Show total expenses")

    # Terminal eken dunna arguments parse karala tracker object eka hadanawa
    args = parser.parse_args()
    tracker = ExpenseTracker(Path("expenses.csv"))

    # Thoragatta command eka anuwa adala method eka run karanawa
    if args.command == "add":
        # `nargs="+"` nisa `args.note` list ekak widiyata enawa; `" ".join(...)` walin string karanawa
        tracker.add_expense(args.amount, " ".join(args.note))
        print("Added expense.")
    elif args.command == "total":
        print(tracker.get_total())


# File eka kelinma run kaloth witharak main() call wenawa (import kaloth auto run wenne na)
if __name__ == "__main__":
    main()