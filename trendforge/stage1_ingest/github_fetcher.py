"""GitHub fetcher: search API + star velocity for watched repos."""
from __future__ import annotations

import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Iterable

import httpx

from trendforge import store
from trendforge.config_loader import load_watched_repos

log = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"


def _headers() -> dict:
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def search_repositories(q: str, sort: str = "stars", per_page: int = 30) -> list[dict]:
    """Run a GitHub repo search."""
    params = {"q": q, "sort": sort, "order": "desc", "per_page": per_page}
    try:
        r = httpx.get(
            f"{GITHUB_API}/search/repositories",
            params=params,
            headers=_headers(),
            timeout=30,
        )
        r.raise_for_status()
        return r.json().get("items", [])
    except Exception as e:
        log.warning("GitHub search failed (%s): %s", q, e)
        return []


def get_repo(full_name: str) -> dict | None:
    try:
        r = httpx.get(
            f"{GITHUB_API}/repos/{full_name}", headers=_headers(), timeout=30
        )
        if r.status_code == 200:
            return r.json()
    except Exception as e:
        log.warning("GitHub get_repo failed (%s): %s", full_name, e)
    return None


def search_to_items(repos: list[dict]) -> list[dict]:
    items: list[dict] = []
    for r in repos:
        items.append(
            {
                "url": r.get("html_url"),
                "source": "github",
                "title": f"{r.get('full_name')}: {r.get('description') or ''}".strip(),
                "author": (r.get("owner") or {}).get("login"),
                "published_at": r.get("created_at"),
                "raw_metadata": {
                    "stars": r.get("stargazers_count"),
                    "forks": r.get("forks_count"),
                    "language": r.get("language"),
                    "topics": r.get("topics", []),
                    "pushed_at": r.get("pushed_at"),
                    "full_name": r.get("full_name"),
                },
            }
        )
    return items


def ingest_searches(searches: Iterable[dict], db_path=None) -> int:
    """For each search dict {q, sort, days?}, fetch and insert results."""
    db = db_path or store.DB_PATH
    n = 0
    with store.get_conn(db) as conn:
        for s in searches:
            q = s.get("q", "")
            sort = s.get("sort", "stars")
            days = int(s.get("days", 7))
            since = (datetime.now(timezone.utc) - timedelta(days=days)).date().isoformat()
            full_q = q.replace("{since}", since)
            if "created:" not in full_q:
                full_q = f"{full_q} created:>{since}"
            results = search_repositories(full_q, sort=sort)
            for it in search_to_items(results):
                if not it["url"]:
                    continue
                row_id = store.insert_item(conn, **it)
                if row_id is not None:
                    n += 1
    log.info("GitHub search: inserted %d new items", n)
    return n


def snapshot_watched_repos(db_path=None, threshold: int = 50) -> int:
    """Snapshot star counts for watchlist; insert items for repos that
    crossed the velocity threshold today."""
    db = db_path or store.DB_PATH
    repos = load_watched_repos()
    n_alerts = 0
    with store.get_conn(db) as conn:
        for repo in repos:
            data = get_repo(repo)
            if not data:
                continue
            stars = data.get("stargazers_count", 0)
            store.snapshot_stars(conn, repo, stars)
            velocity = store.star_velocity(conn, repo)
            if velocity is not None and velocity >= threshold:
                row_id = store.insert_item(
                    conn,
                    url=data.get("html_url"),
                    source="github",
                    title=f"⭐ velocity: {repo} +{velocity}/day — {data.get('description') or ''}",
                    author=(data.get("owner") or {}).get("login"),
                    published_at=data.get("pushed_at"),
                    raw_metadata={
                        "stars": stars,
                        "stars_delta_today": velocity,
                        "language": data.get("language"),
                        "topics": data.get("topics", []),
                        "full_name": repo,
                        "velocity_alert": True,
                    },
                )
                if row_id is not None:
                    n_alerts += 1
    log.info("GitHub velocity: %d alerts", n_alerts)
    return n_alerts
