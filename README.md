# BookForge AI 📚

> **AI-powered book publishing pipeline** — NovelClaw → EPUB/DOCX → Amazon KDP

[![CI](https://github.com/Gzeu/bookforge-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Gzeu/bookforge-ai/actions/workflows/ci.yml)
[![Release](https://github.com/Gzeu/bookforge-ai/actions/workflows/release.yml/badge.svg)](https://github.com/Gzeu/bookforge-ai/actions/workflows/release.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.5.0-green.svg)](CHANGELOG.md)

BookForge AI takes a story premise and automatically generates a full book manuscript via **NovelClaw**, converts it to KDP-ready EPUB and DOCX, generates a cover, and optionally uploads directly to **Amazon KDP** — all in one command or via the Web UI.

---

## ✨ Features

- **Full pipeline** — Premise → NovelClaw manuscript → EPUB → DOCX → KDP upload
- **20-genre library** — Thriller, Romance, Fantasy, Sci-Fi, Mystery, Horror, and 14 more
- **Async batch generation** — Multiple books concurrently via `asyncio.Semaphore`
- **Web UI** — FastAPI + DaisyUI dark theme, live job dashboard, polling API
- **6 cover presets** — `minimal`, `bold`, `noir`, `romance`, `scifi`, `fantasy`; auto-selected by genre
- **Scheduled jobs** — JSON-based scheduler with safe subprocess execution
- **Webhook notifications** — Discord + generic HTTP POST (batch start / done / fail)
- **KDP sales stats** — Playwright scraper: units sold + royalties, `/report/month` or `/report/custom` date range
- **Email delivery** — Send finished EPUB as attachment via SMTP (Gmail / Outlook / custom)
- **Batch state manager** — Persist + resume interrupted batches from disk
- **Docker Compose** — Full stack (`novelclaw` + `bookforge`) with one command

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────┐
│                  BookForge AI                      │
│                                                    │
│  CLI (pipeline.py / batch_pipeline.py)             │
│       │                                            │
│       ▼                                            │
│  NovelClaw API ──► Manuscript (.txt)               │
│       │                                            │
│       ├──► txt_to_epub.py   ──► .epub (KDP ready)  │
│       ├──► txt_to_docx.py   ──► .docx (paperback)  │
│       ├──► cover_generator.py ► .png (1.6:1 ratio) │
│       ├──► kdp_upload.py    ──► Amazon KDP         │
│       └──► email_delivery.py ► EPUB via SMTP       │
│                                                    │
│  Web UI (FastAPI :8020)                            │
│  ├── /           Single book form                  │
│  ├── /jobs       Live dashboard                    │
│  ├── /categories Browse genres + launch batch      │
│  └── /research   AI niche research                 │
└────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Option A — Docker Compose (recommended)

```bash
git clone https://github.com/Gzeu/bookforge-ai.git
cd bookforge-ai
cp .env.example .env        # fill in your API keys
docker compose up -d
```

**Web UI → http://localhost:8020**

### Option B — Local setup

**Requirements:** Python 3.10+, Chromium (via Playwright)

```bash
git clone https://github.com/Gzeu/bookforge-ai.git
cd bookforge-ai
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env
playwright install chromium
```

Start the Web UI:
```bash
uvicorn web.app:app --host 0.0.0.0 --port 8020 --reload
```

---

## ⚡ CLI Usage

### Single book

```bash
python pipeline.py \
  --premise "A detective discovers time travel in 1920s Berlin" \
  --title "The Timekeeper" \
  --author "A. Smith" \
  --chapters 12 \
  --provider deepseek
```

With KDP upload:
```bash
python pipeline.py --premise "..." --title "..." --author "..." --upload
```

Interactive mode (prompts for all fields):
```bash
python pipeline.py --interactive
```

### Batch generation

```bash
# 4 genres, 2 concurrent, 10 chapters each
python -m scripts.batch_pipeline --genres thriller,romance,mystery,scifi --concurrent 2

# All 20 genres
python -m scripts.batch_pipeline --genres all --concurrent 3 --chapters 8

# Custom provider + report output
python -m scripts.batch_pipeline --genres fantasy,horror --provider openai --report my_batch.json
```

### KDP sales stats

```bash
# Current month (default)
python -m scripts.sales_stats

# Custom date range (uses /report/custom)
python -m scripts.sales_stats --days 7
python -m scripts.sales_stats --days 90 --output q2_stats.json
```

---

## 🔧 Configuration — `.env`

Copy `.env.example` to `.env` and fill in your values:

```dotenv
# ── AI Providers (at least one required) ───────────────────────────────────
DEEPSEEK_API_KEY=sk-...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_PROVIDER=deepseek          # deepseek | openai | anthropic | local_llm

# ── NovelClaw (local Docker or remote) ─────────────────────────────────────
NOVELCLAW_BASE_URL=http://localhost:8000
NOVELCLAW_API_KEY=your_key_here

# ── Amazon KDP ──────────────────────────────────────────────────────────────
KDP_EMAIL=your@email.com
KDP_PASSWORD=your_kdp_password

# ── Cover generation (optional) ─────────────────────────────────────────────
SD_WEBUI_URL=http://localhost:7860  # Stable Diffusion WebUI
CANVA_API_KEY=                      # Canva API (alternative)

# ── Webhooks (optional) ──────────────────────────────────────────────────────
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# ── Email delivery (optional) ────────────────────────────────────────────────
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=your_app_password     # Gmail: use App Password, not account password
EMAIL_FROM=BookForge AI <your@gmail.com>

# ── Storage paths ─────────────────────────────────────────────────────────────
MANUSCRIPTS_DIR=./manuscripts
EPUB_OUTPUT_DIR=./epub_output
COVERS_DIR=./covers
```

> **Gmail tip:** Generate an App Password at https://myaccount.google.com/apppasswords (2FA must be enabled).

---

## 🌐 Web UI — All Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Home — single book generation form |
| `POST` | `/generate` | Submit a new book job (background task) |
| `GET` | `/jobs` | **Live dashboard** — all jobs, status, progress, download links |
| `GET` | `/job/{id}` | Single job detail page with live log |
| `GET` | `/categories` | Browse all 20 genres, launch batch from UI |
| `POST` | `/batch` | Submit a batch job |
| `GET` | `/research` | AI niche & keyword research form |
| `POST` | `/research` | Run niche research |
| `GET` | `/download/{id}` | Download EPUB for a single job |
| `GET` | `/download/zip/{id}` | Download all EPUBs from a batch as ZIP |
| `GET` | `/health` | Health check — BookForge + NovelClaw status |
| `GET` | `/api/jobs` | Jobs list JSON (polled by dashboard every 5s) |
| `GET` | `/api/job/{id}` | Single job status JSON |
| `GET` | `/api/genres` | All genres JSON |
| `GET` | `/api/genres/{id}/premise` | Random premise for a genre |

---

## 📦 Scripts Reference

| Script | CLI command | Description |
|---|---|---|
| `pipeline.py` | `python pipeline.py --interactive` | Main orchestrator (single book) |
| `scripts/batch_pipeline.py` | `python -m scripts.batch_pipeline` | Async batch generation |
| `scripts/batch_manager.py` | `python -m scripts.batch_manager` | Disk-persisted batch state + resume |
| `scripts/generate_book.py` | imported | NovelClaw API client |
| `scripts/txt_to_epub.py` | imported | EPUB converter (KDP-ready) |
| `scripts/txt_to_docx.py` | imported | DOCX converter (paperback) |
| `scripts/cover_generator.py` | imported | Cover generation (SD / Canva / placeholder) |
| `scripts/kdp_upload.py` | imported | Playwright KDP uploader |
| `scripts/sales_stats.py` | `python -m scripts.sales_stats --days 30` | KDP stats scraper |
| `scripts/scheduler.py` | `python -m scripts.scheduler` | Scheduled jobs runner |
| `scripts/webhooks.py` | imported | Discord + HTTP webhook notifications |
| `scripts/email_delivery.py` | imported | EPUB email delivery via SMTP |
| `scripts/niche_research.py` | imported | AI niche & keyword research |
| `scripts/categories.py` | imported | 20-genre library with premise templates |
| `scripts/zip_export.py` | imported | Batch EPUB → ZIP export |

---

## 🎨 Cover Presets

| Preset | Best for | Style |
|---|---|---|
| `noir` | Thriller, Mystery, Crime, Horror | Dark, moody, cinematic shadows |
| `romance` | Romance, Paranormal | Warm tones, soft bokeh, intimate |
| `scifi` | Sci-Fi | Futuristic, neon, space |
| `fantasy` | Fantasy | Epic landscapes, magical, detailed |
| `minimal` | Literary, Self-Help, Memoir | Clean typography, white background |
| `bold` | Business, non-fiction | High contrast, strong colors |

Presets are auto-selected by genre, or override with `--preset`:

```python
from scripts.cover_generator import generate_cover_sd
generate_cover_sd("My Novel", "J. Doe", genre_id="thriller")          # auto → noir
generate_cover_sd("My Novel", "J. Doe", preset_name="minimal")        # explicit
```

---

## 📧 Email Delivery

```python
from scripts.email_delivery import EmailDelivery

ed = EmailDelivery()  # reads SMTP_* from .env
ed.send_epub(
    to="reader@example.com",
    epub_path="./epub_output/my_book.epub",
    title="The Timekeeper",
    author="A. Smith",
)
```

Test your SMTP config before sending:
```python
assert ed.test_connection()  # True = credentials valid
```

---

## 🧪 Tests

```bash
pytest                            # run all (11 test files, 60+ tests)
pytest tests/ -v                  # verbose output
pytest --cov=scripts --cov-report=term-missing   # coverage report
pytest tests/test_pipeline.py -v  # single module
```

**Coverage:**

| Module | Tests |
|---|---|
| `pipeline.py` | `test_pipeline.py` — 4 tests |
| `batch_pipeline.py` | `test_batch_pipeline.py` — 7 tests |
| `batch_manager.py` | `test_batch_manager.py` — 5 tests |
| `kdp_upload.py` | `test_kdp_upload.py` — 3 tests |
| `email_delivery.py` | `test_email_delivery.py` — 5 tests |
| `cover_generator.py` | `test_cover_generator.py` — 10 tests |
| `sales_stats.py` | `test_sales_stats.py` — 4 tests |
| `zip_export.py` | `test_zip_export.py` — 3 tests |
| `txt_to_epub.py` | `test_txt_to_epub.py` — 5 tests |
| `categories.py` | `test_categories.py` — 5 tests |
| `utils.py` | `test_utils.py` — 4 tests |

---

## 🐳 Docker

```bash
# Full stack (NovelClaw + BookForge)
docker compose up -d

# BookForge only (if NovelClaw runs elsewhere)
docker build -t bookforge-ai .
docker run -p 8020:8020 --env-file .env bookforge-ai

# View logs
docker compose logs -f bookforge
docker compose logs -f novelclaw

# Stop
docker compose down
```

Volumes:
- `bookforge_data` → `/data` (manuscripts, EPUBs, covers)
- `novelclaw_data` → NovelClaw story database
- `./schedules` → `/app/schedules` (JSON schedule files, bind-mounted)

---

## 📁 Project Structure

```
bookforge-ai/
├── pipeline.py              # Main CLI orchestrator
├── docker-compose.yml       # Full stack compose
├── Dockerfile               # Production image
├── pyproject.toml           # Dependencies + metadata
├── .env.example             # Config template
│
├── scripts/
│   ├── generate_book.py     # NovelClaw API client
│   ├── txt_to_epub.py       # EPUB converter
│   ├── txt_to_docx.py       # DOCX converter
│   ├── cover_generator.py   # Cover gen (SD/Canva/placeholder)
│   ├── kdp_upload.py        # KDP Playwright uploader
│   ├── batch_pipeline.py    # Async batch engine
│   ├── batch_manager.py     # Batch state persistence
│   ├── email_delivery.py    # SMTP email delivery
│   ├── sales_stats.py       # KDP stats scraper
│   ├── scheduler.py         # Job scheduler
│   ├── webhooks.py          # Discord/HTTP notifications
│   ├── niche_research.py    # AI niche research
│   ├── categories.py        # 20-genre library
│   ├── zip_export.py        # Batch ZIP export
│   └── utils.py             # Shared utilities
│
├── web/
│   ├── app.py               # FastAPI app (15 routes)
│   ├── templates/           # Jinja2 HTML (DaisyUI dark)
│   └── static/              # CSS, JS (jobs.js dashboard)
│
├── tests/                   # 11 test files, 60+ tests
├── manuscripts/             # Generated .txt manuscripts
├── epub_output/             # Generated .epub files
└── covers/                  # Generated cover images
```

---

## 📄 License

[MIT](LICENSE) — George Pricop
