#!/usr/bin/env python3
"""
BookForge AI — FastAPI Web UI v2.0.1
Run: uvicorn web.app:app --host 0.0.0.0 --port 8020 --reload
"""
import asyncio
import os
import json
import uuid
from pathlib import Path

from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv

load_dotenv()

BASE_DIR        = Path(__file__).parent
MANUSCRIPTS_DIR = Path(os.getenv("MANUSCRIPTS_DIR", "./manuscripts"))
EPUB_OUTPUT_DIR = Path(os.getenv("EPUB_OUTPUT_DIR", "./epub_output"))
COVERS_DIR      = Path(os.getenv("COVERS_DIR", "./covers"))

for d in (MANUSCRIPTS_DIR, EPUB_OUTPUT_DIR, COVERS_DIR):
    d.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="BookForge AI", version="2.0.1")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

_jinja_env = Environment(
    loader=FileSystemLoader(str(BASE_DIR / "templates")),
    autoescape=True,
    cache_size=0,
)


def _render(template_name: str, context: dict) -> HTMLResponse:
    html = _jinja_env.get_template(template_name).render(context)
    return HTMLResponse(content=html)


JOBS: dict[str, dict] = {}

STATUS_COLORS = {
    "queued": "badge-neutral",
    "generating": "badge-warning",
    "running": "badge-warning",
    "converting": "badge-warning",
    "done": "badge-success",
    "error": "badge-error",
    "failed": "badge-error",
}

# ── Active Cerebras model (update here if deprecated) ──────────────────────
CEREBRAS_MODEL = "llama-3.3-70b"   # llama3.1-8b | llama-3.3-70b | gpt-oss-120b
# ───────────────────────────────────────────────────────────────────────────


def _get_providers() -> list[dict]:
    providers = []
    if os.getenv("MISTRAL_API_KEY"):
        providers.append({"slug": "mistral", "label": "Mistral AI", "cost": "Free"})
    if os.getenv("CEREBRAS_API_KEY"):
        providers.append({"slug": "cerebras", "label": "Cerebras AI", "cost": "Free"})
    if os.getenv("DEEPSEEK_API_KEY"):
        providers.append({"slug": "deepseek", "label": "DeepSeek", "cost": "~$0.007/book"})
    if os.getenv("OPENAI_API_KEY"):
        providers.append({"slug": "openai", "label": "OpenAI", "cost": "~$0.03/book"})
    if os.getenv("ANTHROPIC_API_KEY"):
        providers.append({"slug": "anthropic", "label": "Anthropic", "cost": "~$0.04/book"})
    providers.append({"slug": "local_llm", "label": "Local LLM (Ollama)", "cost": "Free"})
    return providers or [{"slug": "mistral", "label": "Mistral AI (key missing)", "cost": ""}]


def _cerebras_or_mistral_completion(prompt: str, temperature: float = 0.9, max_tokens: int = 300) -> str:
    """Call Cerebras first (llama-3.3-70b), fall back to Mistral. Returns raw text."""
    cerebras_key = os.getenv("CEREBRAS_API_KEY")
    mistral_key  = os.getenv("MISTRAL_API_KEY")

    if cerebras_key:
        try:
            from cerebras.cloud.sdk import Cerebras
            client = Cerebras(api_key=cerebras_key)
            resp = client.chat.completions.create(
                model=CEREBRAS_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            # Log and fall through to Mistral
            print(f"[Cerebras] {e} — falling back to Mistral")

    if mistral_key:
        try:
            from mistralai import Mistral
            client = Mistral(api_key=mistral_key)
            resp = client.chat.complete(
                model="mistral-small-latest",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Mistral] {e}")

    raise RuntimeError("No AI provider available. Set CEREBRAS_API_KEY or MISTRAL_API_KEY in .env")


def _run_pipeline_sync(job_id: str, premise: str, title: str, author: str,
                       chapters: int, provider: str, description: str):
    import sys, time
    sys.path.insert(0, str(Path(__file__).parent.parent))
    JOBS[job_id]["status"] = "generating"
    JOBS[job_id]["log"] = ["Starting NovelClaw generation..."]
    try:
        from scripts.generate_book import NovelClawClient
        client = NovelClawClient()
        if not client.health():
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["log"].append("ERROR: NovelClaw not running.")
            return
        story = client.create_story(premise, chapters, provider)
        story_id = story["id"]
        JOBS[job_id]["story_id"] = story_id
        JOBS[job_id]["log"].append(f"Story created (ID={story_id}). Generating chapters...")
        while True:
            data = client.get_story(story_id)
            status = data.get("status", "unknown")
            done  = data.get("chapters_completed", 0)
            total = data.get("chapters_requested", 0)
            JOBS[job_id]["progress"] = {"done": done, "total": total, "status": status}
            JOBS[job_id]["log"].append(f"  [{status}] {done}/{total} chapters")
            if status in ("completed", "failed", "cancelled"):
                break
            time.sleep(20)
        if data["status"] != "completed":
            JOBS[job_id]["status"] = "error"
            JOBS[job_id]["log"].append(f"Generation failed: {data.get('error', 'unknown')}")
            return
        manuscript_file = str(MANUSCRIPTS_DIR / f"manuscript_{story_id}.txt")
        client.export(story_id, manuscript_file)
        JOBS[job_id]["log"].append(f"Manuscript exported: {manuscript_file}")
        JOBS[job_id]["status"] = "converting"
        JOBS[job_id]["log"].append("Converting to EPUB...")
        from scripts.txt_to_epub import txt_to_epub
        safe = title.lower().replace(" ", "_")[:30]
        epub_file = str(EPUB_OUTPUT_DIR / f"{safe}_{story_id}.epub")
        txt_to_epub(manuscript_file, epub_file, title, author, description=description)
        JOBS[job_id]["log"].append(f"EPUB created: {epub_file}")
        JOBS[job_id]["epub_file"] = epub_file
        JOBS[job_id]["epub_name"] = Path(epub_file).name
        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["log"].append("Pipeline complete!")
    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["log"].append(f"ERROR: {e}")


def _run_batch_sync(batch_job_id: str, genre_ids: list[str], author: str,
                    chapters: int, provider: str):
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.batch_pipeline import build_batch_from_genres, run_batch, save_batch_report
    JOBS[batch_job_id]["status"] = "running"
    JOBS[batch_job_id]["log"].append(f"Starting batch: {len(genre_ids)} genres")
    try:
        jobs = build_batch_from_genres(genre_ids, author, chapters, provider)
        JOBS[batch_job_id]["log"].append(f"Queued {len(jobs)} books")
        results = asyncio.run(run_batch(jobs, max_concurrent=2))
        done_count = sum(1 for j in results if j.status == "done")
        fail_count = sum(1 for j in results if j.status == "failed")
        epub_files = [j.epub_file for j in results if j.epub_file]
        JOBS[batch_job_id].update({
            "status": "done",
            "batch_results": [
                {"genre": j.genre_id, "title": j.title,
                 "status": j.status, "epub": j.epub_file, "error": j.error}
                for j in results
            ],
            "epub_files": epub_files,
            "progress": {"done": done_count, "total": len(jobs)},
        })
        JOBS[batch_job_id]["log"].append(
            f"Batch complete: {done_count} done, {fail_count} failed"
        )
        report_path = str(MANUSCRIPTS_DIR / f"batch_report_{batch_job_id}.json")
        save_batch_report(results, report_path)
    except Exception as e:
        JOBS[batch_job_id]["status"] = "error"
        JOBS[batch_job_id]["log"].append(f"ERROR: {e}")


# ── Routes ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return _render("index.html", {
        "request": request,
        "providers": _get_providers(),
        "jobs": list(JOBS.values())[-10:],
    })


@app.post("/api/generate-premise")
async def generate_premise(request: Request):
    """Generate a story premise from a genre using Cerebras (fast)."""
    body = await request.json()
    genre = body.get("genre", "thriller").strip() or "thriller"
    prompt = (
        f"Write a single compelling, original story premise for a {genre} novel.\n"
        f"Rules:\n"
        f"- 2-3 sentences maximum\n"
        f"- Vivid, specific details (location, character, conflict)\n"
        f"- Amazon KDP commercial style — hook the reader immediately\n"
        f"- No title, no chapter info, just the premise\n"
        f"Output only the premise text, nothing else."
    )
    try:
        raw = _cerebras_or_mistral_completion(prompt, temperature=0.95, max_tokens=150)
        return JSONResponse({"premise": raw})
    except RuntimeError as e:
        raise HTTPException(503, str(e))


@app.post("/api/generate-titles")
async def generate_titles(request: Request):
    """Generate 4 book title suggestions from a premise using Cerebras."""
    body = await request.json()
    premise = body.get("premise", "").strip()
    if not premise:
        raise HTTPException(400, "premise is required")
    prompt = (
        f"Generate exactly 4 compelling, marketable book titles for this premise:\n"
        f"{premise}\n\n"
        f"Rules:\n"
        f"- One title per line\n"
        f"- No numbering, no quotes, no explanations\n"
        f"- Make them punchy, commercial, Amazon KDP style\n"
        f"Output only the 4 titles, nothing else."
    )
    try:
        raw = _cerebras_or_mistral_completion(prompt, temperature=0.9, max_tokens=200)
        titles = [t.strip() for t in raw.split("\n") if t.strip()][:4]
        if not titles:
            titles = ["The Hidden Protocol", "Dark Chain", "Zero Trust", "The Cipher Event"]
        return JSONResponse({"titles": titles})
    except RuntimeError as e:
        raise HTTPException(503, str(e))


@app.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request, background_tasks: BackgroundTasks,
    premise: str = Form(...), title: str = Form(...), author: str = Form(...),
    chapters: int = Form(10), provider: str = Form("mistral"), description: str = Form(""),
):
    job_id = str(uuid.uuid4())[:8]
    JOBS[job_id] = {
        "id": job_id, "title": title, "author": author, "chapters": chapters,
        "provider": provider, "status": "queued",
        "progress": {"done": 0, "total": chapters},
        "log": [], "epub_file": None, "epub_name": None, "is_batch": False,
    }
    background_tasks.add_task(
        _run_pipeline_sync, job_id, premise, title, author, chapters, provider, description
    )
    return _render("job.html", {"request": request, "job": JOBS[job_id]})


@app.get("/job/{job_id}", response_class=HTMLResponse)
async def job_page(request: Request, job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return _render("job.html", {"request": request, "job": job})


@app.get("/api/job/{job_id}")
async def job_status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return JSONResponse(job)


@app.get("/jobs", response_class=HTMLResponse)
async def jobs_dashboard(request: Request):
    return _render("jobs.html", {
        "request": request,
        "jobs": list(JOBS.values()),
        "status_colors": STATUS_COLORS,
    })


@app.get("/api/jobs")
async def api_jobs():
    jobs_list = [
        {
            **{k: v for k, v in job.items() if k != "log"},
            "log_tail": (job.get("log") or [""])[-3:],
            "status_color": STATUS_COLORS.get(job.get("status", ""), "badge-neutral"),
        }
        for job in JOBS.values()
    ]
    return JSONResponse(jobs_list)


@app.get("/download/zip/{job_id}")
async def download_batch_zip(job_id: str):
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from scripts.zip_export import zip_epub_batch
    zip_path = zip_epub_batch(job_id, JOBS, output_dir=EPUB_OUTPUT_DIR)
    if not zip_path:
        raise HTTPException(404, "No EPUBs available for this job")
    return FileResponse(
        zip_path, media_type="application/zip", filename=Path(zip_path).name
    )


@app.get("/download/{job_id}")
async def download_epub(job_id: str):
    job = JOBS.get(job_id)
    if not job or not job.get("epub_file"):
        raise HTTPException(404, "EPUB not ready")
    return FileResponse(
        job["epub_file"], media_type="application/epub+zip", filename=job["epub_name"]
    )


@app.get("/research", response_class=HTMLResponse)
async def research_page(request: Request):
    from scripts.niche_research import available_providers
    return _render("research.html", {
        "request": request,
        "result": None,
        "available_providers": available_providers(),
    })


@app.post("/research", response_class=HTMLResponse)
async def research_submit(request: Request, topic: str = Form(...), provider: str = Form(None)):
    from scripts.niche_research import research_niche, available_providers
    avail = available_providers()
    if "cerebras" in avail:
        provider = "cerebras"
    elif "mistral" in avail:
        provider = "mistral"
    elif avail:
        provider = avail[0]
    try:
        result = research_niche(topic, provider)
    except Exception as e:
        result = {"error": str(e)}
    return _render("research.html", {
        "request": request,
        "result": result,
        "topic": topic,
        "available_providers": available_providers(),
    })


@app.get("/categories", response_class=HTMLResponse)
async def categories_page(request: Request):
    from scripts.categories import get_all_genres
    from dataclasses import asdict
    genres = get_all_genres()
    genres_json = json.dumps({g.id: asdict(g) for g in genres})
    return _render("categories.html", {
        "request": request, "genres": genres, "genres_json": genres_json,
    })


@app.post("/batch", response_class=HTMLResponse)
async def batch_generate(
    request: Request, background_tasks: BackgroundTasks,
    genre_ids: list[str] = Form(...), author: str = Form("BookForge AI"),
    chapters: int = Form(10), provider: str = Form("mistral"),
):
    batch_id = "batch_" + str(uuid.uuid4())[:8]
    JOBS[batch_id] = {
        "id": batch_id,
        "title": f"Batch: {', '.join(genre_ids[:3])}{'...' if len(genre_ids) > 3 else ''}",
        "author": author, "chapters": chapters, "provider": provider,
        "status": "queued", "is_batch": True, "genre_ids": genre_ids,
        "batch_results": [], "epub_files": [],
        "progress": {"done": 0, "total": len(genre_ids)},
        "log": [f"Batch queued: {len(genre_ids)} genres"],
    }
    background_tasks.add_task(
        _run_batch_sync, batch_id, genre_ids, author, chapters, provider
    )
    return _render("job.html", {"request": request, "job": JOBS[batch_id]})


@app.get("/api/genres")
async def api_genres():
    from scripts.categories import get_all_genres
    from dataclasses import asdict
    return JSONResponse({g.id: asdict(g) for g in get_all_genres()})


@app.get("/api/genres/{genre_id}/premise")
async def api_random_premise(genre_id: str, fill: bool = True):
    from scripts.categories import get_random_premise, get_genre
    if not get_genre(genre_id):
        raise HTTPException(404, f"Genre '{genre_id}' not found")
    return JSONResponse({"genre_id": genre_id, "premise": get_random_premise(genre_id, fill)})


@app.get("/health")
async def health():
    from scripts.generate_book import NovelClawClient
    nc = NovelClawClient()
    return {"bookforge": "ok", "novelclaw": nc.health(), "version": "2.0.1",
            "cerebras_model": CEREBRAS_MODEL}
