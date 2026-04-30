"""Topical tagger — extract 3-5 tags per item using a single Claude batch call.

Cheap during cron (one call covers ~50 items); makes Mode B retrieval much
better than keyword search alone.
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from typing import Iterable

from trendforge import store

log = logging.getLogger(__name__)

BATCH_SIZE = 50


# Heuristic fallback if Claude CLI isn't available — extract tags from
# title and topics. Lets the rest of the pipeline keep working.
HEURISTIC_TAGS = {
    "agent": "agents",
    "agents": "agents",
    "claude": "claude",
    "mcp": "mcp",
    "skill": "claude-skills",
    "skills": "claude-skills",
    "rag": "rag",
    "memory": "agent-memory",
    "embedding": "embeddings",
    "vector": "vector-store",
    "voice": "voice-ai",
    "tts": "voice-ai",
    "stt": "voice-ai",
    "vlsi": "vlsi",
    "risc-v": "risc-v",
    "video": "video",
    "rss": "rss",
    "research": "research",
    "tool-use": "tool-use",
    "function": "tool-use",
    "vision": "vision",
}


def heuristic_tags(text: str) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    low = text.lower()
    for kw, tag in HEURISTIC_TAGS.items():
        if kw in low and tag not in seen:
            out.append(tag)
            seen.add(tag)
    if not out:
        # extract topics from raw_metadata if present
        m = re.search(r'"topics":\s*\[(.*?)\]', text)
        if m:
            for t in re.findall(r'"([^"]+)"', m.group(1))[:5]:
                if t not in seen:
                    out.append(t)
                    seen.add(t)
    return out[:5]


def claude_tag_batch(items: list[dict]) -> dict[int, list[str]] | None:
    """Tag a batch of items via the claude CLI. Returns {item_id: [tags]} or None on failure."""
    if not items:
        return {}
    payload = [
        {
            "id": it["id"],
            "title": it.get("title", "")[:200],
            "source": it["source"],
            "metadata": it.get("raw_metadata") or {},
        }
        for it in items
    ]
    prompt = (
        "For each item below, return 3-5 short topical tags (lowercase, hyphenated).\n"
        "Tags should be specific concepts (e.g. 'agent-memory', 'vector-store', 'voice-ai',\n"
        "'mcp-server', 'rag', 'tool-use') — NOT vague terms ('ai', 'ml', 'tech').\n\n"
        "Return ONLY a JSON object mapping id -> array of tag strings. No prose, no fences.\n\n"
        f"Items:\n{json.dumps(payload, ensure_ascii=False)}"
    )
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)  # force Max-plan auth
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True,
            text=True,
            env=env,
            timeout=300,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("Claude CLI unavailable for tagging: %s", e)
        return None
    if result.returncode != 0:
        log.warning("Claude tagger non-zero exit: %s", result.stderr[:200])
        return None
    text = result.stdout.strip()
    # Strip ```json fences if present
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # Try to find a JSON object inside the text
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return None
        try:
            parsed = json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
    out: dict[int, list[str]] = {}
    for k, v in parsed.items():
        try:
            iid = int(k)
        except (TypeError, ValueError):
            continue
        if isinstance(v, list):
            out[iid] = [str(t).lower().strip() for t in v if t][:5]
    return out


def tag_pending(db_path=None, use_claude: bool = True) -> int:
    """Tag all status='scored' or 'selected' items that don't have tags yet."""
    db = db_path or store.DB_PATH
    n = 0
    with store.get_conn(db) as conn:
        rows = conn.execute(
            "SELECT * FROM items WHERE status IN ('scored', 'selected') AND (tags IS NULL OR tags = '[]')"
        ).fetchall()
        items = [store.row_to_dict(r) for r in rows]
        items = [i for i in items if i is not None]

        # Heuristic baseline first — guarantees every item gets some tags.
        for it in items:
            text = f"{it.get('title') or ''} {json.dumps(it.get('raw_metadata') or {})}"
            it["_heuristic"] = heuristic_tags(text)

        # Claude refinement in batches.
        claude_tags: dict[int, list[str]] = {}
        if use_claude:
            for i in range(0, len(items), BATCH_SIZE):
                batch = items[i : i + BATCH_SIZE]
                got = claude_tag_batch(batch)
                if got is None:
                    log.info("Tagger falling back to heuristics for remaining items")
                    break
                claude_tags.update(got)

        for it in items:
            tags = claude_tags.get(it["id"]) or it["_heuristic"] or []
            if not tags:
                continue
            conn.execute(
                "UPDATE items SET tags = ? WHERE id = ?",
                (json.dumps(tags), it["id"]),
            )
            n += 1
        conn.commit()
    log.info("Tagged %d items", n)
    return n
