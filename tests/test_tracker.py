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


          
if __name__ == "__main__":
    unittest.main()