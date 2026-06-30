#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.cover_generator import (
    build_cover_prompt, get_preset, save_cover_placeholder,
    COVER_PRESETS, GENRE_PRESET_MAP
)


class TestCoverPresets:
    def test_all_presets_have_required_keys(self):
        for name, preset in COVER_PRESETS.items():
            assert "style_prompt" in preset, f"{name} missing style_prompt"
            assert "negative_prompt" in preset, f"{name} missing negative_prompt"

    def test_get_preset_by_name(self):
        preset = get_preset(preset_name="noir")
        assert "noir" in preset["style_prompt"].lower() or "dark" in preset["style_prompt"].lower()

    def test_get_preset_by_genre(self):
        preset = get_preset(genre_id="thriller")
        assert preset is not None

    def test_unknown_genre_returns_bold(self):
        preset = get_preset(genre_id="unknown_xyz")
        assert preset == COVER_PRESETS["bold"]

    def test_genre_preset_map_all_valid(self):
        for genre, preset_name in GENRE_PRESET_MAP.items():
            assert preset_name in COVER_PRESETS, f"Genre {genre} maps to unknown preset {preset_name}"


class TestBuildCoverPrompt:
    def test_returns_dict_with_required_keys(self):
        result = build_cover_prompt("Test Title", "Author Name", genre_id="thriller")
        assert "prompt" in result
        assert "negative_prompt" in result
        assert "width" in result
        assert "height" in result

    def test_prompt_contains_title(self):
        result = build_cover_prompt("Dark Horizon", "J. Smith")
        assert "Dark Horizon" in result["prompt"]

    def test_prompt_contains_author(self):
        result = build_cover_prompt("Book", "Famous Author")
        assert "Famous Author" in result["prompt"]

    def test_kdp_dimensions(self):
        result = build_cover_prompt("T", "A")
        assert result["width"] == 2560
        assert result["height"] == 1600


class TestSaveCoverPlaceholder:
    def test_creates_png_file(self, tmp_path):
        result = save_cover_placeholder("My Novel", "Author", output_dir=tmp_path)
        assert "path" in result
        assert Path(result["path"]).exists()
        assert result["path"].endswith(".png")

    def test_backend_is_placeholder(self, tmp_path):
        result = save_cover_placeholder("T", output_dir=tmp_path)
        assert result["backend"] == "placeholder"

    def test_no_output_dir_uses_default(self, tmp_path, monkeypatch):
        import scripts.cover_generator as cg
        monkeypatch.setattr(cg, "_DEFAULT_COVERS_DIR", tmp_path)
        result = cg.save_cover_placeholder("Title", "Author")
        assert Path(result["path"]).exists()
