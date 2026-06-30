#!/usr/bin/env python3
"""
BookForge AI — Batch Job State Manager.
Persists batch job state to disk so it survives process restarts.
Used alongside batch_pipeline.py for long-running or scheduled batches.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

_DEFAULT_STATE_DIR = Path(os.getenv("MANUSCRIPTS_DIR", "./manuscripts"))


class BatchStateManager:
    """
    Saves and loads batch job state as JSON on disk.
    Allows resuming a failed batch without re-running completed jobs.
    """

    def __init__(self, state_dir: Path = None):
        self.state_dir = state_dir or _DEFAULT_STATE_DIR
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, batch_id: str) -> Path:
        return self.state_dir / f"batch_state_{batch_id}.json"

    def save(self, batch_id: str, jobs: list[dict]) -> str:
        """Persist batch job list to disk. Each job must be a dict (use dataclasses.asdict)."""
        state = {
            "batch_id": batch_id,
            "saved_at": datetime.now().isoformat(),
            "total": len(jobs),
            "done": sum(1 for j in jobs if j.get("status") == "done"),
            "failed": sum(1 for j in jobs if j.get("status") == "failed"),
            "jobs": jobs,
        }
        path = self._path(batch_id)
        path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        return str(path)

    def load(self, batch_id: str) -> dict | None:
        """Load saved batch state. Returns None if not found."""
        path = self._path(batch_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_batches(self) -> list[str]:
        """Return all saved batch IDs in the state directory."""
        return [
            p.stem.replace("batch_state_", "")
            for p in self.state_dir.glob("batch_state_*.json")
        ]

    def delete(self, batch_id: str) -> bool:
        """Delete saved state for a batch. Returns True if deleted."""
        path = self._path(batch_id)
        if path.exists():
            path.unlink()
            return True
        return False

    def pending_jobs(self, batch_id: str) -> list[dict]:
        """Return only jobs with status != 'done' — for resume logic."""
        state = self.load(batch_id)
        if not state:
            return []
        return [j for j in state["jobs"] if j.get("status") != "done"]
