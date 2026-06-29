#!/usr/bin/env python3
"""
BookForge AI — Batch Pipeline
Generate multiple books in parallel across genres.
"""
from __future__ import annotations
import asyncio
import os
import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict
from dotenv import load_dotenv
from scripts.categories import GENRES, get_random_premise

load_dotenv()

MANUSCRIPTS_DIR = Path(os.getenv("MANUSCRIPTS_DIR", "./manuscripts"))
EPUB_OUTPUT_DIR = Path(os.getenv("EPUB_OUTPUT_DIR", "./epub_output"))


@dataclass
class BatchJob:
    genre_id: str
    title: str
    author: str
    premise: str
    chapters: int
    provider: str
    status: str = "pending"  # pending | running | done | failed
    story_id: int | None = None
    manuscript_file: str | None = None
    epub_file: str | None = None
    error: str | None = None
    started_at: str | None = None
    finished_at: str | None = None


async def run_single_job(job: BatchJob, semaphore: asyncio.Semaphore) -> BatchJob:
    """Run one book generation job with concurrency control."""
    async with semaphore:
        from scripts.generate_book import NovelClawClient
        from scripts.txt_to_epub import txt_to_epub
        import threading

        job.status = "running"
        job.started_at = datetime.now().isoformat()
        print(f"  ▶ [{job.genre_id.upper()}] Starting: {job.title}")

        try:
            # Run blocking NovelClaw call in thread pool
            loop = asyncio.get_event_loop()
            client = NovelClawClient()

            def generate():
                return client.create_and_wait(job.premise, job.chapters, job.provider)

            story_id = await loop.run_in_executor(None, generate)
            job.story_id = story_id

            # Export manuscript
            MANUSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
            mfile = str(MANUSCRIPTS_DIR / f"batch_{job.genre_id}_{story_id}.txt")
            await loop.run_in_executor(None, lambda: client.export(story_id, mfile))
            job.manuscript_file = mfile

            # Convert to EPUB
            EPUB_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            safe = job.title.lower().replace(" ", "_")[:25]
            epub_file = str(EPUB_OUTPUT_DIR / f"{safe}_{story_id}.epub")
            await loop.run_in_executor(
                None,
                lambda: txt_to_epub(mfile, epub_file, job.title, job.author)
            )
            job.epub_file = epub_file
            job.status = "done"
            print(f"  ✅ [{job.genre_id.upper()}] Done: {job.title} → {epub_file}")

        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            print(f"  ❌ [{job.genre_id.upper()}] Failed: {job.title} — {e}")

        job.finished_at = datetime.now().isoformat()
        return job


async def run_batch(
    jobs: list[BatchJob],
    max_concurrent: int = 2,
) -> list[BatchJob]:
    """Run all jobs with a concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)
    tasks = [run_single_job(job, semaphore) for job in jobs]
    return await asyncio.gather(*tasks)


def build_batch_from_genres(
    genre_ids: list[str],
    author: str = "BookForge AI",
    chapters_per_book: int = 10,
    provider: str = None,
) -> list[BatchJob]:
    """Auto-build batch jobs from genre IDs using random premise templates."""
    provider = provider or os.getenv("DEFAULT_PROVIDER", "deepseek")
    jobs = []
    for gid in genre_ids:
        if gid not in GENRES:
            print(f"  ⚠️ Unknown genre: {gid}, skipping")
            continue
        genre = GENRES[gid]
        premise = get_random_premise(gid, fill_placeholders=True)
        # Generate a working title from the premise
        words = premise.split()[:6]
        title = " ".join(w.capitalize() for w in words if w.isalpha())[:40] or genre.name + " Novel"
        jobs.append(BatchJob(
            genre_id=gid,
            title=title,
            author=author,
            premise=premise,
            chapters=chapters_per_book,
            provider=provider,
        ))
    return jobs


def save_batch_report(jobs: list[BatchJob], output_path: str = "batch_report.json"):
    report = {
        "generated_at": datetime.now().isoformat(),
        "total": len(jobs),
        "done": sum(1 for j in jobs if j.status == "done"),
        "failed": sum(1 for j in jobs if j.status == "failed"),
        "jobs": [asdict(j) for j in jobs],
    }
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n📊 Batch report saved: {output_path}")
    return report


if __name__ == "__main__":
    import typer
    app = typer.Typer()

    @app.command()
    def run(
        genres: str = typer.Option(
            "thriller,romance,mystery,scifi",
            "--genres", "-g",
            help="Comma-separated genre IDs (or 'all' for all 19 genres)"
        ),
        author: str = typer.Option("BookForge AI", "--author", "-a"),
        chapters: int = typer.Option(10, "--chapters", "-c"),
        provider: str = typer.Option(None, "--provider", "-p"),
        concurrent: int = typer.Option(2, "--concurrent", help="Max parallel jobs"),
        report: str = typer.Option("batch_report.json", "--report"),
    ):
        from rich.console import Console
        from rich.table import Table
        console = Console()

        all_genre_ids = list(GENRES.keys())
        genre_list = all_genre_ids if genres == "all" else [g.strip() for g in genres.split(",")]

        console.print(f"\n[bold cyan]📚 BookForge AI — Batch Mode[/bold cyan]")
        console.print(f"Genres: {genre_list}")
        console.print(f"Concurrent: {concurrent} | Chapters/book: {chapters}\n")

        jobs = build_batch_from_genres(genre_list, author, chapters, provider)
        console.print(f"[yellow]🚀 Starting {len(jobs)} books...[/yellow]\n")

        results = asyncio.run(run_batch(jobs, concurrent))
        report_data = save_batch_report(results, report)

        table = Table(title="Batch Results")
        table.add_column("Genre")
        table.add_column("Title")
        table.add_column("Status")
        table.add_column("EPUB")
        for j in results:
            status_color = "green" if j.status == "done" else "red"
            table.add_row(
                j.genre_id, j.title[:30],
                f"[{status_color}]{j.status}[/{status_color}]",
                j.epub_file or j.error or "-"
            )
        console.print(table)

    app()
