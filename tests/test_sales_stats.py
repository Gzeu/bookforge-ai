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
            "date": datetime.now().isoformat(),
            "days": 30,
            "units_sold": 12,
            "royalties": 21.50,
            "currency": "USD",
            "rows": [{"title": "Test Book", "units": 12, "royalty": 21.50}],
        }
        out = str(tmp_path / "kdp_stats_test.json")
        result = scraper.save(stats, out)
        assert os.path.exists(result)
        loaded = json.loads(open(result).read())
        assert loaded["units_sold"] == 12
        assert loaded["currency"] == "USD"

    def test_output_filename_format(self, tmp_path):
        scraper = KDPStatsScraper()
        import scripts.sales_stats as ss
        ss.MANUSCRIPTS_DIR = tmp_path
        stats = {"date": "", "days": 30, "units_sold": 0,
                 "royalties": 0.0, "currency": "USD", "rows": []}
        path = scraper.save(stats)
        assert "kdp_stats_" in path
        assert path.endswith(".json")

    def test_stats_structure_has_required_keys(self):
        required = {"date", "days", "units_sold", "royalties", "currency", "rows"}
        stats = {
            "date": datetime.now().isoformat(), "days": 7,
            "units_sold": 0, "royalties": 0.0, "currency": "USD", "rows": [],
        }
        assert required.issubset(set(stats.keys()))

    def test_empty_rows_stats_zero(self, tmp_path):
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
