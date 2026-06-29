#!/usr/bin/env python3
"""
BookForge AI — Manuscript to EPUB Converter
Converts NovelClaw TXT output to KDP-ready EPUB.
"""
import re
import os
from pathlib import Path
from datetime import datetime
from ebooklib import epub
from dotenv import load_dotenv

load_dotenv()

KDP_CSS = """
body {
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 1em;
    line-height: 1.7;
    margin: 5% 8%;
    color: #1a1a1a;
}
h1.chapter-title {
    font-size: 1.8em;
    text-align: center;
    margin: 3em 0 2em;
    page-break-before: always;
    font-weight: bold;
    letter-spacing: 0.05em;
}
p {
    text-indent: 1.5em;
    margin: 0 0 0.4em;
    orphans: 3;
    widows: 3;
}
p.first { text-indent: 0; margin-top: 0.5em; }
.scene-break { text-align: center; margin: 1.5em 0; color: #888; }
"""

CHAPTER_RE = re.compile(
    r"(Chapter\\s+\\d+[:\\s\u2014\u2013\\-]?[^\\n]*|CHAPTER\\s+\\d+[^\\n]*)",
    re.IGNORECASE,
)


def detect_chapters(text: str):
    parts = CHAPTER_RE.split(text)
    if len(parts) > 1:
        chapters = []
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            body  = parts[i + 1].strip() if i + 1 < len(parts) else ""
            chapters.append((title, body))
        return chapters
    # fallback: split into ~10 equal chunks
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunk = max(1, len(paragraphs) // 10)
    return [
        (f"Chapter {idx + 1}", "\n".join(paragraphs[i : i + chunk]))
        for idx, i in enumerate(range(0, len(paragraphs), chunk))
    ]


def paragraphs_to_html(body: str) -> str:
    lines = [ln.strip() for ln in body.split("\n") if ln.strip()]
    html = ""
    for i, line in enumerate(lines):
        if line in ("* * *", "---", "***"):
            html += '<p class="scene-break">* * *</p>\n'
        else:
            cls = 'first' if i == 0 else ''
            html += f'<p class="{cls}">{line}</p>\n'
    return html


def txt_to_epub(
    input_file: str,
    output_file: str,
    title: str = "My Novel",
    author: str = "Author Name",
    language: str = "en",
    cover_image: str = None,
    description: str = "",
) -> str:
    text = Path(input_file).read_text(encoding="utf-8")
    chapters = detect_chapters(text)

    book = epub.EpubBook()
    book.set_identifier(f"bookforge-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)
    if description:
        book.add_metadata("DC", "description", description)

    style = epub.EpubItem(
        uid="style",
        file_name="style/main.css",
        media_type="text/css",
        content=KDP_CSS,
    )
    book.add_item(style)

    if cover_image and os.path.exists(cover_image):
        with open(cover_image, "rb") as f:
            book.set_cover("cover.jpg", f.read())

    epub_chapters = []
    for idx, (chap_title, chap_body) in enumerate(chapters, 1):
        c = epub.EpubHtml(
            title=chap_title,
            file_name=f"chapter_{idx:02d}.xhtml",
            lang=language,
        )
        body_html = paragraphs_to_html(chap_body)
        c.content = (
            f'<html><body>'
            f'<h1 class="chapter-title">{chap_title}</h1>\n{body_html}'
            f'</body></html>'
        )
        c.add_item(style)
        book.add_item(c)
        epub_chapters.append(c)

    book.toc = tuple(
        epub.Link(c.file_name, c.title, c.id) for c in epub_chapters
    )
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav"] + epub_chapters

    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(output_file, book)
    print(f"✅ EPUB created: {output_file}  ({len(epub_chapters)} chapters)")
    return output_file


if __name__ == "__main__":
    import typer
    app = typer.Typer()

    @app.command()
    def run(
        input_file: str = typer.Argument(...),
        output_file: str = typer.Argument(...),
        title: str = typer.Option("My Novel"),
        author: str = typer.Option("Author Name"),
        language: str = typer.Option("en"),
        cover: str = typer.Option(None),
        description: str = typer.Option(""),
    ):
        txt_to_epub(input_file, output_file, title, author, language, cover, description)

    app()
