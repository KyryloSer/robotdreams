"""
Tests sales_api.py module.
"""
import json
from pathlib import Path
from unittest import TestCase, mock

from lec02.hw.job2.dal.sales_local_dir import get_sales


class GetSalesLocalDirTestCase(TestCase):
    def setUp(self):
        self.raw_dir = "some_dir"
        self.filename = "sales_2022-08-09.json"

    @mock.patch("job2.dal.sales_local_dir.get_file_name")
    @mock.patch("job2.dal.sales_local_dir.Path.exists", return_value=False)
    def test_returns_empty_when_file_missing(
        self, mock_exists, mock_get_file_name
    ):
        mock_get_file_name.return_value = self.filename

        result = get_sales(self.raw_dir)

        self.assertEqual(result, [])

    @mock.patch("job2.dal.sales_local_dir.get_file_name")
    @mock.patch("job2.dal.sales_local_dir.Path.exists", return_value=True)
    @mock.patch(
        "builtins.open",
        new_callable=mock.mock_open,
        read_data='[{"id": 1}, {"id": 2}]',
    )
    def test_reads_json_file_and_returns_records(
        self, mock_open, mock_exists, mock_get_file_name
    ):
        mock_get_file_name.return_value = "sales_some_dir.json"

        result = get_sales(self.raw_dir)

        self.assertEqual(result, [{"id": 1}, {"id": 2}])

        mock_open.assert_called_once_with(
        Path(self.raw_dir) / "sales_some_dir.json", "r", encoding = "utf-8"

    )

    @mock.patch("job2.dal.sales_local_dir.get_file_name")
    @mock.patch("job2.dal.sales_local_dir.Path.exists", return_value=True)
    @mock.patch(
        "builtins.open",
        new_callable=mock.mock_open,
        read_data="not a json",
    )
    def test_raises_when_json_is_invalid(
        self, mock_open, mock_exists, mock_get_file_name
    ):
        mock_get_file_name.return_value = self.filename

        with self.assertRaises(json.JSONDecodeError):
            _ = get_sales(self.raw_dir)
