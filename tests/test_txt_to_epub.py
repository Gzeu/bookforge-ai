#!/usr/bin/env python3
"""
Unit tests for scripts/txt_to_epub.py
"""
import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.txt_to_epub import detect_chapters, paragraphs_to_html, txt_to_epub


SAMPLE_WITH_CHAPTERS = """
Chapter 1: The Beginning

This is the first paragraph of chapter one.
It continues here with more text.

Chapter 2: The Middle

This is the second chapter opening.
More content follows in this chapter.

Chapter 3: The End

Final chapter begins here.
The story concludes.
"""

SAMPLE_NO_CHAPTERS = """
First big paragraph that stands on its own.

Second big paragraph with more content here.

Third paragraph continues the story.

Fourth paragraph adds more detail to the narrative.

Fifth paragraph wraps up this section nicely.
"""


class TestDetectChapters:
    def test_detects_named_chapters(self):
        chapters = detect_chapters(SAMPLE_WITH_CHAPTERS)
        assert len(chapters) == 3
        assert "Chapter 1" in chapters[0][0]
        assert "Chapter 2" in chapters[1][0]
        assert "Chapter 3" in chapters[2][0]

    def test_fallback_no_chapters(self):
        chapters = detect_chapters(SAMPLE_NO_CHAPTERS)
        assert len(chapters) >= 1
        for title, body in chapters:
            assert title.startswith("Chapter")

    def test_chapter_body_not_empty(self):
        chapters = detect_chapters(SAMPLE_WITH_CHAPTERS)
        for _, body in chapters:
            assert len(body) > 0

    def test_empty_string(self):
        chapters = detect_chapters("")
        assert isinstance(chapters, list)


class TestParagraphsToHtml:
    def test_basic_paragraph(self):
        html = paragraphs_to_html("Hello world.")
        assert "<p" in html
        assert "Hello world." in html

    def test_scene_break(self):
        html = paragraphs_to_html("Before.\n* * *\nAfter.")
        assert 'scene-break' in html

    def test_first_paragraph_class(self):
        html = paragraphs_to_html("First line.\nSecond line.")
        assert 'class="first"' in html

    def test_multiple_paragraphs(self):
        html = paragraphs_to_html("Para one.\nPara two.\nPara three.")
        assert html.count("<p") == 3


class TestTxtToEpub:
    def test_creates_epub_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.txt")
            output_file = os.path.join(tmpdir, "output.epub")
            with open(input_file, "w", encoding="utf-8") as f:
                f.write(SAMPLE_WITH_CHAPTERS)
            result = txt_to_epub(input_file, output_file, "Test Book", "Test Author")
            assert os.path.exists(output_file)
            assert result == output_file
            assert os.path.getsize(output_file) > 1000

    def test_epub_with_no_chapter_headings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "flat.txt")
            output_file = os.path.join(tmpdir, "flat.epub")
            with open(input_file, "w", encoding="utf-8") as f:
                f.write(SAMPLE_NO_CHAPTERS)
            result = txt_to_epub(input_file, output_file)
            assert os.path.exists(output_file)

    def test_creates_output_dir_if_missing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.txt")
            output_file = os.path.join(tmpdir, "subdir", "nested", "out.epub")
            with open(input_file, "w", encoding="utf-8") as f:
                f.write(SAMPLE_WITH_CHAPTERS)
            txt_to_epub(input_file, output_file)
            assert os.path.exists(output_file)
