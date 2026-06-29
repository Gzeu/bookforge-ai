# 📚 BookForge AI

> **One-command pipeline: Story Premise → Published on Amazon KDP**

BookForge AI is a fully automated pipeline that uses [NovelClaw](https://github.com/iLearn-Lab/NovelClaw) (multi-agent long-form fiction engine) to generate complete novels, converts them to KDP-ready EPUB format, and optionally auto-uploads to Amazon Kindle Direct Publishing via Playwright. Includes a **Web UI** for non-technical users.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-required-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-web%20UI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![NovelClaw](https://img.shields.io/badge/Powered%20by-NovelClaw-F97316?style=flat-square)](https://github.com/iLearn-Lab/NovelClaw)

---

## 🏗️ Architecture

```
Premise (text)
     │
     ▼
┌─────────────────┐
│   NovelClaw     │  Multi-agent long-form fiction engine
│   (Docker)      │  DeepSeek / OpenAI / Anthropic / Local LLM
└────────┬────────┘
         │ manuscript .txt
         ▼
┌─────────────────┐
│  BookForge      │  txt_to_epub.py — KDP-ready EPUB with CSS
│  Converter      │  Cover image support, auto chapter detection
└────────┬────────┘
         │ .epub + cover.jpg
         ▼
┌─────────────────┐
│  Web UI / CLI   │  FastAPI UI or python pipeline.py
└─────────────────┘
         │
         ▼
┌─────────────────┐
│  KDP Uploader   │  Playwright — login, fill, upload, publish
│  (optional)     │
└─────────────────┘
```

---

## ✨ Features

- 🤖 **Multi-agent generation** via NovelClaw — memory-aware, chapter-by-chapter
- 🌐 **Web UI** — FastAPI + DaisyUI, live progress, EPUB download in browser
- 🔍 **Niche Research** — AI-powered KDP keyword & sub-niche finder
- 📦 **KDP-ready EPUB** — proper CSS, TOC, spine, cover embed
- 🔄 **Full CLI pipeline** — one command from premise to `.epub`
- 🌐 **Multiple AI providers** — DeepSeek (cheap), OpenAI, Anthropic, or local Ollama
- 📤 **KDP auto-upload** (optional) — Playwright, AI disclosure auto-checked
- 🐳 **Docker-first** — NovelClaw runs in Docker, scripts run locally

---

## 🚀 Quick Start

### 1. Clone + setup

```bash
git clone https://github.com/Gzeu/bookforge-ai.git
cd bookforge-ai
git clone https://github.com/iLearn-Lab/NovelClaw.git
cp .env.example .env
# → Edit .env with your API keys
```

### 2. Start NovelClaw

```bash
cd NovelClaw
cp .env.auth-portal.example apps/auth-portal/.env
cp .env.multiagent.example apps/multiagent/.env
cp .env.novelclaw.example apps/novelclaw/.env
# Edit apps/novelclaw/.env — set DEEPSEEK_API_KEY and APP_AGENT_API_KEY
./docker-start.sh    # Linux/Mac
.\docker-start.bat   # Windows
cd ..
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 4a. Web UI (recommended)

```bash
uvicorn web.app:app --host 0.0.0.0 --port 8020 --reload
# Open http://localhost:8020
```

### 4b. CLI (advanced)

```bash
python pipeline.py --interactive
# or
python pipeline.py \
  --premise "A blockchain trader discovers a global conspiracy." \
  --title "The Hash Conspiracy" \
  --author "Your Name" \
  --chapters 12
```

---

## 🌐 Web UI Pages

| Route | Description |
|---|---|
| `GET /` | Book generation form with provider selector |
| `POST /generate` | Submit new pipeline job |
| `GET /job/{id}` | Live job status with progress bar + log |
| `GET /download/{id}` | Download finished EPUB |
| `GET /research` | AI niche & keyword research form |
| `GET /health` | Health check for BookForge + NovelClaw |

---

## 📁 Project Structure

```
bookforge-ai/
├── .github/
│   ├── workflows/        # CI + auto-release
│   ├── ISSUE_TEMPLATE/   # bug + feature templates
│   └── pull_request_template.md
├── scripts/              # core pipeline modules
├── web/                  # FastAPI web UI
│   ├── app.py            # routes + background jobs
│   ├── static/app.js     # real-time polling
│   └── templates/        # Jinja2 (base, index, job, research)
├── tests/                # pytest unit tests
├── pipeline.py           # CLI orchestrator
├── pyproject.toml
├── requirements.txt
├── CHANGELOG.md
├── CONTRIBUTING.md
└── README.md
```

---

## 💰 AI Provider Costs (per book, ~50k tokens)

| Provider | Model | Cost | Quality |
|---|---|---|---|
| **DeepSeek** | deepseek-chat | ~$0.007 | ⭐⭐⭐⭐ |
| **OpenAI** | gpt-4o-mini | ~$0.03 | ⭐⭐⭐⭐⭐ |
| **Anthropic** | claude-3-haiku | ~$0.04 | ⭐⭐⭐⭐⭐ |
| **Ollama local** | llama3.2:3b | Free | ⭐⭐⭐ |

---

## ⚠️ Amazon KDP AI Policy

1. ✅ **Disclose** AI-generated content at upload (text, images, translations)
2. ✅ **Human-edit** before publishing — pure AI content may be rejected
3. ❌ **No flooding** — max ~3 books/day per account
4. ℹ️ **Copyright** — AI content cannot be copyrighted in the US
5. 💰 **Royalty** — 35% under $2.99 | 70% at $2.99–$9.99

---

## 🙏 Credits

- [NovelClaw](https://github.com/iLearn-Lab/NovelClaw) by iLearn-Lab — core fiction engine (MIT)
- [ebooklib](https://github.com/aerkalov/ebooklib) — EPUB generation
- [Playwright](https://playwright.dev) — KDP automation
- [FastAPI](https://fastapi.tiangolo.com) + [DaisyUI](https://daisyui.com) — Web UI

---

## 📄 License

MIT — free for personal and commercial use.
