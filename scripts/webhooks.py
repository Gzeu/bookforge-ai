#!/usr/bin/env python3
"""BookForge AI — Webhook notifications for batch and job events."""
import logging
import requests

logger = logging.getLogger(__name__)


def send_discord_webhook(webhook_url: str, content: str) -> int:
    """Send a Discord webhook message. Returns HTTP status code, or 0 on failure."""
    try:
        r = requests.post(webhook_url, json={"content": content}, timeout=15)
        r.raise_for_status()
        return r.status_code
    except Exception as e:
        logger.warning(f"Discord webhook failed (non-fatal): {e}")
        return 0


def send_json_webhook(webhook_url: str, payload: dict) -> int:
    """Send a generic JSON POST webhook. Returns HTTP status code, or 0 on failure."""
    try:
        r = requests.post(webhook_url, json=payload, timeout=15)
        r.raise_for_status()
        return r.status_code
    except Exception as e:
        logger.warning(f"JSON webhook failed (non-fatal): {e}")
        return 0
