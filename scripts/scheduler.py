#!/usr/bin/env python3
"""BookForge AI — Simple scheduled batch runner."""
import json
import logging
import subprocess
import time
from pathlib import Path

logger = logging.getLogger(__name__)

ALLOWED_COMMANDS = {"python", "python3"}


def load_schedule(path: str) -> list:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run_job(command: str) -> int:
    parts = command.split()
    if not parts:
        logger.warning("Empty command, skipping")
        return -1
    if parts[0] not in ALLOWED_COMMANDS:
        raise ValueError(f"Command not allowed: '{parts[0]}'. Allowed: {ALLOWED_COMMANDS}")
    result = subprocess.run(parts, shell=False, check=False)
    return result.returncode


def run_scheduler(schedule_file: str, once: bool = False, interval: int = 60):
    """Run scheduled jobs. Reloads schedule from file on every iteration."""
    while True:
        try:
            jobs = load_schedule(schedule_file)  # reload every cycle to pick up changes
        except Exception as e:
            logger.error(f"Failed to load schedule file: {e}")
            if once:
                break
            time.sleep(interval)
            continue

        for job in jobs:
            if job.get("enabled", True):
                try:
                    rc = run_job(job["command"])
                    logger.info(f"Job '{job.get('name', job['command'])}' exited with code {rc}")
                except Exception as e:
                    logger.error(f"Job failed: {e}")

        if once:
            break
        time.sleep(interval)
