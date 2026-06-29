# Changelog

All notable changes to **BookForge AI** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-06-30

### Added
- **`pipeline.py`** — main orchestrator, single-command premise → EPUB flow
- **`scripts/generate_book.py`** — `NovelClawClient` class for full NovelClaw REST API integration
  - `create_story()`, `wait_for_completion()`, `export()`, `create_and_wait()`
  - `rich` progress bar with real-time chapter count
- **`scripts/txt_to_epub.py`** — KDP-ready EPUB converter
  - Auto chapter detection via regex (with fallback to paragraph chunking)
  - Georgia serif CSS, proper `orphans`/`widows`, scene break support
  - Cover image embed, metadata (title, author, description, language)
- **`scripts/kdp_upload.py`** — Amazon KDP Playwright uploader
  - Login, title/author/description/keywords fill
  - EPUB + cover upload, price configuration
  - AI disclosure checkbox auto-handled
  - `KDP_HEADLESS` env flag for CI/prod runs
- **`scripts/niche_research.py`** — AI-powered KDP niche & keyword research
  - Supports DeepSeek and OpenAI backends
  - Returns JSON: niches, keywords, SEO title, price, revenue estimate, sample premise
- **`.env.example`** — complete environment template with all variables documented
- **`pyproject.toml`** — full package metadata, `bookforge` CLI entry point, ruff config
- **`.github/workflows/ci.yml`** — lint (ruff) + pytest matrix on Python 3.10/3.11/3.12
- **`.github/workflows/release.yml`** — auto GitHub Release on `v*` tag push
- **`tests/`** — unit tests for EPUB converter and API client
- MIT License

### Supported AI Providers
- DeepSeek (`deepseek-chat`) — recommended, lowest cost
- OpenAI (`gpt-4o-mini`)
- Anthropic (`claude-3-haiku`)
- Local LLM via Ollama / LM Studio (OpenAI-compatible)

---

## [Unreleased]

### Planned
- Web UI (FastAPI + React) for non-technical users
- Cover generation via Stable Diffusion / Canva API
- Batch pipeline (multiple books in parallel)
- KDP sales dashboard integration
- DOCX export for print-on-demand (KDP paperback)
