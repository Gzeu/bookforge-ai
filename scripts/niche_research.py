#!/usr/bin/env python3
"""
BookForge AI — Amazon Niche & Keyword Research Helper
Uses AI to identify profitable KDP niches and keywords.
"""
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY   = os.getenv("OPENAI_API_KEY", "")
DEEPSEEK_KEY = os.getenv("DEEPSEEK_API_KEY", "")

REQUEST_TIMEOUT = 30  # seconds — prevents hang in Web UI background tasks

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


def research_niche(topic: str, provider: str = "deepseek") -> dict:
    prompt = RESEARCH_PROMPT.format(topic=topic)

    if provider == "deepseek" and DEEPSEEK_KEY:
        r = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {DEEPSEEK_KEY}",
                     "Content-Type": "application/json"},
            json={"model": "deepseek-chat",
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.7},
            timeout=REQUEST_TIMEOUT,
        )
        content = r.json()["choices"][0]["message"]["content"]
    elif OPENAI_KEY:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENAI_KEY}",
                     "Content-Type": "application/json"},
            json={"model": "gpt-4o-mini",
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=REQUEST_TIMEOUT,
        )
        content = r.json()["choices"][0]["message"]["content"]
    else:
        raise ValueError("No AI provider API key found in .env")

    start = content.find("{")
    end   = content.rfind("}") + 1
    if start >= 0 and end > start:
        return json.loads(content[start:end])
    return {"raw": content}


if __name__ == "__main__":
    import typer
    from rich import print as rprint

    app = typer.Typer()

    @app.command()
    def run(
        topic: str = typer.Argument(..., help="Book genre or topic"),
        provider: str = typer.Option("deepseek", "--provider", "-p"),
    ):
        print(f"🔍 Researching niche: {topic}")
        result = research_niche(topic, provider)
        rprint(result)

    app()
