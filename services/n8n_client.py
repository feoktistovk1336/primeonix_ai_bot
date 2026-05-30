from __future__ import annotations

from typing import Any
import re

import aiohttp

from config import settings


DEFAULT_TIMEOUT_SECONDS = 120


def _select_webhook_url(payload: dict[str, Any] | None = None) -> str:
    """Select n8n webhook by action/platform. Keeps fallback to N8N_WEBHOOK_URL."""
    payload = payload or {}
    action = str(payload.get("action") or "").lower()
    platform = str(payload.get("platform") or "").lower()
    workflow = str(payload.get("workflow") or "").lower()
    content_type = str(payload.get("content_type") or payload.get("tool") or "").lower()

    def pick(value: str | None) -> str | None:
        value = (value or "").strip()
        return value or None

    if any(x in action + workflow for x in ("system", "ping", "health")):
        url = pick(getattr(settings, "N8N_SYSTEM_WEBHOOK_URL", None))
        if url: return url
    if any(x in action + workflow + content_type for x in ("broadcast", "mailing", "рассыл")):
        url = pick(getattr(settings, "N8N_BROADCAST_WEBHOOK_URL", None))
        if url: return url
    if any(x in action + workflow for x in ("pro", "limit", "admin_ops")):
        url = pick(getattr(settings, "N8N_PRO_WEBHOOK_URL", None))
        if url: return url
    if any(x in action + workflow + content_type for x in ("funnel", "ig_tg", "ig→tg", "dm")):
        url = pick(getattr(settings, "N8N_FUNNEL_WEBHOOK_URL", None))
        if url: return url
    if any(x in action + workflow + content_type for x in ("reels", "reel", "video")):
        url = pick(getattr(settings, "N8N_REELS_WEBHOOK_URL", None))
        if url: return url
    if any(x in action + workflow + content_type for x in ("carousel", "карус")):
        url = pick(getattr(settings, "N8N_CAROUSEL_WEBHOOK_URL", None))
        if url: return url
    if ("instagram" in action or platform == "instagram" or "ig" == platform):
        url = pick(getattr(settings, "N8N_INSTAGRAM_WEBHOOK_URL", None))
        if url: return url
    if ("telegram" in action or platform == "telegram" or "tg" == platform):
        url = pick(getattr(settings, "N8N_TELEGRAM_WEBHOOK_URL", None))
        if url: return url

    return (settings.N8N_WEBHOOK_URL or "").strip()

def n8n_config_status(payload: dict[str, Any] | None = None) -> tuple[bool, list[str], dict[str, str | None]]:
    """Return status of the n8n bridge configuration."""
    url = _select_webhook_url(payload)
    cfg = {
        "webhook_url": url or None,
        "main_webhook_url": (settings.N8N_WEBHOOK_URL or "").strip() or None,
        "telegram_webhook_url": (getattr(settings, "N8N_TELEGRAM_WEBHOOK_URL", None) or "").strip() or None,
        "instagram_webhook_url": (getattr(settings, "N8N_INSTAGRAM_WEBHOOK_URL", None) or "").strip() or None,
        "carousel_webhook_url": (getattr(settings, "N8N_CAROUSEL_WEBHOOK_URL", None) or "").strip() or None,
        "reels_webhook_url": (getattr(settings, "N8N_REELS_WEBHOOK_URL", None) or "").strip() or None,
        "funnel_webhook_url": (getattr(settings, "N8N_FUNNEL_WEBHOOK_URL", None) or "").strip() or None,
        "broadcast_webhook_url": (getattr(settings, "N8N_BROADCAST_WEBHOOK_URL", None) or "").strip() or None,
        "pro_webhook_url": (getattr(settings, "N8N_PRO_WEBHOOK_URL", None) or "").strip() or None,
        "has_secret": "yes" if settings.N8N_WEBHOOK_SECRET else "no",
    }
    missing: list[str] = []
    if not url:
        missing.append("N8N_WEBHOOK_URL")
    return len(missing) == 0, missing, cfg


def sanitize_n8n_text(text: str | None) -> str | None:
    """Remove bad generated links and force the PrimeOnix Telegram link."""
    if not text:
        return text
    prime_link = getattr(settings, "TELEGRAM_LINK", "https://t.me/primeonix26")
    # Replace all Telegram links/placeholders with the real link.
    text = re.sub(r"https?://(?:t\.me|telegram\.me)/[^\s)\]}>]+", prime_link, text, flags=re.I)
    text = re.sub(r"\[?https?://t\.me/YOUR_CHANNEL_OR_BOT\]?", prime_link, text, flags=re.I)
    text = re.sub(r"YOUR_CHANNEL_OR_BOT|YOUR_CHANNEL|YOUR_BOT|t\.me/example|example\.com", prime_link, text, flags=re.I)
    return text


def extract_n8n_text(data: Any) -> str | None:
    """Try to extract a useful text field from a flexible n8n response."""
    if data is None:
        return None
    if isinstance(data, str):
        return sanitize_n8n_text(data.strip()) or None
    if isinstance(data, list):
        for item in data:
            text = extract_n8n_text(item)
            if text:
                return text
        return None
    if not isinstance(data, dict):
        return None

    direct_keys = (
        "text",
        "result",
        "content",
        "message",
        "output",
        "response",
        "caption",
        "generated_text",
    )
    for key in direct_keys:
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            return sanitize_n8n_text(value.strip())

    # n8n often wraps node results in json/data/body fields.
    for key in ("json", "data", "body", "item", "result"):
        if key in data:
            text = extract_n8n_text(data.get(key))
            if text:
                return text

    # LangChain/OpenAI-like nested shapes.
    choices = data.get("choices")
    if isinstance(choices, list) and choices:
        text = extract_n8n_text(choices[0])
        if text:
            return text

    return None


async def call_n8n(payload: dict[str, Any], timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    """POST a task to the configured n8n webhook."""
    ok, missing, cfg = n8n_config_status(payload)
    if not ok:
        return {"ok": False, "error": "missing_config", "missing": missing, "config": cfg}

    headers = {"Content-Type": "application/json"}
    if settings.N8N_WEBHOOK_SECRET:
        headers["X-Primeonix-Secret"] = settings.N8N_WEBHOOK_SECRET

    url = cfg["webhook_url"]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=timeout) as resp:
                raw_text = await resp.text()
                try:
                    data: Any = await resp.json(content_type=None)
                except Exception:
                    data = raw_text

                if resp.status >= 400:
                    return {
                        "ok": False,
                        "error": "http_error",
                        "status": resp.status,
                        "data": data,
                        "raw": raw_text[:2000],
                    }

                return {
                    "ok": True,
                    "status": resp.status,
                    "data": data,
                    "text": extract_n8n_text(data),
                    "raw": raw_text[:2000],
                }
    except Exception as exc:
        return {"ok": False, "error": "request_failed", "message": str(exc), "config": cfg}


async def ping_n8n() -> dict[str, Any]:
    return await call_n8n(
        {
            "action": "ping",
            "source": "telegram_bot",
            "message": "PrimeOnix bot n8n connection test",
            "expected_response": "Return JSON with text/status if webhook works.",
        },
        timeout=30,
    )
