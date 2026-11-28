from contextlib import redirect_stdout
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tracker import ExpenseTracker, main


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "expenses.csv"
        self.tracker = ExpenseTracker(self.path)

    def test_missing_file_has_no_expenses_and_zero_total(self):
        self.assertEqual(self.tracker.get_expenses(), [])
        self.assertEqual(self.tracker.get_total(), 0)

    def test_add_expense_and_total(self):
        self.tracker.add_expense(450, "lunch")
        self.tracker.add_expense(250, "tea")

        self.assertEqual(self.tracker.get_total(), 700)
        self.assertEqual(
            self.tracker.get_expenses(),
            [{"amount": 450.0, "note": "lunch"}, {"amount": 250.0, "note": "tea"}],
        )

    def test_invalid_expense_is_rejected(self):
        with self.assertRaises(ValueError):
            self.tracker.add_expense(0, "lunch")
        with self.assertRaises(ValueError):
            self.tracker.add_expense(10, " ")

    def test_cli_add_list_and_total(self):
        output = io.StringIO()
        with patch("sys.argv", ["tracker.py", "--file", str(self.path), "add", "450", "lunch"]), redirect_stdout(output):
            main()
        self.assertIn("Added expense.", output.getvalue())

        output = io.StringIO()
        with patch("sys.argv", ["tracker.py", "--file", str(self.path), "list"]), redirect_stdout(output):
            main()
        self.assertIn("1. 450.0 - lunch", output.getvalue())

        output = io.StringIO()
        with patch("sys.argv", ["tracker.py", "--file", str(self.path), "total"]), redirect_stdout(output):
            main()
        self.assertIn("450.0", output.getvalue())


if __name__ == "__main__":
    unittest.main()
