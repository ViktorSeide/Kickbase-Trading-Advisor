import unittest
from unittest.mock import patch, MagicMock

from kickbase_api.config import get_json_with_token


class TestKickbaseConfig(unittest.TestCase):

    @patch("kickbase_api.config.requests.get")
    def test_successful_request(self, mock_get):

        mock_response = MagicMock()

        mock_response.status_code = 200
        mock_response.json.return_value = {
            "test": "success"
        }

        mock_get.return_value = mock_response

        result = get_json_with_token(
            "https://api.kickbase.com/v4/test",
            "test-token"
        )

        self.assertEqual(
            result,
            {"test": "success"}
        )

        mock_get.assert_called_once()

    @patch("kickbase_api.config.requests.get")
    def test_timeout(self, mock_get):

        import requests

        mock_get.side_effect = requests.exceptions.Timeout()

        with self.assertRaises(RuntimeError) as context:
            get_json_with_token(
                "https://api.kickbase.com/v4/test",
                "test-token"
            )

        self.assertIn(
            "timed out",
            str(context.exception)
        )

    @patch("kickbase_api.config.requests.get")
    def test_http_error(self, mock_get):

        mock_response = MagicMock()

        mock_response.status_code = 401

        http_error = __import__(
            "requests"
        ).exceptions.HTTPError()

        mock_response.raise_for_status.side_effect = http_error

        mock_get.return_value = mock_response

        with self.assertRaises(RuntimeError) as context:
            get_json_with_token(
                "https://api.kickbase.com/v4/test",
                "test-token"
            )

        self.assertIn(
            "HTTP 401",
            str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
