#!/usr/bin/env python3
"""
BookForge AI — Amazon KDP Playwright Uploader
Automates book upload to Kindle Direct Publishing.
NOTE: Requires a valid KDP account. Use responsibly.
"""
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

KDP_EMAIL    = os.getenv("KDP_EMAIL", "")
KDP_PASSWORD = os.getenv("KDP_PASSWORD", "")
KDP_HEADLESS = os.getenv("KDP_HEADLESS", "false").lower() == "true"


async def upload_to_kdp(
    epub_file: str,
    title: str,
    author: str,
    description: str,
    keywords: list,
    cover_image: str = None,
    price_usd: float = 2.99,
    language: str = "English",
    ai_disclosure: bool = True,
) -> bool:
    from playwright.async_api import async_playwright

    # Validate epub exists before launching browser
    if not Path(epub_file).exists():
        raise FileNotFoundError(f"EPUB file not found: {epub_file}")

    if not KDP_EMAIL or not KDP_PASSWORD:
        raise ValueError("KDP_EMAIL and KDP_PASSWORD must be set in .env")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=KDP_HEADLESS)
        context = await browser.new_context(viewport={"width": 1280, "height": 900})
        page    = await context.new_page()

        print("🌐 Opening KDP...")
        await page.goto("https://kdp.amazon.com/en_US/signin")
        await page.fill('input[name="email"]', KDP_EMAIL)
        await page.click('input[id="continue"]')
        await page.wait_for_selector('input[name="password"]', timeout=15000)
        await page.fill('input[name="password"]', KDP_PASSWORD)
        await page.click('input[id="signInSubmit"]')
        await page.wait_for_url("**/bookshelf**", timeout=30000)
        print("✅ Logged in")

        await page.click('a[id="add-new-kindle-book"]', timeout=10000)
        await page.wait_for_url("**/title-setup**", timeout=15000)

        print("📝 Filling book details...")
        await page.fill('input[id="data-print-book-title"]', title)
        parts = author.strip().split()
        await page.fill('input[id="data-print-book-primary-author-first-name"]', parts[0])
        if len(parts) > 1:
            await page.fill(
                'input[id="data-print-book-primary-author-last-name"]',
                " ".join(parts[1:])
            )
        await page.fill('textarea[id="data-print-book-description"]', description)
        for i, kw in enumerate(keywords[:7]):
            await page.fill(f'input[id="data-print-book-keywords-{i}"]', kw)

        if ai_disclosure:
            cb = page.locator('input[id*="ai-content"]').first
            if await cb.is_visible():
                await cb.check()
                print("✅ AI disclosure checked")

        await page.click('input[id="save-and-continue-announce"]')
        await page.wait_for_url("**/content**", timeout=15000)

        print(f"📤 Uploading EPUB: {epub_file}")
        inputs = page.locator('input[type="file"]')
        await inputs.first.set_input_files(epub_file)
        await page.wait_for_selector(".upload-complete, .file-uploaded", timeout=180000)
        print("✅ EPUB uploaded")

        if cover_image and Path(cover_image).exists():
            print(f"🖼️ Uploading cover: {cover_image}")
            if await inputs.count() > 1:
                await inputs.nth(1).set_input_files(cover_image)
                await page.wait_for_selector(".cover-uploaded, .cover-complete", timeout=90000)
                print("✅ Cover uploaded")

        await page.click('input[id="save-and-continue-announce"]')
        await page.wait_for_url("**/pricing**", timeout=15000)

        print("💰 Setting price...")
        await page.select_option('select[id="data-print-book-territories"]', "worldwide")
        await page.fill('input[id="data-print-book-price-0"]', str(price_usd))

        await page.click('input[id="save-and-publish-announce"]')
        print("🎉 Book submitted for review!")
        print("⏳ Amazon review: 24–72 hours")

        await browser.close()
        return True


if __name__ == "__main__":
    import typer
    app = typer.Typer()

    @app.command()
    def run(
        epub_file: str = typer.Argument(...),
        title: str = typer.Option(..., prompt=True),
        author: str = typer.Option(..., prompt=True),
        description: str = typer.Option(..., prompt=True),
        cover: str = typer.Option(None),
        keywords: str = typer.Option("", help="Comma-separated"),
        price: float = typer.Option(2.99),
        ai_disclosure: bool = typer.Option(True),
    ):
        kw_list = [k.strip() for k in keywords.split(",") if k.strip()]
        asyncio.run(upload_to_kdp(
            epub_file, title, author, description,
            kw_list, cover, price,
            ai_disclosure=ai_disclosure
        ))

    app()
