# Changelog

All notable changes to **BookForge AI** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] — 2026-06-30

### Added
- **`scripts/categories.py`** — Full genre library with 20 major KDP genres:
  - Thriller, Romance, Fantasy, Sci-Fi, Mystery, Horror, Historical Fiction
  - Young Adult, Literary Fiction, Crime, Self-Help, Business & Finance
  - Paranormal, Western, Adventure, Children’s, Memoir, Erotica, Spiritual
  - Each genre has: 5 premise templates, 7 KDP keywords, recommended chapters, price point, sub-genres, AI tip
- **`scripts/batch_pipeline.py`** — Async batch book generator
  - Run multiple genres concurrently with `asyncio.Semaphore` throttling
  - Auto-builds premises from templates with `fill_placeholders=True`
  - JSON batch report saved after completion
  - CLI: `python -m scripts.batch_pipeline --genres thriller,romance,mystery --concurrent 2`
- **`web/templates/categories.html`** — Browse Genres page in Web UI
  - Genre cards with sub-genres, chapter count, price, click-to-expand modal
  - Modal shows: tip, highlighted premise template, KDP keywords, direct link to generate
  - Batch form: select multiple genres + author + chapters + provider → queue all
- **`web/static/categories.js`** — Genre page interactivity
- **`tests/test_categories.py`** — Full pytest suite for genre library

---

## [1.1.0] — 2026-06-30

### Added
- **`web/`** — FastAPI Web UI with DaisyUI dark theme
  - `web/app.py` — 7 routes, background jobs, health check
  - Templates: base, index, job progress, niche research
  - `web/static/app.js` — real-time job polling every 4 seconds
- Updated `requirements.txt` with `fastapi`, `uvicorn`, `jinja2`
- Updated `pyproject.toml` to `1.1.0`

---

## [1.0.0] — 2026-06-30

### Added
- **`pipeline.py`** — main orchestrator, single-command premise → EPUB flow
- **`scripts/generate_book.py`** — `NovelClawClient` class for full NovelClaw REST API integration
- **`scripts/txt_to_epub.py`** — KDP-ready EPUB converter with Georgia CSS, auto chapter detection
- **`scripts/kdp_upload.py`** — Amazon KDP Playwright uploader (login, metadata, AI disclosure)
- **`scripts/niche_research.py`** — AI-powered KDP niche & keyword research
- **`.github/workflows/ci.yml`** — lint (ruff) + pytest on Python 3.10/3.11/3.12
- **`.github/workflows/release.yml`** — auto GitHub Release on `v*` tag
- **`tests/`** — unit tests for EPUB converter and API client
- MIT License

---

## [Unreleased]

### Planned
- Web UI route `/batch` for async batch queue from browser
- Cover generation via Stable Diffusion / Canva API
- KDP sales dashboard integration
- DOCX export for print-on-demand (KDP paperback)
- Docker Compose for full stack (NovelClaw + BookForge Web UI)
