#!/usr/bin/env python3
"""
BookForge AI — Amazon Niche & Keyword Research Helper
Uses AI to identify profitable KDP niches and keywords.
Supports: Mistral (free), Cerebras (free), DeepSeek, OpenAI.
"""
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

MISTRAL_KEY  = os.getenv("MISTRAL_API_KEY", "")
CEREBRAS_KEY = os.getenv("CEREBRAS_API_KEY", "")
OPENAI_KEY   = os.getenv("OPENAI_API_KEY", "")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")

REQUEST_TIMEOUT = 30  # seconds — prevents hang in Web UI background tasks

# Provider configs — all OpenAI-compatible
PROVIDERS = {
    "mistral": {
        "url": "https://api.mistral.ai/v1/chat/completions",
        "key_env": MISTRAL_KEY,
        "model": "mistral-small-latest",
    },
    "cerebras": {
        "url": "https://api.cerebras.ai/v1/chat/completions",
        "key_env": CEREBRAS_KEY,
        "model": "llama-4-scout-17b-16e-instruct",
    },
    "deepseek": {
        "url": "https://api.deepseek.com/v1/chat/completions",
        "key_env": DEEPSEEK_KEY,
        "model": "deepseek-chat",
    },
    "openai": {
        "url": "https://api.openai.com/v1/chat/completions",
        "key_env": OPENAI_KEY,
        "model": "gpt-4o-mini",
    },
}

RESEARCH_PROMPT = """
You are an Amazon KDP publishing strategist. Given a book genre or topic, provide:

1. Top 5 profitable sub-niches (low competition, decent search volume)
2. 7 KDP keywords (what readers actually search for)
3. Suggested book title + subtitle (SEO-optimized)
4. Ideal price point ($2.99–$9.99 range)
5. Estimated monthly revenue potential (conservative)
6. Sample book premise (2–3 sentences)

Genre/Topic: {topic}

Respond ONLY in valid JSON with keys:
niches, keywords, title, subtitle, price, monthly_revenue_estimate, sample_premise
"""


def research_niche(topic: str, provider: str = None) -> dict:
    # Auto-select first available provider if not specified
    if not provider:
        provider = _auto_provider()

    cfg = PROVIDERS.get(provider)
    if not cfg:
        raise ValueError(f"Unknown provider: {provider}. Options: {list(PROVIDERS)}")
    if not cfg["key_env"]:
        raise ValueError(f"API key for '{provider}' not set in .env")

    prompt = RESEARCH_PROMPT.format(topic=topic)
    r = requests.post(
        cfg["url"],
        headers={
            "Authorization": f"Bearer {cfg['key_env']}",
            "Content-Type": "application/json",
        },
        json={
            "model": cfg["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        },
        timeout=REQUEST_TIMEOUT,
    )
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]

    start = content.find("{")
    end   = content.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(content[start:end])
    return {"raw": content}


def _auto_provider() -> str:
    """Return the first provider with a key configured."""
    default = os.getenv("DEFAULT_PROVIDER", "mistral")
    if default in PROVIDERS and PROVIDERS[default]["key_env"]:
        return default
    for name, cfg in PROVIDERS.items():
        if cfg["key_env"]:
            return name
    raise ValueError("No AI provider API key found in .env")


def available_providers() -> list[str]:
    """Return list of providers that have a key configured."""
    return [name for name, cfg in PROVIDERS.items() if cfg["key_env"]]


if __name__ == "__main__":
    import typer
    from rich import print as rprint

    app = typer.Typer()

    @app.command()
    def run(
        topic: str = typer.Argument(..., help="Book genre or topic"),
        provider: str = typer.Option(None, "--provider", "-p",
                                     help="mistral | cerebras | deepseek | openai"),
    ):
        p = provider or _auto_provider()
        print(f"🔍 Researching niche: {topic} [provider: {p}]")
        result = research_niche(topic, p)
        rprint(result)

    app()
