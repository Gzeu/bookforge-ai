#!/usr/bin/env python3
"""BookForge AI — Batch ZIP export for EPUB files."""
import zipfile
from datetime import datetime
from pathlib import Path


def zip_files(paths: list[str], output_path: str) -> str | None:
    """
    Zip a list of file paths into a single archive.
    Returns output_path on success, or None if no valid files were added.
    """
    added = 0
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in paths:
            fp = Path(p)
            if fp.exists():
                zf.write(fp, fp.name)
                added += 1
    if added == 0:
        Path(output_path).unlink(missing_ok=True)
        return None
    return output_path


def zip_epub_batch(
    job_id: str,
    jobs_store: dict,
    output_dir: Path = None,
) -> str | None:
    """
    Zip all EPUBs from a batch job into one archive.
    Returns the path to the ZIP file, or None if no EPUBs found.
    """
    job = jobs_store.get(job_id)
    if not job:
        return None

    epub_files = job.get("epub_files") or []
    if not epub_files and job.get("epub_file"):
        epub_files = [job["epub_file"]]

    epub_files = [f for f in epub_files if f and Path(f).exists()]
    if not epub_files:
        return None

    out_dir = output_dir or Path(epub_files[0]).parent
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = str(out_dir / f"bookforge_batch_{ts}.zip")
    return zip_files(epub_files, zip_path)
