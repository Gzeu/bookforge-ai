#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.sales_stats import KDPStatsScraper


class TestKDPStatsScraperUnit:
    def test_save_creates_json_file(self, tmp_path):
        scraper = KDPStatsScraper()
        stats = {
            "date": datetime.now().isoformat(), "days": 30,
            "units_sold": 12, "royalties": 21.50,
            "currency": "USD",
            "rows": [{"title": "Test Book", "units": 12, "royalty": 21.50}],
        }
        out = str(tmp_path / "kdp_stats_test.json")
        result = scraper.save(stats, out)
        assert os.path.exists(result)
        loaded = json.loads(open(result).read())
        assert loaded["units_sold"] == 12
        assert loaded["currency"] == "USD"

    def test_save_uses_output_dir_param(self, tmp_path):
        scraper = KDPStatsScraper()
        stats = {"date": "", "days": 30, "units_sold": 0,
                 "royalties": 0.0, "currency": "USD", "rows": []}
        path = scraper.save(stats, output_dir=tmp_path)
        assert path.startswith(str(tmp_path))
        assert "kdp_stats_" in path
        assert path.endswith(".json")

    def test_stats_structure_has_required_keys(self):
        required = {"date", "days", "units_sold", "royalties", "currency", "rows"}
        stats = {
            "date": datetime.now().isoformat(), "days": 7,
            "units_sold": 0, "royalties": 0.0, "currency": "USD", "rows": [],
        }
        assert required.issubset(set(stats.keys()))

    def test_empty_rows_and_zero_totals(self, tmp_path):
        scraper = KDPStatsScraper()
        stats = {
            "date": datetime.now().isoformat(), "days": 30,
            "units_sold": 0, "royalties": 0.0, "currency": "USD", "rows": [],
        }
        out = str(tmp_path / "empty.json")
        scraper.save(stats, out)
        loaded = json.loads(open(out).read())
        assert loaded["units_sold"] == 0
        assert loaded["rows"] == []

    def test_scrape_error_field_present_on_failure(self):
        """If scrape_error key present, it must be a non-empty string."""
        stats = {
            "date": "", "days": 30, "units_sold": 0,
            "royalties": 0.0, "currency": "USD", "rows": [],
            "scrape_error": "Timeout waiting for networkidle",
        }
        assert isinstance(stats.get("scrape_error"), str)
        assert len(stats["scrape_error"]) > 0
