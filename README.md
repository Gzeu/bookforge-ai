# BookForge AI 📚

> **AI-powered book publishing pipeline** — NovelClaw → EPUB/DOCX → Amazon KDP

[![CI](https://github.com/Gzeu/bookforge-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/Gzeu/bookforge-ai/actions/workflows/ci.yml)
[![Release](https://github.com/Gzeu/bookforge-ai/actions/workflows/release.yml/badge.svg)](https://github.com/Gzeu/bookforge-ai/actions/workflows/release.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.5.0-green.svg)](CHANGELOG.md)

BookForge AI takes a story premise and automatically generates a full book manuscript, converts it to KDP-ready EPUB and DOCX, generates a cover, and optionally uploads directly to Amazon KDP — all in one command or via the Web UI.

---

## ✨ Features

- **Full pipeline**: Premise → NovelClaw manuscript → EPUB → DOCX → KDP upload
- **20-genre library**: Thriller, Romance, Fantasy, Sci-Fi, Mystery, Horror, and 14 more
- **Async batch generation**: Generate multiple books concurrently with `asyncio.Semaphore`
- **Web UI**: FastAPI + DaisyUI dark theme with live job dashboard
- **Cover generation**: Stable Diffusion WebUI or Canva API, KDP-safe 1.6:1 ratio
- **Scheduled jobs**: JSON-based scheduler with safe subprocess execution
- **Webhook notifications**: Discord + generic HTTP POST (batch start/done/fail)
- **KDP sales stats**: Playwright scraper for units sold and royalties
- **Email delivery**: Send finished EPUB directly to any email after generation
- **Docker Compose**: Full stack with one command

---

## 🚀 Quick Start

### Option A — Docker Compose (recommended)

```bash
git clone https://github.com/Gzeu/bookforge-ai.git
cd bookforge-ai
cp .env.example .env        # fill in your API keys
docker compose up -d
```

Web UI: **http://localhost:8020**

### Option B — Local setup

```bash
git clone https://github.com/Gzeu/bookforge-ai.git
cd bookforge-ai
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env        # fill in your API keys
playwright install chromium
```

Start Web UI:
```bash
uvicorn web.app:app --host 0.0.0.0 --port 8020 --reload
```

CLI — single book:
```bash
python pipeline.py --premise "A detective discovers time travel" \
  --title "The Timekeeper" --author "A. Smith" --chapters 12
```

CLI — batch:
```bash
python -m scripts.batch_pipeline --genres thriller,romance,mystery --concurrent 2
```

---

## 🔧 Configuration — `.env`

```dotenv
# AI Providers (at least one required)
DEEPSEEK_API_KEY=sk-...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
DEFAULT_PROVIDER=deepseek

# NovelClaw (local Docker)
NOVELCLAW_BASE_URL=http://localhost:8000
NOVELCLAW_API_KEY=your_key_here

# Amazon KDP
KDP_EMAIL=your@email.com
KDP_PASSWORD=your_password

# Cover generation (optional)
SD_WEBUI_URL=http://localhost:7860
CANVA_API_KEY=

# Webhooks (optional)
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Email delivery (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=app_password_here
EMAIL_FROM=BookForge AI <your@gmail.com>

# Paths
MANUSCRIPTS_DIR=./manuscripts
EPUB_OUTPUT_DIR=./epub_output
COVERS_DIR=./covers
```

---

## 🌐 Web UI Routes

| Route | Description |
|---|---|
| `GET /` | Home — generate a single book |
| `GET /jobs` | **Live dashboard** — all jobs, status, progress, downloads |
| `GET /categories` | Browse 20 genres, launch batch |
| `GET /research` | AI niche & keyword research |
| `GET /job/{id}` | Single job detail + log |
| `GET /download/{id}` | Download EPUB |
| `GET /download/zip/{id}` | Download batch as ZIP |
| `GET /health` | Health check |
| `GET /api/jobs` | Jobs JSON (dashboard polling) |

---

## 📦 Scripts

| Script | CLI | Description |
|---|---|---|
| `pipeline.py` | `python pipeline.py --interactive` | Main orchestrator |
| `scripts/batch_pipeline.py` | `python -m scripts.batch_pipeline` | Async batch |
| `scripts/batch_manager.py` | `python -m scripts.batch_manager` | Batch job state manager |
| `scripts/sales_stats.py` | `python -m scripts.sales_stats --days 30` | KDP stats scraper |
| `scripts/scheduler.py` | `python -m scripts.scheduler` | Scheduled jobs runner |
| `scripts/email_delivery.py` | imported by pipeline | EPUB email sender |

---

## 🧪 Tests

```bash
pytest                        # run all
pytest tests/ -v              # verbose
pytest --cov=scripts          # with coverage
```

---

## 📄 License

[MIT](LICENSE) — George Pricop
