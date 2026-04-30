"""RSS / Atom feed fetcher."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Iterable

import feedparser

from trendforge import store

log = logging.getLogger(__name__)


def _parse_published(entry) -> str | None:
    for key in ("published", "updated"):
        val = entry.get(key)
        if val:
            return str(val)
    return None


def fetch_rss(urls: Iterable[str], hours: int = 24) -> list[dict]:
    """Fetch each RSS URL; return list of normalized item dicts.

    Items older than `hours` are skipped when published date is parseable.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    out: list[dict] = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            log.warning("RSS parse failed %s: %s", url, e)
            continue
        for entry in feed.entries:
            link = entry.get("link")
            if not link:
                continue
            pub_struct = entry.get("published_parsed") or entry.get("updated_parsed")
            published_iso = None
            if pub_struct:
                try:
                    published_dt = datetime(*pub_struct[:6], tzinfo=timezone.utc)
                    published_iso = published_dt.isoformat()
                    if published_dt < cutoff:
                        continue
                except (ValueError, TypeError):
                    pass
            out.append(
                {
                    "url": link,
                    "source": "rss",
                    "title": entry.get("title", "(untitled)"),
                    "author": entry.get("author"),
                    "published_at": published_iso or _parse_published(entry),
                    "raw_metadata": {
                        "feed_url": url,
                        "summary": entry.get("summary", "")[:2000],
                        "feed_title": feed.feed.get("title", ""),
                    },
                }
            )
    return out


def ingest_rss(urls: Iterable[str], hours: int = 24, db_path=None) -> int:
    items = fetch_rss(urls, hours=hours)
    n = 0
    db = db_path or store.DB_PATH
    with store.get_conn(db) as conn:
        for it in items:
            row_id = store.insert_item(conn, **it)
            if row_id is not None:
                n += 1
    log.info("RSS: inserted %d new items", n)
    return n
