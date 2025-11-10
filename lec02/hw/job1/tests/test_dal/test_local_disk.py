"""
Tests dal.local_disk.py module
"""

import os
from unittest import TestCase, mock

from lec02.hw.job1.dal.local_disk import save_to_disk


class SaveToDiskTestCase(TestCase):
    """
    Test dal.local_disk.save_to_disk function.

    """


    def setUp(self):
        # Setup test data
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
        self.test_path = "test_output"


    def tearDown(self):
        # Cleanup test files if they exist
        if os.path.exists(self.test_path):
            for file in os.listdir(self.test_path):
                os.remove(os.path.join(self.test_path, file))
            os.rmdir(self.test_path)


    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_save_to_disk_writes_data(self, mock_open):
        # Test that function attempts to write data
        save_to_disk(self.test_data, self.test_path)
        mock_open.assert_called_once()


    def test_save_to_disk_creates_directory(self):
        # Test that function creates directory if it doesn't exist
        if os.path.exists(self.test_path):
            os.rmdir(self.test_path)

        save_to_disk(self.test_data, self.test_path)
        self.assertTrue(os.path.exists(self.test_path))


    def test_save_to_disk_with_empty_data(self):
        # Test handling of empty data
        empty_data = []
        save_to_disk(empty_data, self.test_path)
        # Add assertions based on expected behavior


    def test_save_to_disk_with_invalid_path(self):
        # Test handling of invalid path
        with self.assertRaises(
            Exception
        ):  # Specify exact exception based on implementation
            save_to_disk(self.test_data, "")
