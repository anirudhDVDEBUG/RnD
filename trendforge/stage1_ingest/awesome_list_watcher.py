"""Watch awesome-list READMEs for newly-added entries."""
from __future__ import annotations

import logging
import re
from typing import Iterable

import httpx

from trendforge import store

log = logging.getLogger(__name__)


def fetch_readme(repo: str) -> str | None:
    """Fetch the default-branch README from a GitHub repo."""
    for branch in ("main", "master"):
        url = f"https://raw.githubusercontent.com/{repo}/{branch}/README.md"
        try:
            r = httpx.get(url, timeout=20, follow_redirects=True)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            log.debug("README fetch %s/%s: %s", repo, branch, e)
    return None


# Capture every URL that appears inside a markdown link `[text](url)` —
# we treat the union of these as the "current" set of curated links.
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def parse_links(readme_text: str) -> list[tuple[str, str]]:
    return [(m.group(1), m.group(2)) for m in LINK_RE.finditer(readme_text)]


def ingest_awesome_lists(repos: Iterable[str], db_path=None) -> int:
    """Insert any new (title, url) pair found in the README of each repo.

    Idempotency comes from items.url uniqueness: links already seen on a
    prior run are dropped silently.
    """
    db = db_path or store.DB_PATH
    n = 0
    with store.get_conn(db) as conn:
        for repo in repos:
            text = fetch_readme(repo)
            if not text:
                continue
            for title, url in parse_links(text):
                # skip relative anchors / GitHub badges
                if not url.startswith("http"):
                    continue
                if "img.shields.io" in url or "badge" in url.lower():
                    continue
                row_id = store.insert_item(
                    conn,
                    url=url,
                    source="awesome_list",
                    title=title.strip(),
                    raw_metadata={"list_repo": repo},
                )
                if row_id is not None:
                    n += 1
    log.info("Awesome-list: inserted %d new items", n)
    return n
