#!/usr/bin/env python3
"""
BookForge AI — Cover Generator.
Supports multiple layout presets: minimal, bold, noir, romance, scifi.
Backends: Stable Diffusion WebUI (local) or Canva API.
"""
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SD_WEBUI_URL = os.getenv("SD_WEBUI_URL", "http://localhost:7860")
CANVA_API_KEY = os.getenv("CANVA_API_KEY", "")
_DEFAULT_COVERS_DIR = Path(os.getenv("COVERS_DIR", "./covers"))

# KDP-safe cover size: 2560x1600 px (1.6:1 ratio)
KDP_WIDTH = 2560
KDP_HEIGHT = 1600

COVER_PRESETS: dict[str, dict] = {
    "minimal": {
        "description": "Clean white background, large title, minimal decoration",
        "style_prompt": "minimalist book cover, clean typography, white background, elegant",
        "negative_prompt": "cluttered, busy, dark, violent",
    },
    "bold": {
        "description": "High-contrast, strong colors, impactful title",
        "style_prompt": "bold graphic book cover, high contrast colors, strong typography, dramatic",
        "negative_prompt": "pastel, soft, blurry",
    },
    "noir": {
        "description": "Dark, moody, shadows — ideal for Thriller/Crime/Mystery",
        "style_prompt": "noir book cover, dark moody atmosphere, shadows, cinematic lighting, thriller",
        "negative_prompt": "bright, cheerful, colorful",
    },
    "romance": {
        "description": "Warm tones, soft bokeh, romantic atmosphere",
        "style_prompt": "romance novel cover, warm soft colors, bokeh, intimate, beautiful",
        "negative_prompt": "dark, violent, scary",
    },
    "scifi": {
        "description": "Futuristic, space, neon, technological",
        "style_prompt": "sci-fi book cover, futuristic, space, neon lights, technological, epic",
        "negative_prompt": "medieval, fantasy, nature",
    },
    "fantasy": {
        "description": "Magical, epic landscapes, mystical elements",
        "style_prompt": "fantasy book cover, magical landscape, epic, mystical, detailed artwork",
        "negative_prompt": "modern, technology, urban",
    },
}

# Genre → default preset mapping
GENRE_PRESET_MAP: dict[str, str] = {
    "thriller": "noir",
    "mystery": "noir",
    "crime": "noir",
    "horror": "noir",
    "romance": "romance",
    "paranormal": "romance",
    "scifi": "scifi",
    "fantasy": "fantasy",
    "literary": "minimal",
    "self_help": "minimal",
    "business": "bold",
    "memoir": "minimal",
}


def get_preset(genre_id: str = None, preset_name: str = None) -> dict:
    """Return preset dict by name, or auto-select based on genre ID."""
    if preset_name and preset_name in COVER_PRESETS:
        return COVER_PRESETS[preset_name]
    if genre_id:
        mapped = GENRE_PRESET_MAP.get(genre_id.lower(), "bold")
        return COVER_PRESETS[mapped]
    return COVER_PRESETS["bold"]


def build_cover_prompt(title: str, author: str, genre_id: str = None,
                       subtitle: str = "", preset_name: str = None) -> dict:
    """Build a full SD prompt dict for a book cover."""
    preset = get_preset(genre_id, preset_name)
    prompt = (
        f"{preset['style_prompt']}, "
        f"book title '{title}'{f', subtitle {subtitle}' if subtitle else ''}, "
        f"author name '{author}', professional book cover design, KDP ready"
    )
    return {
        "prompt": prompt,
        "negative_prompt": preset["negative_prompt"] + ", text errors, blurry text",
        "width": KDP_WIDTH,
        "height": KDP_HEIGHT,
        "steps": 30,
        "cfg_scale": 7,
    }


def generate_cover_sd(title: str, author: str, genre_id: str = None,
                      subtitle: str = "", preset_name: str = None,
                      output_dir: Path = None) -> dict:
    """Generate cover using local Stable Diffusion WebUI."""
    import requests
    import base64
    from PIL import Image
    import io

    out_dir = output_dir or _DEFAULT_COVERS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    params = build_cover_prompt(title, author, genre_id, subtitle, preset_name)
    payload = {"prompt": params["prompt"], "negative_prompt": params["negative_prompt"],
               "width": params["width"], "height": params["height"],
               "steps": params["steps"], "cfg_scale": params["cfg_scale"]}

    try:
        resp = requests.post(f"{SD_WEBUI_URL}/sdapi/v1/txt2img", json=payload, timeout=120)
        resp.raise_for_status()
        img_b64 = resp.json()["images"][0]
        img = Image.open(io.BytesIO(base64.b64decode(img_b64)))
        safe = title.lower().replace(" ", "_")[:20]
        out_path = out_dir / f"cover_{safe}.png"
        img.save(str(out_path))
        logger.info(f"Cover saved: {out_path}")
        return {"path": str(out_path), "backend": "stable_diffusion",
                "preset": preset_name or "auto", "title": title}
    except Exception as e:
        logger.warning(f"SD cover generation failed: {e}. Falling back to placeholder.")
        return save_cover_placeholder(title, author, output_dir=out_dir)


def save_cover_placeholder(title: str, author: str = "",
                           output_dir: Path = None) -> dict:
    """Create a minimal placeholder PNG cover using Pillow."""
    from PIL import Image, ImageDraw, ImageFont

    out_dir = output_dir or _DEFAULT_COVERS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (KDP_WIDTH, KDP_HEIGHT), color=(30, 30, 46))
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
        font_author = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 70)
    except OSError:
        font_title = ImageFont.load_default()
        font_author = font_title

    # Title centered
    draw.text((KDP_WIDTH // 2, KDP_HEIGHT // 3), title,
              fill=(255, 255, 255), font=font_title, anchor="mm")
    if author:
        draw.text((KDP_WIDTH // 2, KDP_HEIGHT * 2 // 3), f"by {author}",
                  fill=(180, 180, 200), font=font_author, anchor="mm")

    safe = title.lower().replace(" ", "_")[:20]
    out_path = out_dir / f"cover_{safe}_placeholder.png"
    img.save(str(out_path))
    return {"path": str(out_path), "backend": "placeholder", "title": title}
