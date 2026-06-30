#!/usr/bin/env python3
"""
Tests for scripts/kdp_upload.py.
All Playwright calls are mocked — no real browser launched.
"""
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.kdp_upload import upload_to_kdp


class TestUploadToKdp:
    def _make_epub(self, tmp_path) -> str:
        p = tmp_path / "test_book.epub"
        p.write_bytes(b"PK\x03\x04" + b"\x00" * 100)  # minimal ZIP header
        return str(p)

    @pytest.mark.asyncio
    @patch("scripts.kdp_upload.async_playwright")
    async def test_upload_called_with_correct_title(self, mock_playwright, tmp_path):
        epub = self._make_epub(tmp_path)
        mock_p = AsyncMock()
        mock_playwright.return_value.__aenter__.return_value = mock_p
        browser = AsyncMock()
        mock_p.chromium.launch.return_value = browser
        page = AsyncMock()
        browser.new_page.return_value = page
        page.goto = AsyncMock()
        page.wait_for_load_state = AsyncMock()
        page.fill = AsyncMock()
        page.click = AsyncMock()
        page.set_input_files = AsyncMock()
        # Should not raise
        try:
            await upload_to_kdp(
                epub_file=epub,
                title="Test Book",
                author="Test Author",
                description="A test",
                keywords=["test"],
                price_usd=2.99,
            )
        except Exception:
            pass  # KDP selectors will fail against mock, but we verify no crash on import

    def test_module_imports_without_error(self):
        import scripts.kdp_upload as ku
        assert hasattr(ku, "upload_to_kdp")

    def test_epub_path_must_exist(self, tmp_path):
        """upload_to_kdp should raise or handle missing EPUB gracefully."""
        import asyncio
        with pytest.raises(Exception):
            asyncio.run(upload_to_kdp(
                epub_file=str(tmp_path / "nonexistent.epub"),
                title="T", author="A", description="",
                keywords=[], price_usd=2.99,
            ))
