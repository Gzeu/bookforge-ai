#!/usr/bin/env python3
"""
BookForge AI — KDP Sales Stats Scraper.
Uses Playwright to log in to KDP and scrape units sold + royalties.

Note on `days` param: KDP's /report/month shows the current month.
For a full date-range report, extend this to use /report/custom with date params.
"""
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

KDP_EMAIL = os.getenv("KDP_EMAIL", "")
KDP_PASSWORD = os.getenv("KDP_PASSWORD", "")
_DEFAULT_OUTPUT_DIR = Path(os.getenv("MANUSCRIPTS_DIR", "./manuscripts"))


class KDPStatsScraper:
    KDP_SIGNIN_URL = "https://kdp.amazon.com/en_US/signin"
    KDP_REPORTS_URL = "https://kdp.amazon.com/en_US/report/month"

    def __init__(self, email: str = None, password: str = None):
        self.email = email or KDP_EMAIL
        self.password = password or KDP_PASSWORD

    def scrape(self, days: int = 30) -> dict:
        """
        Log in to KDP and scrape sales stats from the monthly report.
        `days` is stored in output metadata but does not filter the KDP report page
        (KDP /report/month shows current month only).
        Returns dict with: date, days, units_sold, royalties, currency, rows.
        """
        from playwright.sync_api import sync_playwright

        rows = []
        total_units = 0
        total_royalties = 0.0
        scrape_error = None

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(self.KDP_SIGNIN_URL)
                page.fill("input[name='email']", self.email)
                page.fill("input[name='password']", self.password)
                page.click("input[type='submit']")
                page.wait_for_load_state("networkidle", timeout=30000)

                page.goto(self.KDP_REPORTS_URL)
                page.wait_for_load_state("networkidle", timeout=30000)

                table_rows = page.query_selector_all("table tr")
                for row in table_rows[1:]:  # skip header
                    cells = row.query_selector_all("td")
                    if len(cells) >= 4:
                        title = cells[0].inner_text().strip()
                        units_text = cells[2].inner_text().strip().replace(",", "")
                        royalty_text = (
                            cells[3].inner_text().strip().replace(",", "").replace("$", "")
                        )
                        try:
                            units = int(units_text) if units_text.isdigit() else 0
                            royalty = float(royalty_text) if royalty_text else 0.0
                        except ValueError:
                            units, royalty = 0, 0.0
                        total_units += units
                        total_royalties += royalty
                        rows.append({"title": title, "units": units, "royalty": royalty})

                if not rows:
                    logger.warning(
                        "KDP scraper returned 0 rows — possible CAPTCHA, 2FA, or selector mismatch."
                    )

            except Exception as e:
                scrape_error = str(e)
                logger.error(f"KDP scraping failed: {e}")
            finally:
                browser.close()

        result = {
            "date": datetime.now().isoformat(),
            "days": days,
            "units_sold": total_units,
            "royalties": round(total_royalties, 2),
            "currency": "USD",
            "rows": rows,
        }
        if scrape_error:
            result["scrape_error"] = scrape_error
        return result

    def save(
        self,
        stats: dict,
        output_path: str = None,
        output_dir: Path = None,  # explicit param — avoids global in tests
    ) -> str:
        out_dir = output_dir or _DEFAULT_OUTPUT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)
        path = output_path or str(
            out_dir / f"kdp_stats_{datetime.now().strftime('%Y%m%d')}.json"
        )
        Path(path).write_text(json.dumps(stats, indent=2), encoding="utf-8")
        return path


if __name__ == "__main__":
    import typer
    app = typer.Typer()

    @app.command()
    def run(
        days: int = typer.Option(30, "--days", "-d", help="Days for report metadata (KDP shows current month)"),
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
        if stats.get("scrape_error"):
            console.print(f"[red]Warning: scraping error — {stats['scrape_error']}[/red]")
        path = scraper.save(stats, output)
        console.print(f"[green]Saved: {path}[/green]")
        table = Table(title=f"KDP Stats — Last {days} days")
        table.add_column("Title")
        table.add_column("Units")
        table.add_column("Royalties")
        for row in stats["rows"]:
            table.add_row(row["title"][:40], str(row["units"]), f"${row['royalty']:.2f}")
        table.add_row(
            "[bold]TOTAL[/bold]",
            str(stats["units_sold"]),
            f"[bold]${stats['royalties']:.2f}[/bold]"
        )
        console.print(table)

    app()
