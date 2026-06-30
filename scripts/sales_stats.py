#!/usr/bin/env python3
"""
BookForge AI — KDP Sales Stats Scraper.
Uses Playwright to log in to KDP and scrape units sold + royalties.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

KDP_EMAIL = os.getenv("KDP_EMAIL", "")
KDP_PASSWORD = os.getenv("KDP_PASSWORD", "")
MANUSCRIPTS_DIR = Path(os.getenv("MANUSCRIPTS_DIR", "./manuscripts"))


class KDPStatsScraper:
    KDP_REPORTS_URL = "https://kdp.amazon.com/en_US/report/month"

    def __init__(self, email: str = None, password: str = None):
        self.email = email or KDP_EMAIL
        self.password = password or KDP_PASSWORD

    def scrape(self, days: int = 30) -> dict:
        """
        Log in to KDP and scrape sales stats.
        Returns dict with keys: date, days, units_sold, royalties, currency, rows.
        """
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://kdp.amazon.com/en_US/signin")

            # Login
            page.fill("input[name='email']", self.email)
            page.fill("input[name='password']", self.password)
            page.click("input[type='submit']")
            page.wait_for_load_state("networkidle", timeout=30000)

            page.goto(self.KDP_REPORTS_URL)
            page.wait_for_load_state("networkidle", timeout=30000)

            rows = []
            total_units = 0
            total_royalties = 0.0

            try:
                table_rows = page.query_selector_all("table tr")
                for row in table_rows[1:]:  # skip header
                    cells = row.query_selector_all("td")
                    if len(cells) >= 4:
                        title = cells[0].inner_text().strip()
                        units_text = cells[2].inner_text().strip().replace(",", "")
                        royalty_text = cells[3].inner_text().strip().replace(",", "").replace("$", "")
                        try:
                            units = int(units_text) if units_text.isdigit() else 0
                            royalty = float(royalty_text) if royalty_text else 0.0
                        except ValueError:
                            units, royalty = 0, 0.0
                        total_units += units
                        total_royalties += royalty
                        rows.append({"title": title, "units": units, "royalty": royalty})
            except Exception:
                pass

            browser.close()

        return {
            "date": datetime.now().isoformat(),
            "days": days,
            "units_sold": total_units,
            "royalties": round(total_royalties, 2),
            "currency": "USD",
            "rows": rows,
        }

    def save(self, stats: dict, output_path: str = None) -> str:
        MANUSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
        path = output_path or str(
            MANUSCRIPTS_DIR / f"kdp_stats_{datetime.now().strftime('%Y%m%d')}.json"
        )
        Path(path).write_text(json.dumps(stats, indent=2), encoding="utf-8")
        return path


if __name__ == "__main__":
    import typer
    app = typer.Typer()

    @app.command()
    def run(
        days: int = typer.Option(30, "--days", "-d", help="Days back to report"),
        output: str = typer.Option(None, "--output", "-o", help="Output JSON path"),
        email: str = typer.Option(None, "--email"),
        password: str = typer.Option(None, "--password"),
    ):
        from rich.console import Console
        from rich.table import Table
        console = Console()
        scraper = KDPStatsScraper(email, password)
        console.print("[cyan]Scraping KDP stats...[/cyan]")
        stats = scraper.scrape(days)
        path = scraper.save(stats, output)
        console.print(f"[green]Saved: {path}[/green]")
        table = Table(title=f"KDP Stats — Last {days} days")
        table.add_column("Title")
        table.add_column("Units")
        table.add_column("Royalties")
        for row in stats["rows"]:
            table.add_row(row["title"][:40], str(row["units"]), f"${row['royalty']:.2f}")
        table.add_row("[bold]TOTAL[/bold]", str(stats["units_sold"]), f"[bold]${stats['royalties']:.2f}[/bold]")
        console.print(table)

    app()
