import os
import unittest
from unittest.mock import patch, MagicMock

from kickbase_api import KickbaseAPI


class TestKickbaseAPI(unittest.TestCase):

    @patch("kickbase_api.requests.Session")
    def test_login_success(self, mock_session):
        session = MagicMock()
        mock_session.return_value = session

        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "token": "test-token"
        }

        session.post.return_value = response

        api = KickbaseAPI("test@example.com", "password")

        result = api.login()

        self.assertTrue(result)
        self.assertEqual(api.token, "test-token")

    @patch("kickbase_api.requests.Session")
    def test_login_failure(self, mock_session):
        session = MagicMock()
        mock_session.return_value = session

        response = MagicMock()
        response.status_code = 401
        response.json.return_value = {}

        session.post.return_value = response

        api = KickbaseAPI("test@example.com", "password")

        result = api.login()

        self.assertFalse(result)

    @patch("kickbase_api.requests.Session")
    def test_get_market(self, mock_session):
        session = MagicMock()
        mock_session.return_value = session

        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {
            "players": [
                {
                    "id": "123",
                    "firstName": "Test",
                    "lastName": "Player",
                    "marketValue": 10000000
                }
            ]
        }

        session.get.return_value = response

        api = KickbaseAPI("test@example.com", "password")
        api.token = "test-token"

        result = api.get_market("league123")

        self.assertIsNotNone(result)
        self.assertEqual(len(result["players"]), 1)


if __name__ == "__main__":
    unittest.main()
