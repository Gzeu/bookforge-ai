# Changelog

All notable changes to **BookForge AI** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.0] — 2026-06-30

### Added
- **`scripts/cover_generator.py`** — automatic cover generation helper
  - Supports local Stable Diffusion WebUI (`SD_WEBUI_URL`) and Canva (`CANVA_API_KEY`) modes
  - Genre-aware prompts, subtitle support, KDP-safe 1.6:1 cover size defaults
  - Saves output in `covers/` and returns metadata JSON
- **`scripts/txt_to_docx.py`** — DOCX export for KDP paperback workflows
  - Chapter heading detection, scene break styling, title page metadata
  - Produces print-friendly `.docx` alongside EPUB when requested
- **`scripts/scheduler.py`** — scheduled batch automation
  - JSON-based schedules, interval polling, safe subprocess execution
  - Designed for cron/systemd or long-running worker usage
- **`scripts/webhooks.py`** — notification dispatch layer
  - Supports Discord webhook and generic JSON POST callback endpoints
  - Emits batch start, success, failure events
- **`tests/test_cover_generator.py`** — validates prompt building and filename sanitization
- **`tests/test_txt_to_docx.py`** — validates DOCX export and output creation
- **`web/templates/tools.html`** — web UI tools page for cover + DOCX utilities
- **`web/static/tools.js`** — browser helpers for tools page interactions

### Changed
- Updated **`pipeline.py`** design roadmap to support optional DOCX and cover generation stages
- Expanded **`requirements.txt`** for DOCX and webhook support
- Updated **`pyproject.toml`** to version `1.3.0`
- Updated **`README.md`** roadmap to mention paperback, covers, and automation hooks

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
- KDP sales dashboard integration
- Docker Compose for full stack (NovelClaw + BookForge Web UI)
- Multi-provider cover layout presets
