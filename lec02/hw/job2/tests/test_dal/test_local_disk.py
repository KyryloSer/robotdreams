"""
Tests dal.local_disk.py module
"""

import os
from unittest import TestCase, mock

from lec02.hw.job2.dal.local_disk import save_to_avro, PARSED_SCHEMA


class SaveToDiskTestCase(TestCase):
    """
    Test dal.local_disk.save_to_disk function.

    """

    def setUp(self):
        self.test_data = [
            {
                "client": "John",
                "purchase_date": "2023-01-01",
                "product": "apple",
                "price": 100,
            },
            {
                "client": "Jane",
                "purchase_date": "2023-01-02",
                "product": "banana",
                "price": 200,
            },
        ]
        self.test_path = "out_avro"
        self.file_path = os.path.join(self.test_path, "sales.avro")


    def tearDown(self):
        try:
            if os.path.exists(self.test_path):
                for f in os.listdir(self.test_path):
                    os.remove(os.path.join(self.test_path, f))
                os.rmdir(self.test_path)
        except Exception:
            pass


    @mock.patch("lec02.hw.job2.dal.local_disk.writer")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("lec02.hw.job2.dal.local_disk.prepare_and_get_file_path")
    def test_writer_called_with_parsed_schema_and_records(
        self, mock_prepare, mock_open, mock_writer
    ):
        mock_prepare.return_value = self.file_path

        save_to_avro(self.test_data, self.test_path)

        mock_prepare.assert_called_once_with(self.test_path, extension="avro")
        mock_open.assert_called_once_with(self.file_path, "wb")

        self.assertTrue(mock_writer.called)
        called_args = mock_writer.call_args[0]
        self.assertIs(called_args[1], PARSED_SCHEMA)
        self.assertEqual(called_args[2], self.test_data)


    @mock.patch("lec02.hw.job2.dal.local_disk.writer")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("lec02.hw.job2.dal.local_disk.prepare_and_get_file_path")
    def test_handles_empty_records_calls_writer_with_empty_list(
        self, mock_prepare, mock_open, mock_writer
    ):
        mock_prepare.return_value = self.file_path

        save_to_avro([], self.test_path)

        mock_prepare.assert_called_once_with(self.test_path, extension="avro")
        self.assertTrue(mock_writer.called)
        called_args = mock_writer.call_args[0]
        self.assertIs(called_args[1], PARSED_SCHEMA)
        self.assertEqual(called_args[2], [])


    @mock.patch("lec02.hw.job2.dal.local_disk.prepare_and_get_file_path")
    def test_prepare_raises_propagates_error(self, mock_prepare):
        mock_prepare.side_effect = ValueError("invalid path")

        with self.assertRaises(ValueError):
            save_to_avro(self.test_data, "")
