# Contributing to BookForge AI

Thank you for your interest in contributing! This guide covers everything you need.

---

## Development Setup

```bash
git clone https://github.com/Gzeu/bookforge-ai.git
cd bookforge-ai
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
playwright install chromium
```

## Running Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=scripts --cov-report=term-missing
```

## Linting

```bash
ruff check scripts/ pipeline.py
ruff format scripts/ pipeline.py  # auto-fix
```

## Project Structure

```
bookforge-ai/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml          # lint + test on every push/PR
│   │   └── release.yml     # auto release on v* tags
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── scripts/
│   ├── generate_book.py    # NovelClaw API client
│   ├── txt_to_epub.py      # EPUB converter
│   ├── kdp_upload.py       # KDP Playwright uploader
│   └── niche_research.py   # AI niche/keyword research
├── tests/
│   ├── test_txt_to_epub.py
│   └── test_generate_book.py
├── pipeline.py             # main orchestrator
├── pyproject.toml
├── requirements.txt
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add cover generation via Stable Diffusion
fix: handle empty manuscript in EPUB converter
docs: update Quick Start in README
test: add unit tests for niche_research.py
chore: bump ebooklib to 0.19
```

## Branching

- `main` — stable, always passing CI
- `feat/your-feature` — new features
- `fix/bug-description` — bug fixes

## Release Process

```bash
# Update CHANGELOG.md, bump version in pyproject.toml, then:
git tag v1.1.0
git push origin v1.1.0
# GitHub Actions will create the release automatically
```

## Areas That Need Help

- 🎨 Cover generation (Stable Diffusion / Canva API integration)
- 🌐 Web UI (FastAPI + React for non-technical users)
- 📚 DOCX export for KDP print-on-demand
- 🔄 Batch pipeline (generate multiple books in parallel)
- 🇷🇴 Multi-language support testing
