"""Open a GitHub Issue for the daily digest via `gh` CLI."""
from __future__ import annotations

import logging
import os
import subprocess
from datetime import date
from pathlib import Path

from trendforge import store

log = logging.getLogger(__name__)


def open_issue(brief_path: Path, digest_date: str | None = None, db_path=None) -> str | None:
    """Create the issue. Returns the URL, or None on failure."""
    today = digest_date or date.today().isoformat()
    title = f"TrendForge Daily — {today}"
    env = os.environ.copy()
    # gh CLI uses GH_TOKEN — mirror from GITHUB_TOKEN so cron works
    # without an interactive `gh auth login`.
    if not env.get("GH_TOKEN") and env.get("GITHUB_TOKEN"):
        env["GH_TOKEN"] = env["GITHUB_TOKEN"]
    try:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "create",
                "--title",
                title,
                "--body-file",
                str(brief_path),
                "--label",
                "daily-digest",
            ],
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("gh CLI unavailable for issue creation: %s", e)
        return None

    if result.returncode != 0:
        log.warning("gh issue create failed: %s", result.stderr[:300])
        return None

    url = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else None

    if url and db_path is not None or url:
        db = db_path or store.DB_PATH
        with store.get_conn(db) as conn:
            conn.execute(
                "UPDATE digests SET github_issue_url = ? WHERE digest_date = ?",
                (url, today),
            )
            conn.commit()
    return url
