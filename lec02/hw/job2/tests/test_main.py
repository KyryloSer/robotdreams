"""
Tests for main.py
"""

from unittest import TestCase, mock

from .. import main


class MainFunctionTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        main.app.testing = True
        cls.client = main.app.test_client()

    @mock.patch("job2.main.save_sales_to_local_disk_as_avro")
    def test_return_400_stg_dir_param_missed(self, get_sales_mock: mock.MagicMock):
        """
        Raise 400 HTTP code when no 'stg_dir' param
        """
        resp = self.client.post(
            "/",
            json={
                "raw_dir": "/foo/bar/",
                # stg_dir отсутствует
            },
        )
        self.assertEqual(400, resp.status_code)
        self.assertIn("stg_dir parameter missed", resp.get_json()["message"])

    @mock.patch("job2.main.save_sales_to_local_disk_as_avro")
    def test_return_400_raw_dir_param_missed(self, get_sales_mock: mock.MagicMock):
        """
        ДRaise 400 HTTP code when no 'raw_dir' param
        """
        resp = self.client.post(
            "/",
            json={
                "stg_dir": "/foo/stg/",
                # raw_dir отсутствует
            },
        )
        self.assertEqual(400, resp.status_code)
        self.assertIn("raw_dir parameter missed", resp.get_json()["message"])

    @mock.patch("job2.main.save_sales_to_local_disk_as_avro")
    def test_save_sales_to_local_disk_called_with_params(
        self, save_mock: mock.MagicMock
    ):
        """
        Test that the BLL function is called with correct parameters.
        """
        fake_stg_dir = "/foo/stg/"
        fake_raw_dir = "/foo/raw/"
        self.client.post(
            "/",
            json={
                "stg_dir": fake_stg_dir,
                "raw_dir": fake_raw_dir,
            },
        )
        save_mock.assert_called_with(stg_dir=fake_stg_dir, raw_dir=fake_raw_dir)

    @mock.patch("job2.main.save_sales_to_local_disk_as_avro")
    def test_return_201_when_all_is_ok(self, _mock: mock.MagicMock):
        """
        Should return 201 when both 'stg_dir' and 'raw_dir' are provided.
        """
        resp = self.client.post(
            "/",
            json={
                "stg_dir": "/foo/stg/",
                "raw_dir": "/foo/raw/",
            },
        )
        self.assertEqual(201, resp.status_code)
        self.assertIn("Data retrieved successfully", resp.get_json()["message"])
