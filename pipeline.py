#!/usr/bin/env python3
"""
BookForge AI — Main Pipeline Orchestrator
Premise → Manuscript → EPUB → (optional) KDP Upload
"""
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

EPUB_OUTPUT_DIR = Path(os.getenv("EPUB_OUTPUT_DIR", "./epub_output"))
MANUSCRIPTS_DIR = Path(os.getenv("MANUSCRIPTS_DIR", "./manuscripts"))
COVERS_DIR      = Path(os.getenv("COVERS_DIR", "./covers"))


def run_pipeline(
    premise: str,
    title: str,
    author: str,
    chapters: int = 10,
    provider: str = None,
    price: float = 2.99,
    cover_image: str = None,
    description: str = "",
    keywords: list = None,
    upload: bool = False,
    no_upload: bool = False,
):
    from rich.console import Console
    from rich.panel import Panel
    console = Console()

    provider = provider or os.getenv("DEFAULT_PROVIDER", "deepseek")
    keywords = keywords or []

    console.print(Panel.fit(
        f"[bold cyan]BookForge AI Pipeline[/bold cyan]\n"
        f"[yellow]Title:[/yellow] {title}\n"
        f"[yellow]Author:[/yellow] {author}\n"
        f"[yellow]Chapters:[/yellow] {chapters}\n"
        f"[yellow]Provider:[/yellow] {provider}",
        border_style="cyan"
    ))

    # Step 1: Generate manuscript
    console.print("\n[bold]Step 1:[/bold] Generating manuscript via NovelClaw...")
    from scripts.generate_book import NovelClawClient
    client = NovelClawClient()
    if not client.health():
        console.print("[red]❌ NovelClaw is not running![/red]")
        console.print("[yellow]Start it with: cd NovelClaw && ./docker-start.sh[/yellow]")
        sys.exit(1)

    story_id = client.create_and_wait(premise, chapters, provider)
    MANUSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    manuscript_file = str(MANUSCRIPTS_DIR / f"manuscript_{story_id}.txt")
    client.export(story_id, manuscript_file)
    console.print(f"[green]✅ Manuscript:[/green] {manuscript_file}")

    # Step 2: Convert to EPUB
    console.print("\n[bold]Step 2:[/bold] Converting to EPUB...")
    from scripts.txt_to_epub import txt_to_epub
    EPUB_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = title.lower().replace(" ", "_")[:30]
    epub_file = str(EPUB_OUTPUT_DIR / f"{safe_title}_{story_id}.epub")
    txt_to_epub(manuscript_file, epub_file, title, author,
                cover_image=cover_image, description=description)
    console.print(f"[green]✅ EPUB:[/green] {epub_file}")

    # Step 3: Upload to KDP (optional)
    if upload and not no_upload:
        console.print("\n[bold]Step 3:[/bold] Uploading to Amazon KDP...")
        from scripts.kdp_upload import upload_to_kdp
        asyncio.run(upload_to_kdp(
            epub_file=epub_file,
            title=title,
            author=author,
            description=description or premise,
            keywords=keywords,
            cover_image=cover_image,
            price_usd=price,
            ai_disclosure=True,
        ))
    else:
        console.print("\n[dim]Step 3: KDP upload skipped (use --upload to enable)[/dim]")

    console.print(Panel.fit(
        f"[bold green]✅ Pipeline Complete![/bold green]\n"
        f"[yellow]Manuscript:[/yellow] {manuscript_file}\n"
        f"[yellow]EPUB:[/yellow] {epub_file}",
        border_style="green"
    ))
    return epub_file


if __name__ == "__main__":
    import typer

    app = typer.Typer(help="BookForge AI — AI-powered book pipeline for Amazon KDP")

    @app.command()
    def main(
        premise: str = typer.Option(None, "--premise", "-p", help="Story premise"),
        title: str = typer.Option(None, "--title", "-t"),
        author: str = typer.Option(None, "--author", "-a"),
        chapters: int = typer.Option(10, "--chapters", "-c"),
        provider: str = typer.Option(None, "--provider"),
        price: float = typer.Option(2.99, "--price"),
        cover: str = typer.Option(None, "--cover"),
        description: str = typer.Option("", "--description", "-d"),
        keywords: str = typer.Option("", "--keywords", "-k", help="Comma-separated"),
        upload: bool = typer.Option(False, "--upload", help="Auto-upload to KDP"),
        no_upload: bool = typer.Option(False, "--no-upload"),
        interactive: bool = typer.Option(False, "--interactive", "-i"),
    ):
        if interactive:
            premise = premise or typer.prompt("Story premise")
            title   = title   or typer.prompt("Book title")
            author  = author  or typer.prompt("Author name")
            chapters = typer.prompt("Number of chapters", default=10, type=int)

        if not premise or not title or not author:
            typer.echo("❌ --premise, --title, and --author are required (or use --interactive)")
            raise typer.Exit(1)

        kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
        run_pipeline(premise, title, author, chapters, provider, price,
                     cover, description, kw_list, upload, no_upload)

    app()
