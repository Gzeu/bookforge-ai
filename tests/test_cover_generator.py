#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.cover_generator import build_cover_prompt, slugify, save_cover_placeholder


def test_slugify_basic():
    assert slugify("The Hash Conspiracy") == "the-hash-conspiracy"


def test_slugify_empty_returns_cover():
    assert slugify("") == "cover"
    assert slugify("!!!##") == "cover"


def test_build_cover_prompt_contains_genre_and_title():
    prompt = build_cover_prompt("The Hash Conspiracy", genre="thriller")
    assert "thriller" in prompt.lower()
    assert "The Hash Conspiracy" in prompt


def test_build_cover_prompt_with_subtitle():
    prompt = build_cover_prompt("Title", subtitle="The Reckoning", genre="horror")
    assert "The Reckoning" in prompt


def test_save_cover_placeholder_uses_output_dir(tmp_path):
    # Uses explicit output_dir param — no global patching needed
    result = save_cover_placeholder("Test Book", "fantasy", output_dir=tmp_path)
    assert result["genre"] == "fantasy"
    assert os.path.exists(result["path"])
    assert result["path"].startswith(str(tmp_path))
