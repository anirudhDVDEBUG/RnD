"""List recent YouTube uploads via channel RSS (no API key needed)."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Iterable

import feedparser

from trendforge import store

log = logging.getLogger(__name__)


def channel_feed_url(channel_id: str) -> str:
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"


def fetch_channel(channel_id: str, hours: int = 24, max_videos: int = 3) -> list[dict]:
    feed = feedparser.parse(channel_feed_url(channel_id))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    out: list[dict] = []
    for entry in feed.entries[: max_videos * 4]:  # over-sample, then filter
        pub = entry.get("published_parsed")
        if pub:
            try:
                pub_dt = datetime(*pub[:6], tzinfo=timezone.utc)
                if pub_dt < cutoff:
                    continue
            except (ValueError, TypeError):
                pass
        link = entry.get("link")
        if not link:
            continue
        media = entry.get("media_thumbnail") or []
        out.append(
            {
                "url": link,
                "source": "youtube",
                "title": entry.get("title", "(untitled)"),
                "author": entry.get("author"),
                "published_at": entry.get("published"),
                "raw_metadata": {
                    "channel_id": channel_id,
                    "video_id": entry.get("yt_videoid"),
                    "thumbnail": media[0]["url"] if media else None,
                    "summary": entry.get("summary", "")[:1000],
                },
            }
        )
        if len(out) >= max_videos:
            break
    return out


def ingest_youtube(
    channel_ids: Iterable[str],
    hours: int = 24,
    max_videos: int = 3,
    db_path=None,
) -> int:
    db = db_path or store.DB_PATH
    n = 0
    with store.get_conn(db) as conn:
        for cid in channel_ids:
            for it in fetch_channel(cid, hours=hours, max_videos=max_videos):
                row_id = store.insert_item(conn, **it)
                if row_id is not None:
                    n += 1
    log.info("YouTube: inserted %d new items", n)
    return n
