"""Run the /watch skill against a YouTube/Loom URL via the claude CLI.

If /watch isn't installed, fall back to fetching the YouTube video page
title + description so the rest of the pipeline still has *something* to
work with.
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from pathlib import Path

import httpx

from trendforge import store

log = logging.getLogger(__name__)


def is_video_url(url: str) -> bool:
    if not url:
        return False
    url_l = url.lower()
    return any(
        d in url_l
        for d in ("youtube.com/watch", "youtu.be/", "loom.com/share/", "vimeo.com/")
    )


def _fallback_youtube(url: str) -> dict | None:
    """Crude fallback: scrape page title + meta description."""
    try:
        r = httpx.get(url, timeout=15, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None
        html = r.text
        title_m = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
        desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
        return {
            "summary": (title_m.group(1).strip() if title_m else "") + " — " + (desc_m.group(1)[:500] if desc_m else ""),
            "key_technical_insights": [],
            "code_shown_on_screen": "",
            "architecture_diagrams": "",
            "skill_candidate": "no",
            "skill_name_suggestion": None,
            "_fallback": True,
        }
    except Exception as e:
        log.warning("Fallback fetch failed for %s: %s", url, e)
        return None


def watch_video(item: dict, timeout: int = 600) -> dict | None:
    """Invoke `claude -p '/watch <url>'` and parse the JSON response.

    Returns the parsed dict, or a fallback dict, or None if everything fails.
    """
    url = item["url"]
    prompt = f"""/watch {url}

Then return ONLY a JSON object with these keys (no fences, no prose):

{{
  "key_technical_insights": ["...", "..."],
  "code_shown_on_screen": "all code/commands/configs visible on screen, verbatim",
  "architecture_diagrams": "description of any diagrams shown",
  "summary": ["bullet 1", "bullet 2", "bullet 3", "bullet 4", "bullet 5"],
  "skill_candidate": "yes|no",
  "skill_name_suggestion": "snake_case name or null",
  "transcript_excerpt": "first 500 chars of transcript"
}}
"""
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)  # CRITICAL: force Max plan

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True,
            text=True,
            env=env,
            timeout=timeout,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("Claude /watch unavailable: %s", e)
        return _fallback_youtube(url)

    if result.returncode != 0:
        log.warning("Claude /watch exit %d: %s", result.returncode, result.stderr[:200])
        return _fallback_youtube(url)

    text = result.stdout.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
    log.warning("Couldn't parse /watch JSON for %s", url)
    return _fallback_youtube(url)


def watch_selected(db_path=None) -> int:
    """Watch every status='selected' item that has a video URL."""
    db = db_path or store.DB_PATH
    n = 0
    with store.get_conn(db) as conn:
        rows = store.get_items_by_status(conn, "selected")
        for raw in rows:
            row = store.row_to_dict(raw)
            assert row is not None
            if not is_video_url(row["url"]):
                # Mark as watched anyway so later stages know not to wait
                store.update_status(conn, row["id"], "watched")
                continue
            log.info("Watching %s", row["url"])
            data = watch_video(row)
            if data:
                summary = data.get("summary")
                if isinstance(summary, list):
                    summary_str = "\n".join(f"- {b}" for b in summary)
                else:
                    summary_str = str(summary or "")
                store.save_transcript(
                    conn,
                    row["id"],
                    transcript_text=data.get("transcript_excerpt", ""),
                    frames_dir=None,
                    watch_summary=json.dumps(data, ensure_ascii=False),
                )
                n += 1
            store.update_status(conn, row["id"], "watched")
    log.info("Watched %d videos", n)
    return n
