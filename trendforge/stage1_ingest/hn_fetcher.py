"""Hacker News ingest via Algolia (no auth needed)."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

import httpx

from trendforge import store

log = logging.getLogger(__name__)

HN_API = "https://hn.algolia.com/api/v1/search"


def fetch_hn(query: str, hours: int = 24, min_points: int = 30) -> list[dict]:
    cutoff = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp())
    params = {
        "query": query,
        "tags": "(story,show_hn)",
        "numericFilters": f"created_at_i>{cutoff},points>={min_points}",
        "hitsPerPage": 100,
    }
    try:
        r = httpx.get(HN_API, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        log.warning("HN fetch failed: %s", e)
        return []
    out: list[dict] = []
    for hit in data.get("hits", []):
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}"
        out.append(
            {
                "url": url,
                "source": "hn",
                "title": hit.get("title") or hit.get("story_title") or "(untitled)",
                "author": hit.get("author"),
                "published_at": hit.get("created_at"),
                "raw_metadata": {
                    "points": hit.get("points"),
                    "num_comments": hit.get("num_comments"),
                    "hn_id": hit["objectID"],
                    "hn_url": f"https://news.ycombinator.com/item?id={hit['objectID']}",
                },
            }
        )
    return out


def ingest_hn(query: str, hours: int = 24, min_points: int = 30, db_path=None) -> int:
    db = db_path or store.DB_PATH
    items = fetch_hn(query, hours=hours, min_points=min_points)
    n = 0
    with store.get_conn(db) as conn:
        for it in items:
            row_id = store.insert_item(conn, **it)
            if row_id is not None:
                n += 1
    log.info("HN: inserted %d new items", n)
    return n
