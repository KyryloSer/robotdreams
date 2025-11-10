import unittest
from datetime import datetime, timedelta

from lec02.utils.validate_date import valid_date


class ValidDateTestCase(unittest.TestCase):
    def test_valid_date_returns_date(self):
        d = valid_date("2023-01-01")
        self.assertEqual(d, datetime(2023, 1, 1).date())

    def test_today_is_allowed(self):
        today = datetime.now().date()
        today_str = today.strftime("%Y-%m-%d")
        self.assertEqual(valid_date(today_str), today)

    def test_future_date_raises(self):
        tomorrow = (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d")
        with self.assertRaises(ValueError):
            valid_date(tomorrow)

    def test_invalid_format_raises(self):
        with self.assertRaises(ValueError):
            valid_date("2023/01/01")

    def test_nonexistent_date_raises(self):
        with self.assertRaises(ValueError):
            valid_date("2023-02-30")
