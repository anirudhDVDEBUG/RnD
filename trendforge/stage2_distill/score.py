"""Score new items by source signal + interest match + recency."""
from __future__ import annotations

import json
import logging
import math
import re
from datetime import datetime, timezone
from typing import Any

import dateutil.parser

from trendforge import store
from trendforge.config_loader import load_interests

log = logging.getLogger(__name__)


WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]+")


def _tokens(text: str) -> set[str]:
    return {m.group(0).lower() for m in WORD_RE.finditer(text or "")}


def source_signal(row: dict) -> float:
    """0-1 score from raw_metadata signals."""
    md = row.get("raw_metadata") or {}
    src = row["source"]
    if src == "github":
        stars = md.get("stars", 0) or 0
        # log10(stars+1) with cap of 5
        return min(1.0, math.log10(stars + 1) / 5.0)
    if src == "hn":
        pts = md.get("points", 0) or 0
        return min(1.0, math.log10(pts + 1) / 3.0)
    if src == "youtube":
        return 0.5  # YT views aren't in feed; treat as medium
    if src == "rss":
        return 0.4
    if src == "awesome_list":
        return 0.3  # already curated, but no engagement signal
    return 0.3


def interest_match(row: dict, interests: dict) -> tuple[float, str]:
    """Keyword-overlap match against interests.yaml (v0; embeddings come later)."""
    blob_parts = [
        row.get("title") or "",
        json.dumps(row.get("raw_metadata") or {}),
    ]
    text = " ".join(blob_parts).lower()
    text_tokens = _tokens(text)

    high = interests.get("high_signal_keywords", []) or []
    boring = interests.get("boring", []) or []
    projects = interests.get("active_projects", {}) or {}

    hits: list[str] = []
    for kw in high:
        if kw.lower() in text:
            hits.append(kw)
    for proj_name, proj_desc in projects.items():
        for tok in _tokens(f"{proj_name} {proj_desc}"):
            if tok in text_tokens and tok not in {"the", "for", "and", "ai", "is", "of"}:
                hits.append(f"project:{proj_name}")
                break

    boring_hits = [b for b in boring if b.lower() in text]
    score = min(1.0, len(hits) * 0.25) - 0.3 * len(boring_hits)
    score = max(0.0, score)
    reasoning = f"hits={hits}; boring={boring_hits}"
    return score, reasoning


def recency(row: dict) -> float:
    """Exponential decay: 1.0 at 0h, 0.5 at 24h, 0.25 at 48h."""
    pub = row.get("published_at") or row.get("fetched_at")
    if not pub:
        return 0.5
    try:
        dt = dateutil.parser.isoparse(pub)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return 0.5
    age_hours = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
    if age_hours < 0:
        age_hours = 0
    return math.pow(0.5, age_hours / 24)


def score_item(row: dict, interests: dict) -> tuple[float, str]:
    s_sig = source_signal(row)
    s_int, reasoning = interest_match(row, interests)
    s_rec = recency(row)
    score = 0.4 * s_sig + 0.4 * s_int + 0.2 * s_rec
    full_reasoning = (
        f"sig={s_sig:.2f} int={s_int:.2f} rec={s_rec:.2f} | {reasoning}"
    )
    return score, full_reasoning


def _is_boring(row: dict, interests: dict) -> bool:
    """Hard filter: any boring keyword in title/metadata kills the item."""
    boring = interests.get("boring", []) or []
    if not boring:
        return False
    text = " ".join([
        row.get("title") or "",
        json.dumps(row.get("raw_metadata") or {}),
    ]).lower()
    return any(b.lower() in text for b in boring)


def score_pending(db_path=None, top_k: int = 5) -> list[int]:
    """Score every status='new' item; return IDs of top_k non-boring 'selected'."""
    db = db_path or store.DB_PATH
    interests = load_interests()
    candidates: list[tuple[float, int, bool]] = []

    with store.get_conn(db) as conn:
        rows = store.get_items_by_status(conn, "new")
        boring_count = 0
        for raw in rows:
            row = store.row_to_dict(raw)
            assert row is not None
            score, reasoning = score_item(row, interests)
            is_boring = _is_boring(row, interests)
            if is_boring:
                boring_count += 1
                store.update_score(
                    conn,
                    row["id"],
                    score=score,
                    reasoning=reasoning + " | DROPPED:boring",
                    tags=None,
                    status="dropped",
                )
                continue
            store.update_score(
                conn,
                row["id"],
                score=score,
                reasoning=reasoning,
                tags=None,
                status="scored",
            )
            candidates.append((score, row["id"], is_boring))

        candidates.sort(reverse=True)
        top = [iid for _, iid, _ in candidates[:top_k]]
        for iid in top:
            store.update_status(conn, iid, "selected")

    log.info("Scored %d items (%d boring dropped); selected top %d",
             len(candidates) + boring_count, boring_count, len(top))
    return top
