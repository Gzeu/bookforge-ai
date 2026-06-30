# Changelog

All notable changes to **BookForge AI** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.4.0] — 2026-06-30

### Added
- **`scripts/zip_export.py`** — batch ZIP export utility
  - `zip_epub_batch(job_ids, jobs_store)` — zips all EPUB files from a batch job into a single archive
  - `zip_files(paths, output_path)` — generic multi-file ZIP helper
  - Output named `bookforge_batch_YYYYMMDD_HHMMSS.zip`, saved alongside EPUBs
- **`scripts/sales_stats.py`** — KDP sales stats scraper via Playwright
  - `KDPStatsScraper` class: login, navigate to reports, scrape units sold and royalties
  - Saves output as `kdp_stats_YYYYMMDD.json` in `manuscripts/`
  - Supports `--days` filter (default 30) and `--output` path override
  - CLI: `python -m scripts.sales_stats --days 30`
- **`GET /jobs`** — live Jobs Dashboard in Web UI
  - Full-page table of all jobs: ID, title, genre/type, status badge, progress, EPUB download, ZIP download
  - Auto-refreshes every 5 seconds via `jobs.js`
  - Status badges color-coded: queued (gray), running/generating/converting (yellow), done (green), error (red)
- **`GET /download/zip/{job_id}`** — download all EPUBs from a batch job as a single ZIP
- **`GET /api/jobs`** — full jobs list as JSON (used by dashboard polling)
- **`web/templates/jobs.html`** — dashboard template
- **`web/static/jobs.js`** — auto-refresh and dynamic status update script

### Changed
- **`web/app.py`** bumped to `v1.4.0`, added `/jobs`, `/download/zip/{job_id}`, `/api/jobs` routes
- **`pyproject.toml`** bumped to `1.4.0`

### Tests
- **`tests/test_zip_export.py`** — 5 tests: creates valid ZIP, includes all EPUBs, empty batch handled, output path correct, file count matches
- **`tests/test_sales_stats.py`** — 4 tests: output filename format, JSON structure, stats parsing, empty response handling

---

## [1.3.1] — 2026-06-30

### Fixed
- **`scripts/scheduler.py`** — shell injection fix (`shell=False` + allowlist), schedule reload per cycle
- **`scripts/webhooks.py`** — full try/except on all HTTP calls, non-fatal failures
- **`scripts/utils.py`** *(new)* — shared `detect_chapters()`, deduped from EPUB + DOCX converters
- **`scripts/cover_generator.py`** — `output_dir` param, no global state in tests
- **`scripts/batch_pipeline.py`** — explicit lambda capture, cleaner title generation

---

## [1.3.0] — 2026-06-30

### Added
- `scripts/cover_generator.py`, `scripts/txt_to_docx.py`, `scripts/scheduler.py`, `scripts/webhooks.py`
- `web/templates/tools.html` + `web/static/tools.js`

---

## [1.2.0] — 2026-06-30

### Added
- `scripts/categories.py` — 20-genre KDP library
- `scripts/batch_pipeline.py` — async batch generator
- `web/templates/categories.html` + `web/static/categories.js`

---

## [1.1.0] — 2026-06-30

### Added
- FastAPI Web UI (`web/`) with DaisyUI dark theme, 7 routes, background jobs

---

## [1.0.0] — 2026-06-30

### Added
- Full pipeline: `pipeline.py`, NovelClaw client, EPUB converter, KDP uploader, niche research, CI/CD

---

## [Unreleased]

### Planned
- Docker Compose full stack (NovelClaw + BookForge)
- Multi-provider cover layout presets
- Email delivery of finished EPUBs
