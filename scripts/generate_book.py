#!/usr/bin/env python3
"""
BookForge AI — NovelClaw API Client
Generates a complete novel manuscript via NovelClaw REST API.
NovelClaw accepts any OpenAI-compatible provider slug via the 'provider' field.
"""
import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("NOVELCLAW_BASE_URL", "http://127.0.0.1:8012")
API_KEY  = os.getenv("NOVELCLAW_API_KEY", "change-this-agent-api-key")
PROVIDER = os.getenv("DEFAULT_PROVIDER", "mistral")
MANUSCRIPTS_DIR = Path(os.getenv("MANUSCRIPTS_DIR", "./manuscripts"))

# Provider slug mapping — NovelClaw accepts these slugs directly
# mistral   → Mistral AI (free tier)
# cerebras  → Cerebras AI (free tier)
# deepseek  → DeepSeek (~$0.007/book)
# openai    → OpenAI GPT-4o-mini
# anthropic → Anthropic Claude
# local_llm → Ollama (local, free)
VALID_PROVIDERS = {"mistral", "cerebras", "deepseek", "openai", "anthropic", "local_llm"}


class NovelClawClient:
    def __init__(self, base_url: str = BASE_URL, api_key: str = API_KEY):
        self.base_url = base_url.rstrip("/")
        self.headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

    def health(self) -> bool:
        try:
            r = requests.get(f"{self.base_url}/api/v1/health", headers=self.headers, timeout=5)
            return r.status_code == 200
        except Exception:
            return False

    def create_story(self, premise: str, chapters: int = 10,
                     provider: str = PROVIDER, language: str = "en") -> dict:
        if provider not in VALID_PROVIDERS:
            raise ValueError(f"Invalid provider '{provider}'. Valid: {VALID_PROVIDERS}")
        payload = {
            "provider": provider,
            "premise": premise,
            "preferred_language": language,
            "requested_chapters": chapters,
            "start": True,
        }
        r = requests.post(f"{self.base_url}/api/v1/stories",
                          headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()

    def get_story(self, story_id: int) -> dict:
        r = requests.get(f"{self.base_url}/api/v1/stories/{story_id}",
                         headers=self.headers)
        r.raise_for_status()
        return r.json()

    def wait_for_completion(self, story_id: int, poll_interval: int = 30) -> dict:
        from rich.progress import Progress, SpinnerColumn, TextColumn
        with Progress(SpinnerColumn(),
                      TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task("Generating...", total=None)
            while True:
                data = self.get_story(story_id)
                status = data.get("status", "unknown")
                done   = data.get("chapters_completed", 0)
                total  = data.get("chapters_requested", 0)
                progress.update(
                    task,
                    description=f"[cyan]{status}[/cyan]  "
                                f"[green]{done}/{total}[/green] chapters"
                )
                if status in ("completed", "failed", "cancelled"):
                    return data
                time.sleep(poll_interval)

    def export(self, story_id: int, output_path: str) -> str:
        r = requests.get(
            f"{self.base_url}/api/v1/stories/{story_id}/export",
            headers=self.headers
        )
        r.raise_for_status()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(r.text)
        return output_path

    def create_and_wait(self, premise: str, chapters: int = 10,
                        provider: str = PROVIDER, language: str = "en") -> int:
        story = self.create_story(premise, chapters, provider, language)
        story_id = story["id"]
        result = self.wait_for_completion(story_id)
        if result["status"] != "completed":
            raise RuntimeError(f"Generation failed: {result.get('error', 'unknown')}")
        return story_id


if __name__ == "__main__":
    import typer
    app = typer.Typer()

    @app.command()
    def run(
        premise: str = typer.Argument(..., help="Story premise"),
        chapters: int = typer.Option(10, "--chapters", "-c"),
        provider: str = typer.Option(PROVIDER, "--provider", "-p",
                                     help="mistral | cerebras | deepseek | openai | anthropic | local_llm"),
    ):
        client = NovelClawClient()
        if not client.health():
            typer.echo("❌ NovelClaw not running")
            raise typer.Exit(1)
        story_id = client.create_and_wait(premise, chapters, provider)
        out = str(MANUSCRIPTS_DIR / f"manuscript_{story_id}.txt")
        client.export(story_id, out)
        typer.echo(f"✅ Saved: {out}")

    app()
