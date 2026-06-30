#!/usr/bin/env python3
"""
Tests for scripts/batch_pipeline.py.
"""
import os
import sys
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from dataclasses import asdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.batch_pipeline import (
    BatchJob, build_batch_from_genres, save_batch_report, _make_title_from_premise
)


class TestBuildBatchFromGenres:
    def test_known_genres_create_jobs(self):
        jobs = build_batch_from_genres(["thriller", "romance"], author="Test")
        assert len(jobs) == 2
        assert all(isinstance(j, BatchJob) for j in jobs)
        assert jobs[0].genre_id == "thriller"
        assert jobs[1].genre_id == "romance"

    def test_unknown_genre_skipped(self):
        jobs = build_batch_from_genres(["thriller", "nonexistent_genre"])
        assert len(jobs) == 1
        assert jobs[0].genre_id == "thriller"

    def test_job_has_required_fields(self):
        jobs = build_batch_from_genres(["mystery"])
        job = jobs[0]
        assert job.title
        assert job.premise
        assert job.author
        assert job.chapters > 0
        assert job.status == "pending"

    def test_custom_author_and_chapters(self):
        jobs = build_batch_from_genres(["fantasy"], author="John Doe", chapters_per_book=15)
        assert jobs[0].author == "John Doe"
        assert jobs[0].chapters == 15


class TestMakeTitleFromPremise:
    def test_returns_string(self):
        title = _make_title_from_premise("A detective discovers a time machine", "Fallback")
        assert isinstance(title, str)
        assert len(title) > 0

    def test_uses_fallback_on_empty(self):
        title = _make_title_from_premise("", "My Fallback")
        assert title == "My Fallback"

    def test_max_length_40_chars(self):
        long_premise = " ".join(["word"] * 20)
        title = _make_title_from_premise(long_premise, "Fallback")
        assert len(title) <= 40


class TestSaveBatchReport:
    def test_creates_json_file(self, tmp_path):
        jobs = [
            BatchJob(genre_id="thriller", title="T", author="A", premise="P",
                     chapters=10, provider="deepseek", status="done"),
            BatchJob(genre_id="romance", title="R", author="A", premise="P",
                     chapters=10, provider="deepseek", status="failed"),
        ]
        out = str(tmp_path / "report.json")
        report = save_batch_report(jobs, out)
        assert os.path.exists(out)
        assert report["total"] == 2
        assert report["done"] == 1
        assert report["failed"] == 1

    def test_report_contains_jobs_array(self, tmp_path):
        jobs = [BatchJob(genre_id="scifi", title="S", author="A", premise="P",
                         chapters=5, provider="deepseek", status="done")]
        out = str(tmp_path / "r.json")
        report = save_batch_report(jobs, out)
        assert isinstance(report["jobs"], list)
        assert report["jobs"][0]["genre_id"] == "scifi"
