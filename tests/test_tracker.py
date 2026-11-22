from pathlib import Path
import tempfile
import unittest

from tracker import ExpenseTracker

class TestExpenseTracker(unittest.TestCase):
    def test_get_total_returns_zero_when_csv_does_not_exist(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
                    missing_csv = Path(tmp_dir) / "expenses.csv"
                    tracker = ExpenseTracker(missing_csv)

                    total = tracker.get_total()

                    self.assertEqual(total, 0.0)

    def test_add_expense_and_get_total(self):
          with tempfile.TemporaryDirectory() as tmp_dir:
                csv_path = Path(tmp_dir) / "expenses.csv"
                tracker = ExpenseTracker(csv_path)

                tracker.add_expense(450.0, "lunch")
                tracker.add_expense(250.0, "tea")

                total = tracker.get_total()

                self.assertEqual(total, 700.0)

    def test_add_expense_negative_amount_raises_error(self):
          with tempfile.TemporaryDirectory() as tmp_dir:
                csv_path = Path(tmp_dir) / "expenses.csv"
                tracker = ExpenseTracker(csv_path)
                
                with self.assertRaises(ValueError):
                    tracker.add_expense(-50.0, "lunch")

    def test_add_expense_empty_note_raises_error(self):
          with tempfile.TemporaryDirectory() as tmp_dir:
                csv_path = Path(tmp_dir) / "expenses.csv"
                tracker = ExpenseTracker(csv_path)

                with self.assertRaises(ValueError):
                    tracker.add_expense(450.0, "")

                with self.assertRaises(ValueError):
                    tracker.add_expense(250.0, "  ")         

    def test_get_total_corrupted_csv_raises_error(self):
            with tempfile.TemporaryDirectory() as tmp_dir:
                csv_path = Path(tmp_dir) / "expenses.csv"
                tracker = ExpenseTracker(csv_path)

                csv_path.write_text("invalid_amount,lunch\n", encoding="utf-8")

                with self.assertRaises(ValueError):
                    tracker.get_total()

    def test_get_expenses_returns_empty_list_when_missing(self):
            with tempfile.TemporaryDirectory() as tmp_dir:
                csv_path = Path(tmp_dir) / "expenses.csv"
                tracker = ExpenseTracker(csv_path)

                expenses = tracker.get_expenses()

                self.assertEqual(expenses, [])

    def test_get_expenses_returns_saved_expenses(self):
            with tempfile.TemporaryDirectory() as tmp_dir:
                csv_path = Path(tmp_dir) / "expenses.csv"
                tracker = ExpenseTracker(csv_path)
              
                tracker.add_expense(450.0, "lunch")
                tracker.add_expense(250.0, "tea")

                expenses = tracker.get_expenses()

                self.assertEqual(expenses, [{"amount": 450.0, "note": "lunch"}, {"amount": 250.0, "note": "tea"}])

          
if __name__ == "__main__":
    unittest.main()