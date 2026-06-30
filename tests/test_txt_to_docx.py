#!/usr/bin/env python3
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.txt_to_docx import txt_to_docx


def test_txt_to_docx_creates_output():
    sample = "Chapter 1\n\nHello world.\n\nChapter 2\n\nAnother scene."
    with tempfile.TemporaryDirectory() as tmpdir:
        input_file = os.path.join(tmpdir, "book.txt")
        output_file = os.path.join(tmpdir, "book.docx")
        with open(input_file, "w", encoding="utf-8") as f:
            f.write(sample)
        result = txt_to_docx(input_file, output_file, "Test", "Author")
        assert result == output_file
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0
