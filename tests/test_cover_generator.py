#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.cover_generator import build_cover_prompt, slugify, save_cover_placeholder


def test_slugify_basic():
    assert slugify("The Hash Conspiracy") == "the-hash-conspiracy"


def test_build_cover_prompt_contains_genre_and_title():
    prompt = build_cover_prompt("The Hash Conspiracy", genre="thriller")
    assert "thriller" in prompt.lower()
    assert "The Hash Conspiracy" in prompt


def test_save_cover_placeholder(tmp_path, monkeypatch):
    monkeypatch.setenv("COVERS_DIR", str(tmp_path))
    from scripts import cover_generator as cg
    cg.COVERS_DIR = tmp_path
    result = save_cover_placeholder("Test Book", "fantasy")
    assert result["genre"] == "fantasy"
    assert os.path.exists(result["path"])
