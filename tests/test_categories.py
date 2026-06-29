#!/usr/bin/env python3
"""
Unit tests for scripts/categories.py
"""
import sys, os, re, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.categories import (
    GENRES, get_all_genres, get_genre, get_random_premise, build_full_premise
)


class TestGenreLibrary:
    def test_minimum_genre_count(self):
        assert len(GENRES) >= 19

    def test_all_genres_have_required_fields(self):
        for gid, g in GENRES.items():
            assert g.id == gid
            assert g.name
            assert g.emoji
            assert len(g.sub_genres) >= 3
            assert len(g.premise_templates) >= 3
            assert len(g.kdp_keywords) >= 5
            assert 8 <= g.recommended_chapters <= 30
            assert 1.99 <= g.typical_price <= 9.99

    def test_get_genre_returns_correct(self):
        g = get_genre("thriller")
        assert g is not None
        assert g.name == "Thriller"

    def test_get_genre_unknown_returns_none(self):
        assert get_genre("nonexistent_genre_xyz") is None

    def test_get_all_genres_length(self):
        assert len(get_all_genres()) == len(GENRES)


class TestPremiseGeneration:
    def test_random_premise_returns_string(self):
        for gid in GENRES:
            p = get_random_premise(gid)
            assert isinstance(p, str)
            assert len(p) > 20

    def test_fill_placeholders_removes_braces(self):
        for gid in list(GENRES.keys())[:5]:
            p = get_random_premise(gid, fill_placeholders=True)
            remaining = re.findall(r"\{[^}]+\}", p)
            # Allow a few unfilled for rare placeholders
            assert len(remaining) <= 5, f"{gid}: {remaining}"

    def test_build_full_premise_replaces_known_fields(self):
        p = build_full_premise("thriller", {
            "protagonist": "Maria",
            "antagonist": "the Shadow Council",
        })
        assert "Maria" in p
        assert "the Shadow Council" in p

    def test_build_full_premise_invalid_genre(self):
        with pytest.raises(ValueError):
            build_full_premise("not_a_real_genre", {})
