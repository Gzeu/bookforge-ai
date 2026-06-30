#!/usr/bin/env python3
import os
import sys
from unittest.mock import patch, MagicMock
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.webhooks import send_discord_webhook, send_json_webhook


class TestDiscordWebhook:
    def test_returns_status_on_success(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 204
        mock_resp.raise_for_status = MagicMock()
        with patch("scripts.webhooks.requests.post", return_value=mock_resp):
            assert send_discord_webhook("https://fake-url", "hello") == 204

    def test_returns_zero_on_timeout(self):
        with patch("scripts.webhooks.requests.post", side_effect=requests.exceptions.Timeout()):
            assert send_discord_webhook("https://fake-url", "hello") == 0

    def test_returns_zero_on_connection_error(self):
        with patch("scripts.webhooks.requests.post", side_effect=requests.exceptions.ConnectionError()):
            assert send_discord_webhook("https://fake-url", "hello") == 0

    def test_does_not_raise_on_failure(self):
        with patch("scripts.webhooks.requests.post", side_effect=Exception("unexpected")):
            result = send_discord_webhook("https://fake-url", "hello")
            assert result == 0


class TestJsonWebhook:
    def test_returns_status_on_success(self):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.raise_for_status = MagicMock()
        with patch("scripts.webhooks.requests.post", return_value=mock_resp):
            assert send_json_webhook("https://fake-url", {"event": "done"}) == 200

    def test_returns_zero_on_timeout(self):
        with patch("scripts.webhooks.requests.post", side_effect=requests.exceptions.Timeout()):
            assert send_json_webhook("https://fake-url", {}) == 0
