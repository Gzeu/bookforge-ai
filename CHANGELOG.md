# Changelog

All notable changes to **BookForge AI** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] — 2026-06-30

### Added
- **Web UI** (`web/`) — FastAPI + Jinja2 + DaisyUI + TailwindCSS
  - `/` — Generate form with provider selector, chapters, title, author, description
  - `/job/{id}` — Live job page with real-time polling, progress bar, log stream
  - `/download/{id}` — EPUB download endpoint
  - `/research` — AI-powered KDP niche & keyword research page
  - `/health` — health check for BookForge + NovelClaw
  - `web/static/app.js` — `pollJob()` function for real-time status updates
- **`bookforge-web` CLI entry point** — `uvicorn web.app:app ...`
- **`python-multipart`**, **`jinja2`**, **`fastapi`**, **`uvicorn`** added to dependencies

### Changed
- `requirements.txt` — added web dependencies
- `pyproject.toml` — bumped to `1.1.0`, added `bookforge-web` script entry

---

## [1.0.0] — 2026-06-30

### Added
- **`pipeline.py`** — main orchestrator, single-command premise → EPUB flow
- **`scripts/generate_book.py`** — `NovelClawClient` class for full NovelClaw REST API
- **`scripts/txt_to_epub.py`** — KDP-ready EPUB converter with Georgia CSS, chapter detection
- **`scripts/kdp_upload.py`** — Amazon KDP Playwright uploader with AI disclosure
- **`scripts/niche_research.py`** — AI niche & keyword research (DeepSeek / OpenAI)
- **`.github/workflows/ci.yml`** — lint + pytest matrix on Python 3.10/3.11/3.12
- **`.github/workflows/release.yml`** — auto GitHub Release on `v*` tag
- **`tests/`** — unit tests for EPUB converter and API client (mocked)
- **`pyproject.toml`** — full package metadata and `bookforge` CLI entry point
- MIT License, CONTRIBUTING.md, issue templates, PR template

---

## [Unreleased]

### Planned
- Cover generation (Stable Diffusion / Canva API)
- Batch pipeline (multiple books in parallel)
- KDP sales dashboard integration
- DOCX export for KDP print-on-demand (paperback)
- Persistent job store (SQLite / Redis)
- Web UI authentication
