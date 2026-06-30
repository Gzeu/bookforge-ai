# Changelog

All notable changes to **BookForge AI** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.3.1] — 2026-06-30

### Fixed
- **`scripts/scheduler.py`** — replaced `shell=True` with `shell=False` + command allowlist `{"python", "python3"}` to prevent shell injection; schedule file now reloads on every cycle so live edits take effect without restart; empty commands return `-1` instead of crashing
- **`scripts/webhooks.py`** — wrapped all `requests.post` calls in granular `try/except` (Timeout, RequestException, Exception); failures log via `logger.warning()` and return `0` — webhooks can no longer crash a running batch job
- **`scripts/utils.py`** *(new)* — extracted shared `detect_chapters()` to eliminate duplication between `txt_to_epub.py` and `txt_to_docx.py`; added empty-string fallback returning `[("Chapter 1", text)]`
- **`scripts/txt_to_epub.py`** + **`scripts/txt_to_docx.py`** — both now import `detect_chapters` from `scripts.utils`; regex and fallback logic guaranteed identical for EPUB and DOCX output
- **`scripts/cover_generator.py`** — `save_cover_placeholder()` accepts `output_dir: Path = None` param; tests no longer require `monkeypatch` on module-level globals
- **`scripts/batch_pipeline.py`** — explicit lambda variable capture (`_mfile, _epub, _title, _author`) prevents closure bug in async executor; `_make_title_from_premise()` extracted as named function with cleaned regex

### Tests
- **`tests/test_utils.py`** — 6 tests for `detect_chapters` including empty input and EPUB/DOCX identity assertion
- **`tests/test_webhooks.py`** — 7 mock tests covering success, timeout, connection error, and unknown exception
- **`tests/test_scheduler.py`** — 5 tests: allowed/disallowed commands, empty string, `once=True` mode, disabled job skip
- **`tests/test_cover_generator.py`** — rewritten to use `output_dir=tmp_path` directly, no global patching

---

## [1.3.0] — 2026-06-30

### Added
- **`scripts/cover_generator.py`** — automatic cover generation helper
  - Supports local Stable Diffusion WebUI (`SD_WEBUI_URL`) and Canva (`CANVA_API_KEY`) modes
  - Genre-aware prompts, subtitle support, KDP-safe 1.6:1 cover size defaults
  - Saves output in `covers/` and returns metadata JSON
- **`scripts/txt_to_docx.py`** — DOCX export for KDP paperback workflows
- **`scripts/scheduler.py`** — scheduled batch automation
- **`scripts/webhooks.py`** — notification dispatch layer (Discord + generic JSON POST)
- **`web/templates/tools.html`** + **`web/static/tools.js`** — Tools page in Web UI

### Changed
- Updated `pyproject.toml` to `1.3.0`
- Expanded `requirements.txt` with `python-docx`

---

## [1.2.0] — 2026-06-30

### Added
- **`scripts/categories.py`** — Full genre library with 20 major KDP genres
- **`scripts/batch_pipeline.py`** — Async batch book generator with `asyncio.Semaphore`
- **`web/templates/categories.html`** + **`web/static/categories.js`** — Browse Genres page
- **`tests/test_categories.py`**

---

## [1.1.0] — 2026-06-30

### Added
- **`web/`** — FastAPI Web UI with DaisyUI dark theme (7 routes, background jobs, health check)
- Updated `requirements.txt` with `fastapi`, `uvicorn`, `jinja2`

---

## [1.0.0] — 2026-06-30

### Added
- **`pipeline.py`** — main orchestrator, single-command premise → EPUB flow
- **`scripts/generate_book.py`** — `NovelClawClient` for NovelClaw REST API
- **`scripts/txt_to_epub.py`** — KDP-ready EPUB converter
- **`scripts/kdp_upload.py`** — Amazon KDP Playwright uploader
- **`scripts/niche_research.py`** — AI-powered niche & keyword research
- **`.github/workflows/ci.yml`** + **`release.yml`** — CI/CD pipeline
- MIT License

---

## [Unreleased]

### Planned
- **v1.4.0** — Job dashboard (FastAPI `/jobs` page with live status table), batch ZIP export, KDP sales stats scraper
- Docker Compose full stack
- Multi-provider cover layout presets
