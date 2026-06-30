#!/usr/bin/env python3
"""BookForge AI — Webhook notifications for batch and job events."""
import requests


def send_discord_webhook(webhook_url: str, content: str) -> int:
    r = requests.post(webhook_url, json={"content": content}, timeout=15)
    return r.status_code


def send_json_webhook(webhook_url: str, payload: dict) -> int:
    r = requests.post(webhook_url, json=payload, timeout=15)
    return r.status_code
