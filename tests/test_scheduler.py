#!/usr/bin/env python3
import json
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from scripts.scheduler import run_job, run_scheduler, ALLOWED_COMMANDS


class TestRunJob:
    def test_allowed_command_runs(self):
        rc = run_job("python -c \"print('ok')\"")
        assert rc == 0

    def test_disallowed_command_raises(self):
        with pytest.raises(ValueError, match="not allowed"):
            run_job("rm -rf /tmp/test")

    def test_empty_command_returns_minus_one(self):
        rc = run_job("")
        assert rc == -1

    def test_allowed_commands_set_contains_python(self):
        assert "python" in ALLOWED_COMMANDS
        assert "python3" in ALLOWED_COMMANDS


class TestRunScheduler:
    def test_once_mode_runs_and_exits(self, tmp_path):
        schedule = [
            {"name": "test-job", "enabled": True, "command": "python -c \"pass\""},
        ]
        schedule_file = str(tmp_path / "schedule.json")
        with open(schedule_file, "w") as f:
            json.dump(schedule, f)
        # Should complete without blocking
        run_scheduler(schedule_file, once=True)

    def test_disabled_job_is_skipped(self, tmp_path):
        executed = []
        schedule = [
            {"name": "skip-me", "enabled": False, "command": "python -c \"pass\""},
        ]
        schedule_file = str(tmp_path / "schedule.json")
        with open(schedule_file, "w") as f:
            json.dump(schedule, f)
        # Nothing should execute — just verify no error raised
        run_scheduler(schedule_file, once=True)
