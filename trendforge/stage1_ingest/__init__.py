"""Stage 1: ingest sources into the items table."""
from __future__ import annotations

import logging
from typing import Any

from trendforge.config_loader import load_dotenv, load_sources

from .awesome_list_watcher import ingest_awesome_lists
from .github_fetcher import ingest_searches, snapshot_watched_repos
from .hn_fetcher import ingest_hn
from .rss_fetcher import ingest_rss
from .youtube_lister import ingest_youtube

log = logging.getLogger(__name__)


def run_ingest(db_path=None) -> dict[str, int]:
    """Run all stage-1 fetchers; return per-source counts of new items."""
    load_dotenv()
    cfg = load_sources()
    counts: dict[str, int] = {}

    counts["rss"] = ingest_rss(cfg.get("rss", []), db_path=db_path)

    counts["github_search"] = ingest_searches(
        cfg.get("github_search", []), db_path=db_path
    )

    velocity_cfg = cfg.get("github_star_velocity") or {}
    counts["github_velocity"] = snapshot_watched_repos(
        db_path=db_path,
        threshold=int(velocity_cfg.get("threshold_stars_per_day", 50)),
    )

    counts["awesome_list"] = ingest_awesome_lists(
        cfg.get("awesome_lists", []), db_path=db_path
    )

    hn_cfg = cfg.get("hackernews") or {}
    counts["hn"] = ingest_hn(
        query=hn_cfg.get("query", "claude"),
        hours=int(hn_cfg.get("hours", 24)),
        min_points=int(hn_cfg.get("min_points", 30)),
        db_path=db_path,
    )

    yt_cfg = cfg.get("youtube") or {}
    counts["youtube"] = ingest_youtube(
        channel_ids=yt_cfg.get("channels", []),
        hours=24,
        max_videos=int(yt_cfg.get("max_videos_per_channel_per_day", 3)),
        db_path=db_path,
    )

    log.info("Ingest totals: %s", counts)
    return counts


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    print(run_ingest())
