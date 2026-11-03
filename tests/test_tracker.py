import unittest
from unittest.mock import MagicMock, patch
from src.tracker import PriceTracker


class TestPriceTracker(unittest.TestCase):
    @patch("requests.Session.get")
    def test_fetch_price_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"bitcoin": {"usd": 68420.5}}
        mock_get.return_value = mock_response

        tracker = PriceTracker(coin_id="bitcoin", currency="usd")
        price = tracker.fetch_price()

        self.assertEqual(price, 68420.5)

    @patch("requests.Session.get")
    def test_fetch_price_rate_limited(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_get.return_value = mock_response

        tracker = PriceTracker(coin_id="bitcoin", currency="usd")
        price = tracker.fetch_price()

        self.assertIsNone(price)

    @patch("requests.Session.get")
    def test_fetch_price_malformed_json(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"other_token": {"eur": 100}}
        mock_get.return_value = mock_response

        tracker = PriceTracker(coin_id="bitcoin", currency="usd")
        price = tracker.fetch_price()

        self.assertIsNone(price)


if __name__ == "__main__":
    unittest.main()
