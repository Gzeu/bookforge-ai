#!/usr/bin/env python3
"""BookForge AI — Simple scheduled batch runner."""
import json
import subprocess
import time
from pathlib import Path


def load_schedule(path: str) -> list:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_job(command: str) -> int:
    result = subprocess.run(command, shell=True, check=False)
    return result.returncode


def run_scheduler(schedule_file: str, once: bool = False, interval: int = 60):
    jobs = load_schedule(schedule_file)
    while True:
        for job in jobs:
            if job.get("enabled", True):
                run_job(job["command"])
        if once:
            break
        time.sleep(interval)
