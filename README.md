# 📚 BookForge AI

> **One-command pipeline: Story Premise → Published on Amazon KDP**

BookForge AI is a fully automated pipeline that uses [NovelClaw](https://github.com/iLearn-Lab/NovelClaw) (multi-agent long-form fiction engine) to generate complete novels, converts them to KDP-ready EPUB format, and optionally auto-uploads to Amazon Kindle Direct Publishing via Playwright.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-required-2496ED?style=flat-square&logo=docker)](https://docker.com)
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
│  KDP Uploader   │  Playwright automation — login, fill metadata,
│  (optional)     │  upload manuscript + cover, set price, publish
└─────────────────┘
```

---

## ✨ Features

- 🤖 **Multi-agent generation** via NovelClaw — memory-aware, chapter-by-chapter
- 📦 **KDP-ready EPUB** — proper CSS, TOC, spine, cover embed
- 🔄 **Full pipeline** — one command from premise to `.epub`
- 🌐 **Multiple AI providers** — DeepSeek (cheap), OpenAI, Anthropic, or local Ollama
- 🤖 **REST API automation** — scriptable via NovelClaw Agent API
- 📤 **KDP auto-upload** (optional) — Playwright-based, AI disclosure auto-checked
- 🐳 **Docker-first** — no local Python env needed for generation

---

## 📋 Requirements

| Tool | Version | Notes |
|---|---|---|
| Docker Desktop | 24+ | For NovelClaw services |
| Python | 3.10+ | For pipeline scripts |
| Node.js | 18+ | Optional, for Playwright |
| Git | any | Clone repos |
| RAM | 8GB+ | Recommended |

---

## 🚀 Quick Start

### 1. Clone this repo and NovelClaw

```bash
git clone https://github.com/Gzeu/bookforge-ai.git
cd bookforge-ai

git clone https://github.com/iLearn-Lab/NovelClaw.git
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start NovelClaw services

```bash
cd NovelClaw
cp .env.auth-portal.example apps/auth-portal/.env
cp .env.multiagent.example apps/multiagent/.env
cp .env.novelclaw.example apps/novelclaw/.env
# Edit apps/novelclaw/.env with your API key and AGENT_API_KEY
./docker-start.sh   # Linux/Mac
# OR
.\docker-start.bat  # Windows
cd ..
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 5. Run the pipeline

```bash
# Generate + convert to EPUB
python pipeline.py \
  --premise "A crypto trader in Bucharest discovers a hidden blockchain controlling global markets." \
  --title "The Hash Conspiracy" \
  --author "Your Name" \
  --chapters 12

# Or use the interactive mode
python pipeline.py --interactive
```

---

## 🔧 Configuration

Copy `.env.example` to `.env` and fill in:

```env
# NovelClaw connection
NOVELCLAW_BASE_URL=http://127.0.0.1:8012
NOVELCLAW_API_KEY=your-agent-api-key

# AI Provider (at least one)
DEEPSEEK_API_KEY=sk-...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Default provider (deepseek recommended for cost)
DEFAULT_PROVIDER=deepseek

# Amazon KDP (optional - for auto-upload)
KDP_EMAIL=your@email.com
KDP_PASSWORD=your_kdp_password
```

---

## 📁 Project Structure

```
bookforge-ai/
├── NovelClaw/              # Clone separately — fiction generation engine
├── scripts/
│   ├── generate_book.py    # NovelClaw API client — generate + export
│   ├── txt_to_epub.py      # Manuscript → KDP-ready EPUB converter
│   ├── kdp_upload.py       # Amazon KDP Playwright uploader (optional)
│   └── niche_research.py   # Amazon keyword/niche research helper
├── pipeline.py             # Main orchestrator — runs full pipeline
├── requirements.txt        # Python dependencies
├── .env.example            # Environment template
├── LICENSE                 # MIT
└── README.md
```

---

## 📖 Usage Examples

### Generate only (no upload)

```bash
python pipeline.py \
  --premise "A detective in 2040 investigates AI-generated crimes." \
  --title "Silicon Noir" \
  --author "J. Smith" \
  --chapters 10 \
  --no-upload
```

### Generate + convert + upload to KDP

```bash
python pipeline.py \
  --premise "A romance set inside a decentralized metaverse." \
  --title "Heart on the Chain" \
  --author "Your Name" \
  --chapters 15 \
  --price 3.99 \
  --cover covers/romance_cover.jpg \
  --upload
```

### API-only (use in your own scripts)

```python
from scripts.generate_book import NovelClawClient
from scripts.txt_to_epub import txt_to_epub

client = NovelClawClient()
story_id = client.create_and_wait(
    premise="Your story premise here",
    chapters=10
)
manuscript = client.export(story_id, "manuscript.txt")
txt_to_epub("manuscript.txt", "book.epub", "Title", "Author")
```

---

## 💰 AI Provider Costs (estimated per book)

| Provider | Model | Cost/book (~50k tokens) | Quality |
|---|---|---|---|
| **DeepSeek** | deepseek-chat | ~$0.007 | ⭐⭐⭐⭐ |
| **OpenAI** | gpt-4o-mini | ~$0.03 | ⭐⭐⭐⭐⭐ |
| **Anthropic** | claude-3-haiku | ~$0.04 | ⭐⭐⭐⭐⭐ |
| **Ollama local** | llama3.2:3b | Free | ⭐⭐⭐ |

---

## ⚠️ Amazon KDP AI Policy

When publishing AI-assisted content on KDP:

1. ✅ **Disclose** AI-generated content (text, images, translations) — mandatory
2. ✅ **Human edit** the manuscript before publishing — pure AI content may be rejected
3. ❌ **Do not flood** — max ~3 books/day per account to avoid suspension
4. ℹ️ **Copyright** — AI-generated content cannot be copyrighted in the US
5. 💰 **Royalty** — 35% under $2.99 | 70% between $2.99–$9.99

---

## 🙏 Credits

- [NovelClaw](https://github.com/iLearn-Lab/NovelClaw) by iLearn-Lab — core fiction generation engine (MIT)
- [ebooklib](https://github.com/aerkalov/ebooklib) — EPUB generation
- [Playwright](https://playwright.dev) — KDP automation

---

## 📄 License

MIT — free for personal and commercial use.
