"""
Tests sales_api.py module.
"""

import requests
from unittest import TestCase, mock

# NB: avoid relative imports when you will write your code:
from lec02.hw.job1.dal.sales_api import get_sales, API_URL


def _make_response(json_value=None, json_side_effect=None, raise_side_effect=None):
    resp = mock.Mock()
    if raise_side_effect:
        resp.raise_for_status.side_effect = raise_side_effect
    else:
        resp.raise_for_status.return_value = None
    if json_side_effect:
        resp.json.side_effect = json_side_effect
    else:
        resp.json.return_value = json_value
    return resp


class GetSalesTestCase(TestCase):
    def setUp(self):
        self.date = "2023-01-01"

    @mock.patch.dict("os.environ", {"AUTH_TOKEN": "token123"})
    @mock.patch("lec02.hw.job1.dal.sales_api.requests.get")
    def test_paginates_and_returns_combined(self, mock_get):
        # page1 -> data1, page2 -> data2, page3 -> []
        data1 = [{"id": 1}]
        data2 = [{"id": 2}]
        r1 = _make_response(json_value=data1)
        r2 = _make_response(json_value=data2)
        r3 = _make_response(json_value=[])
        mock_get.side_effect = [r1, r2, r3]

        result = get_sales(self.date)

        self.assertEqual(result, data1 + data2)
        # three calls: page=1,2,3
        self.assertEqual(mock_get.call_count, 3)
        expected_url1 = f"{API_URL}sales?date={self.date}&page=1"
        expected_url2 = f"{API_URL}sales?date={self.date}&page=2"
        called_urls = [call.args[0] for call in mock_get.call_args_list]
        self.assertEqual(called_urls[0], expected_url1)
        self.assertEqual(called_urls[1], expected_url2)
        # headers include AUTH_TOKEN
        called_headers = [
            call.kwargs.get("headers") for call in mock_get.call_args_list
        ]
        self.assertTrue(all(h == {"Authorization": "token123"} for h in called_headers))

    @mock.patch.dict("os.environ", {"AUTH_TOKEN": "token123"})
    @mock.patch("job1.dal.sales_api.requests.get")
    def test_stops_on_http_error_and_returns_empty(self, mock_get):
        # Simulate raise_for_status raising HTTPError on first call
        r = _make_response(raise_side_effect=requests.exceptions.HTTPError())
        mock_get.return_value = r

        result = get_sales(self.date)

        self.assertEqual(result, [])
        mock_get.assert_called_once()

    @mock.patch.dict("os.environ", {"AUTH_TOKEN": "token123"})
    @mock.patch("job1.dal.sales_api.requests.get")
    def test_stops_on_json_decode_error_and_returns_empty(self, mock_get):
        # Simulate response.json raising JSONDecodeError
        json_err = requests.JSONDecodeError("Expecting value", "doc", 0)
        r = _make_response(json_side_effect=json_err)
        mock_get.return_value = r

        result = get_sales(self.date)

        self.assertEqual(result, [])
        mock_get.assert_called_once()

    @mock.patch("job1.dal.sales_api.requests.get")
    def test_missing_auth_token_sets_none_header(self, mock_get):
        # Ensure Authorization header is present (but None) when env var missing
        r = _make_response(json_value=[])
        mock_get.return_value = r

        result = get_sales(self.date)

        self.assertEqual(result, [])
        mock_get.assert_called_once()
        called_headers = mock_get.call_args.kwargs.get("headers")
        self.assertIn("Authorization", called_headers)
        self.assertIsNone(called_headers["Authorization"])
