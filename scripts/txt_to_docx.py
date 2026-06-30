#!/usr/bin/env python3
"""BookForge AI — TXT to DOCX export for paperback workflows."""
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from scripts.utils import detect_chapters  # shared, deduped


def txt_to_docx(
    input_file: str,
    output_file: str,
    title: str = "My Novel",
    author: str = "Author Name",
) -> str:
    text = Path(input_file).read_text(encoding="utf-8")
    chapters = detect_chapters(text)
    doc = Document()

    # Title page
    title_p = doc.add_paragraph()
    title_run = title_p.add_run(title)
    title_run.bold = True
    title_run.font.size = Pt(22)
    doc.add_paragraph(author)
    doc.add_page_break()

    for chapter_title, chapter_body in chapters:
        h = doc.add_paragraph()
        r = h.add_run(chapter_title)
        r.bold = True
        r.font.size = Pt(18)
        for line in [ln.strip() for ln in chapter_body.split("\n") if ln.strip()]:
            if line in ("* * *", "***", "---"):
                p = doc.add_paragraph("* * *")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                doc.add_paragraph(line)
        doc.add_page_break()

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_file)
    return output_file
