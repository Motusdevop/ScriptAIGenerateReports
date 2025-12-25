"""
Tests for HTTPClient domain class
"""

import pytest
from unittest.mock import MagicMock, patch

from app.domains.lesson_data.client import HTTPClient


@pytest.fixture()
def client(mock_logger):
    """Fixture for client"""
    return HTTPClient(logger=mock_logger)


class TestHTTPClient:
    """Tests for HTTPClient class"""

    def test_request_with_post_data(self, client):
        """Test HTTP request with POST data"""
        # This is an integration test example
        # In real tests, you would mock pycurl or use a test HTTP server

        test_response = "Hello world!!!".encode("windows-1251")

        with patch("app.domains.lesson_data.client.pycurl.Curl") as curl:
            mock_curl = MagicMock()
            curl.return_value = mock_curl

            def write_to_buffer():
                buffer = mock_curl.setopt.call_args_list[1][0][1]
                buffer.write(test_response)

            mock_curl.perform.side_effect = write_to_buffer

            result = client.request("http://example.com", post_data={"key": "value"})

            assert result.encode("windows-1251") == test_response
