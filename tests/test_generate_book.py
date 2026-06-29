#!/usr/bin/env python3
"""
Unit tests for scripts/generate_book.py (mocked — no live NovelClaw needed)
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.generate_book import NovelClawClient


class TestNovelClawClientHealth:
    def test_health_true_on_200(self):
        client = NovelClawClient()
        with patch("scripts.generate_book.requests.get") as mock_get:
            mock_get.return_value = MagicMock(status_code=200)
            assert client.health() is True

    def test_health_false_on_500(self):
        client = NovelClawClient()
        with patch("scripts.generate_book.requests.get") as mock_get:
            mock_get.return_value = MagicMock(status_code=500)
            assert client.health() is False

    def test_health_false_on_exception(self):
        client = NovelClawClient()
        with patch("scripts.generate_book.requests.get", side_effect=Exception("conn refused")):
            assert client.health() is False


class TestNovelClawClientCreateStory:
    def test_create_story_sends_correct_payload(self):
        client = NovelClawClient()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 42, "status": "pending"}
        mock_response.raise_for_status = MagicMock()

        with patch("scripts.generate_book.requests.post", return_value=mock_response) as mock_post:
            result = client.create_story("A spy thriller", chapters=5, provider="deepseek")

        assert result["id"] == 42
        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json") or call_kwargs[0][1]
        assert payload["requested_chapters"] == 5
        assert payload["provider"] == "deepseek"
        assert payload["start"] is True

    def test_export_writes_file(self, tmp_path):
        client = NovelClawClient()
        mock_response = MagicMock()
        mock_response.text = "Chapter 1\n\nOnce upon a time..."
        mock_response.raise_for_status = MagicMock()

        output_file = str(tmp_path / "manuscript.txt")
        with patch("scripts.generate_book.requests.get", return_value=mock_response):
            result = client.export(1, output_file)

        assert os.path.exists(output_file)
        content = open(output_file).read()
        assert "Once upon a time" in content
        assert result == output_file
