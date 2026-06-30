#!/usr/bin/env python3
"""BookForge AI — Shared utilities used across multiple scripts."""
import re

CHAPTER_RE = re.compile(
    r"(Chapter\s+\d+[:\s\u2014\u2013\-]?[^\n]*|CHAPTER\s+\d+[^\n]*)",
    re.IGNORECASE,
)


def detect_chapters(text: str) -> list[tuple[str, str]]:
    """
    Split manuscript text into (title, body) chapter tuples.
    Falls back to equal-size paragraph chunks when no chapter headings are found.
    """
    parts = CHAPTER_RE.split(text)
    if len(parts) > 1:
        chapters = []
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            body = parts[i + 1].strip() if i + 1 < len(parts) else ""
            chapters.append((title, body))
        return chapters

    # Fallback: split into ~10 equal chunks by paragraph
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return [("Chapter 1", text.strip())]
    chunk = max(1, len(paragraphs) // 10)
    return [
        (f"Chapter {idx + 1}", "\n".join(paragraphs[i : i + chunk]))
        for idx, i in enumerate(range(0, len(paragraphs), chunk))
    ]
