#!/usr/bin/env python3
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.batch_manager import BatchStateManager


class TestBatchStateManager:
    def test_save_and_load(self, tmp_path):
        mgr = BatchStateManager(state_dir=tmp_path)
        jobs = [{"genre_id": "thriller", "status": "done"}, {"genre_id": "romance", "status": "failed"}]
        mgr.save("abc123", jobs)
        state = mgr.load("abc123")
        assert state is not None
        assert state["batch_id"] == "abc123"
        assert state["total"] == 2
        assert state["done"] == 1
        assert state["failed"] == 1

    def test_load_missing_returns_none(self, tmp_path):
        mgr = BatchStateManager(state_dir=tmp_path)
        assert mgr.load("nonexistent") is None

    def test_list_batches(self, tmp_path):
        mgr = BatchStateManager(state_dir=tmp_path)
        mgr.save("id1", [{"status": "done"}])
        mgr.save("id2", [{"status": "pending"}])
        ids = mgr.list_batches()
        assert "id1" in ids
        assert "id2" in ids

    def test_delete(self, tmp_path):
        mgr = BatchStateManager(state_dir=tmp_path)
        mgr.save("to_delete", [])
        assert mgr.delete("to_delete") is True
        assert mgr.load("to_delete") is None

    def test_pending_jobs_filters_done(self, tmp_path):
        mgr = BatchStateManager(state_dir=tmp_path)
        jobs = [
            {"genre_id": "thriller", "status": "done"},
            {"genre_id": "romance", "status": "pending"},
            {"genre_id": "mystery", "status": "failed"},
        ]
        mgr.save("batch_x", jobs)
        pending = mgr.pending_jobs("batch_x")
        assert len(pending) == 2
        assert all(j["status"] != "done" for j in pending)
