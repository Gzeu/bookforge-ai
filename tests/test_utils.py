#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.utils import detect_chapters

SAMPLE_WITH_CHAPTERS = """
Chapter 1: The Beginning

This is the first paragraph of chapter one.

Chapter 2: The Middle

This is the second chapter content.

Chapter 3: The End

Final chapter text here.
"""

SAMPLE_NO_CHAPTERS = "\n\n".join([
    f"Paragraph number {i} with enough content to be meaningful."
    for i in range(1, 25)
])


class TestDetectChapters:
    def test_detects_named_chapters(self):
        chapters = detect_chapters(SAMPLE_WITH_CHAPTERS)
        assert len(chapters) == 3

    def test_chapter_titles_correct(self):
        chapters = detect_chapters(SAMPLE_WITH_CHAPTERS)
        assert "Chapter 1" in chapters[0][0]
        assert "Chapter 2" in chapters[1][0]

    def test_body_not_empty(self):
        chapters = detect_chapters(SAMPLE_WITH_CHAPTERS)
        for _, body in chapters:
            assert len(body) > 0

    def test_fallback_no_chapters(self):
        chapters = detect_chapters(SAMPLE_NO_CHAPTERS)
        assert len(chapters) >= 1
        for title, _ in chapters:
            assert title.startswith("Chapter")

    def test_empty_string_returns_list(self):
        chapters = detect_chapters("")
        assert isinstance(chapters, list)
        assert len(chapters) == 1

    def test_deduplication_epub_docx_same_result(self):
        """EPUB and DOCX converters now share detect_chapters — same output guaranteed."""
        from scripts.txt_to_epub import detect_chapters as epub_fn
        # txt_to_epub imports from utils — this is the same function
        assert epub_fn is detect_chapters
