from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tracker import ExpenseTracker, main

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

    def test_cli_list_no_expenses_prints_message(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "expenses.csv"
            buf = io.StringIO()

            with patch("sys.argv", ["tracker.py", "list"]), \
                patch("tracker.ExpenseTracker", return_value=ExpenseTracker(csv_path)), \
                redirect_stdout(buf):
                main()

            self.assertIn("No expenses found.", buf.getvalue())

    def test_cli_list_prints_saved_expenses(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "expenses.csv"
            tracker = ExpenseTracker(csv_path)
            tracker.add_expense(450.0, "lunch")
            tracker.add_expense(250.0, "tea")

            buf = io.StringIO()
            with patch("sys.argv", ["tracker.py", "list"]), \
                patch("tracker.ExpenseTracker", return_value=tracker), \
                redirect_stdout(buf):
                main()

            output = buf.getvalue()
            self.assertIn("450.0 - lunch", output)
            self.assertIn("250.0 - tea", output)    
    def test_cli_add_command_saves_expense_and_prints_message(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "expenses.csv"
            tracker = ExpenseTracker(csv_path)
            buf = io.StringIO()

            with patch("sys.argv", ["tracker.py", "add", "450.0", "lunch"]), \
                 patch("tracker.ExpenseTracker", return_value=tracker), \
                 redirect_stdout(buf):
                main()

            self.assertIn("Added expense.", buf.getvalue())
            self.assertEqual(tracker.get_expenses(), [{"amount": 450.0, "note": "lunch"}])

    def test_cli_total_command_prints_total(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "expenses.csv"
            tracker = ExpenseTracker(csv_path)
            tracker.add_expense(450.0, "lunch")
            tracker.add_expense(250.0, "tea")

            buf = io.StringIO()
            with patch("sys.argv", ["tracker.py", "total"]), \
                 patch("tracker.ExpenseTracker", return_value=tracker), \
                 redirect_stdout(buf):
                main()

        self.assertIn("700.0", buf.getvalue())
if __name__ == "__main__":
    unittest.main()
