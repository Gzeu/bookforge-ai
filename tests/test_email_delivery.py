#!/usr/bin/env python3
import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.email_delivery import EmailDelivery


class TestEmailDelivery:
    def test_send_epub_missing_file_returns_false(self):
        ed = EmailDelivery(host="smtp.test", port=587, user="u", password="p")
        result = ed.send_epub("dest@test.com", "/nonexistent/book.epub", title="T")
        assert result is False

    @patch("scripts.email_delivery.smtplib.SMTP")
    def test_send_epub_success(self, mock_smtp_cls, tmp_path):
        epub = tmp_path / "book.epub"
        epub.write_bytes(b"PK\x03\x04" + b"0" * 50)
        mock_server = MagicMock()
        mock_smtp_cls.return_value.__enter__.return_value = mock_server
        ed = EmailDelivery(host="smtp.test", port=587, user="u@t.com", password="pw")
        result = ed.send_epub("dest@test.com", str(epub), title="My Book", author="Author")
        assert result is True
        mock_server.sendmail.assert_called_once()

    @patch("scripts.email_delivery.smtplib.SMTP")
    def test_send_epub_smtp_auth_error_returns_false(self, mock_smtp_cls, tmp_path):
        import smtplib
        epub = tmp_path / "book.epub"
        epub.write_bytes(b"data")
        mock_smtp_cls.return_value.__enter__.side_effect = smtplib.SMTPAuthenticationError(535, b"auth fail")
        ed = EmailDelivery(host="smtp.test", port=587, user="u", password="wrong")
        result = ed.send_epub("d@t.com", str(epub))
        assert result is False

    @patch("scripts.email_delivery.smtplib.SMTP")
    def test_test_connection_success(self, mock_smtp_cls):
        mock_server = MagicMock()
        mock_smtp_cls.return_value.__enter__.return_value = mock_server
        ed = EmailDelivery(host="smtp.test", port=587, user="u", password="p")
        assert ed.test_connection() is True

    @patch("scripts.email_delivery.smtplib.SMTP")
    def test_test_connection_failure(self, mock_smtp_cls):
        mock_smtp_cls.return_value.__enter__.side_effect = Exception("refused")
        ed = EmailDelivery(host="smtp.test", port=587, user="u", password="p")
        assert ed.test_connection() is False
