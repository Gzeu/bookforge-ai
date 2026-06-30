#!/usr/bin/env python3
"""BookForge AI — Cover Generation Helpers."""
import os
import re
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

SD_WEBUI_URL = os.getenv("SD_WEBUI_URL", "http://127.0.0.1:7860")
CANVA_API_KEY = os.getenv("CANVA_API_KEY", "")
COVERS_DIR = Path(os.getenv("COVERS_DIR", "./covers"))


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "cover"


def build_cover_prompt(
    title: str,
    subtitle: str = "",
    genre: str = "thriller",
    mood: str = "cinematic",
) -> str:
    base = f"Book cover, {genre}, {mood}, dramatic lighting, centered composition, professional typography space"
    if title:
        base += f", title concept: {title}"
    if subtitle:
        base += f", subtitle concept: {subtitle}"
    return base


def generate_cover_metadata(title: str, genre: str, provider: str) -> dict:
    return {
        "title": title,
        "genre": genre,
        "provider": provider,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "size": "1600x2560",
    }


def save_cover_placeholder(
    title: str,
    genre: str,
    provider: str = "placeholder",
    output_dir: Path = None,  # explicit param — avoids global state in tests
) -> dict:
    out = output_dir or COVERS_DIR
    out.mkdir(parents=True, exist_ok=True)
    filename = f"{slugify(title)}-{slugify(genre)}.json"
    path = out / filename
    data = generate_cover_metadata(title, genre, provider)
    data["prompt"] = build_cover_prompt(title, genre=genre)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    data["path"] = str(path)
    return data
