# Changelog

All notable changes to **BookForge AI** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.5.0] — 2026-06-30

### Added
- **`Dockerfile`** — production-ready image with Playwright Chromium deps, non-root friendly
- **`docker-compose.yml`** — full stack: `novelclaw` + `bookforge` services, named volumes, healthchecks, shared `bookforge_net` network
- **`scripts/email_delivery.py`** — `EmailDelivery` class: SMTP (Gmail/Outlook/custom) with STARTTLS; attaches EPUB as `application/epub+zip`; `test_connection()` method; granular exception handling (SMTPAuthenticationError, SMTPException, generic)
- **`scripts/batch_manager.py`** — completed from stub: `BatchStateManager` class with `save()`, `load()`, `list_batches()`, `delete()`, `pending_jobs()` for disk-persisted batch state and resume logic
- **`scripts/cover_generator.py`** — 6 layout presets: `minimal`, `bold`, `noir`, `romance`, `scifi`, `fantasy`; `GENRE_PRESET_MAP` auto-selects preset by genre; `get_preset()` and updated `build_cover_prompt()`
- **`scripts/sales_stats.py`** — real date-range support via `/report/custom?startDate=&endDate=`; `_login_and_navigate()` and `_parse_table()` extracted as private methods
- **`README.md`** — complete rewrite: quick start (Docker + local), `.env` reference, Web UI route table, scripts table, CI badges

### Tests
- **`tests/test_pipeline.py`** — 4 tests: returns EPUB path, exits on NovelClaw down, skips upload by default, calls upload when flag set
- **`tests/test_batch_pipeline.py`** — 7 tests: genre building, unknown genre skip, required fields, custom author/chapters, title from premise, save report
- **`tests/test_kdp_upload.py`** — 3 tests: import check, missing EPUB raises, mocked playwright call
- **`tests/test_batch_manager.py`** — 5 tests: save/load, missing returns None, list, delete, pending filter
- **`tests/test_email_delivery.py`** — 5 tests: missing file, SMTP success, auth error, connection test pass/fail
- **`tests/test_cover_generator.py`** — rewritten with 10 tests covering all presets, genre map, prompt content, dimensions, placeholder output

### Changed
- `pyproject.toml` bumped to `1.5.0`

---

## [1.4.1] — 2026-06-30

### Fixed
- Route ordering in `web/app.py` (`/download/zip` before `/download`)
- `zip_files()` returns None on empty archive
- `sales_stats.py` error logging + `output_dir` param
- `jobs.js` XSS sanitization via `esc()` helper

---

## [1.4.0] — 2026-06-30

### Added
- `scripts/zip_export.py`, `scripts/sales_stats.py`
- `GET /jobs` dashboard, `GET /api/jobs`, `GET /download/zip/{job_id}`

---

## [1.3.1] — 2026-06-30

### Fixed
- Shell injection in `scheduler.py`, webhook error handling, `detect_chapters` dedup

---

## [1.3.0] — 2026-06-30

### Added
- `cover_generator.py`, `txt_to_docx.py`, `scheduler.py`, `webhooks.py`, Web Tools page

---

## [1.2.0] — 2026-06-30

### Added
- `categories.py` (20 genuri), `batch_pipeline.py`, Browse Genres web page

---

## [1.1.0] — 2026-06-30

### Added
- FastAPI Web UI cu DaisyUI dark theme

---

## [1.0.0] — 2026-06-30

### Added
- Pipeline complet: NovelClaw client, EPUB, KDP uploader, niche research, CI/CD

---

## [Unreleased]

### Planned
- KDP sales stats `/report/custom` cu autentificare 2FA bypass
- Multi-language premise generation
- SendGrid backend pentru `email_delivery.py`
