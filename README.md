# BookForge AI

> **One-command pipeline: Story Premise → Published on Amazon KDP**

BookForge AI is a fully automated pipeline that uses NovelClaw to generate complete novels, converts them to KDP-ready EPUB, can export DOCX for paperback workflows, optionally generates covers, and can auto-upload to Amazon KDP.

## Features

- Multi-agent fiction generation via NovelClaw
- EPUB export for Kindle publishing
- DOCX export for paperback preparation
- Optional KDP upload with Playwright
- Genre library with 20 KDP-friendly categories
- Batch generation pipeline
- FastAPI Web UI
- Cover generation hooks for Stable Diffusion / Canva
- Webhook notifications for batch jobs

## Quick Start

```bash
git clone https://github.com/Gzeu/bookforge-ai.git
cd bookforge-ai
pip install -r requirements.txt
python pipeline.py --interactive
```

## New in 1.3.0

- `scripts/cover_generator.py` for automated cover creation
- `scripts/txt_to_docx.py` for paperback-friendly DOCX export
- `scripts/scheduler.py` for recurring batch runs
- `scripts/webhooks.py` for Discord or generic callback notifications

## Roadmap

- KDP sales dashboard integration
- Full Docker Compose stack
- Improved cover layout presets
