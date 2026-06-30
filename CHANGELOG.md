# Changelog

All notable changes to **BookForge AI** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.4.1] — 2026-06-30

### Fixed
- **`web/app.py`** — moved `/download/zip/{job_id}` route **before** `/download/{job_id}` to prevent FastAPI's generic parameter from swallowing the specific route; bumped version string to `1.4.1`
- **`scripts/zip_export.py`** — `zip_files()` now returns `None` and deletes the empty archive if zero valid files were added (previously created a 22-byte empty ZIP)
- **`scripts/sales_stats.py`** — replaced bare `except Exception: pass` with `logger.error()` + `scrape_error` field in output dict; added 0-rows warning for CAPTCHA/2FA detection; clarified `days` param is metadata-only (documented KDP limitation); `save()` accepts `output_dir: Path = None` param to avoid global state in tests
- **`web/static/jobs.js`** — added `esc()` HTML-escape helper; all `job.id`, `job.title`, `job.provider`, `job.status` values sanitized before `innerHTML` insertion to prevent stored XSS

---

## [1.4.0] — 2026-06-30

### Added
- `scripts/zip_export.py` — batch ZIP export
- `scripts/sales_stats.py` — KDP Playwright scraper
- `GET /jobs` — live dashboard, `GET /api/jobs`, `GET /download/zip/{job_id}`
- `web/templates/jobs.html` + `web/static/jobs.js`

---

## [1.3.1] — 2026-06-30

### Fixed
- Shell injection in `scheduler.py`, webhook error handling, `detect_chapters` dedup, cover_generator output_dir, batch_pipeline lambda capture

---

## [1.3.0] — 2026-06-30

### Added
- `scripts/cover_generator.py`, `txt_to_docx.py`, `scheduler.py`, `webhooks.py`
- Web Tools page

---

## [1.2.0] — 2026-06-30

### Added
- `scripts/categories.py` — 20-genre library
- `scripts/batch_pipeline.py` — async batch generator
- Browse Genres web page

---

## [1.1.0] — 2026-06-30

### Added
- FastAPI Web UI with DaisyUI dark theme

---

## [1.0.0] — 2026-06-30

### Added
- Full pipeline: `pipeline.py`, NovelClaw client, EPUB, KDP uploader, niche research, CI/CD

---

## [Unreleased]

### Planned
- Docker Compose full stack
- Multi-provider cover layout presets
- Email delivery of finished EPUBs
