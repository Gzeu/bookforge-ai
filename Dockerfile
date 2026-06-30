# BookForge AI — Production Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps for Playwright Chromium (Debian Bookworm compatible)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget gnupg ca-certificates \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 \
    libgbm1 libasound2t64 libpangocairo-1.0-0 libpango-1.0-0 libcairo2 \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir -e . && playwright install chromium --with-deps

COPY . .

# Runtime dirs
RUN mkdir -p /data/manuscripts /data/epub_output /data/covers /app/schedules

EXPOSE 8020

CMD ["uvicorn", "web.app:app", "--host", "0.0.0.0", "--port", "8020"]
