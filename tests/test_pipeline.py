#!/usr/bin/env python3
"""
Tests for pipeline.py — main orchestrator.
All external calls (NovelClaw, txt_to_epub, kdp_upload) are mocked.
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestRunPipelineUnit:
    """Unit tests for run_pipeline with all IO mocked."""

    def _mock_client(self, story_id=42):
        client = MagicMock()
        client.health.return_value = True
        client.create_and_wait.return_value = story_id
        client.export.return_value = None
        return client

    @patch("pipeline.NovelClawClient")
    @patch("pipeline.txt_to_epub")
    def test_pipeline_returns_epub_path(self, mock_epub, mock_nc_cls, tmp_path):
        mock_nc_cls.return_value = self._mock_client()
        mock_epub.return_value = None
        import pipeline
        pipeline.MANUSCRIPTS_DIR = tmp_path / "manuscripts"
        pipeline.EPUB_OUTPUT_DIR = tmp_path / "epub"
        # Create a fake manuscript file so export doesn't fail
        pipeline.MANUSCRIPTS_DIR.mkdir(parents=True)
        pipeline.EPUB_OUTPUT_DIR.mkdir(parents=True)
        (pipeline.MANUSCRIPTS_DIR / "manuscript_42.txt").write_text("chapter text")
        result = pipeline.run_pipeline(
            premise="A hero saves the world",
            title="Hero Tale",
            author="Test Author",
            chapters=5,
            provider="deepseek",
        )
        assert "hero_tale" in result
        assert result.endswith(".epub")

    @patch("pipeline.NovelClawClient")
    def test_pipeline_exits_when_novelclaw_down(self, mock_nc_cls):
        client = MagicMock()
        client.health.return_value = False
        mock_nc_cls.return_value = client
        import pipeline
        with pytest.raises(SystemExit):
            pipeline.run_pipeline(
                premise="A story", title="Book", author="Author",
                chapters=5, provider="deepseek",
            )

    @patch("pipeline.NovelClawClient")
    @patch("pipeline.txt_to_epub")
    def test_pipeline_skip_upload_by_default(self, mock_epub, mock_nc_cls, tmp_path):
        mock_nc_cls.return_value = self._mock_client()
        mock_epub.return_value = None
        import pipeline
        pipeline.MANUSCRIPTS_DIR = tmp_path / "manuscripts"
        pipeline.EPUB_OUTPUT_DIR = tmp_path / "epub"
        pipeline.MANUSCRIPTS_DIR.mkdir(parents=True)
        pipeline.EPUB_OUTPUT_DIR.mkdir(parents=True)
        (pipeline.MANUSCRIPTS_DIR / "manuscript_42.txt").write_text("text")
        with patch("pipeline.upload_to_kdp") as mock_upload:
            pipeline.run_pipeline(
                premise="Story", title="My Book", author="Author",
                chapters=5, upload=False,
            )
            mock_upload.assert_not_called()

    @patch("pipeline.NovelClawClient")
    @patch("pipeline.txt_to_epub")
    def test_pipeline_calls_upload_when_flag_set(self, mock_epub, mock_nc_cls, tmp_path):
        mock_nc_cls.return_value = self._mock_client()
        mock_epub.return_value = None
        import pipeline
        pipeline.MANUSCRIPTS_DIR = tmp_path / "manuscripts"
        pipeline.EPUB_OUTPUT_DIR = tmp_path / "epub"
        pipeline.MANUSCRIPTS_DIR.mkdir(parents=True)
        pipeline.EPUB_OUTPUT_DIR.mkdir(parents=True)
        (pipeline.MANUSCRIPTS_DIR / "manuscript_42.txt").write_text("text")
        with patch("pipeline.asyncio") as mock_asyncio:
            with patch("pipeline.upload_to_kdp") as mock_upload:
                pipeline.run_pipeline(
                    premise="Story", title="My Book", author="Author",
                    chapters=5, upload=True,
                )
                mock_asyncio.run.assert_called_once()
