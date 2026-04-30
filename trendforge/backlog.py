"""Business backlog — pinned items with their why/how-to-monetize pitch.

Two outputs:
  - output/backlog.md (tracked in git, browseable on GitHub)
  - one persistent GitHub issue labelled `backlog` (auto-updated on each run)
"""
from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path

from trendforge import store

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
BACKLOG_MD = ROOT / "output" / "backlog.md"


def render_markdown(db_path=None) -> str:
    db = db_path or store.DB_PATH
    with store.get_conn(db) as conn:
        rows = conn.execute(
            """
            SELECT id, url, title, source, notes, business_pitch,
                   raw_metadata, score, status, fetched_at
            FROM items WHERE pinned = 1
            ORDER BY id
            """
        ).fetchall()
    if not rows:
        return "# TrendForge Business Backlog\n\n_(empty)_\n"

    lines = [
        "# TrendForge Business Backlog",
        "",
        "Hand-curated items worth building. Each entry maps a TrendForge",
        "ingest item to a concrete business Anirudh / Adroitec could sell.",
        "",
        "Update via `python3 scripts/seed_backlog.py` or by setting",
        "`pinned = 1` and filling `notes` + `business_pitch` on the items row.",
        "",
        f"_Last regenerated from {len(rows)} pinned items._",
        "",
        "---",
        "",
    ]
    for i, r in enumerate(rows, 1):
        lines.append(f"## {i}. {r['title'] or '(untitled)'}")
        lines.append("")
        lines.append(f"- **Source:** {r['url']}")
        if r['source']:
            lines.append(f"- **Channel:** `{r['source']}`")
        if r['notes']:
            lines.append(f"- **What it is:** {r['notes']}")
        lines.append("")
        if r['business_pitch']:
            lines.append("**Pitch:**")
            lines.append("")
            for ln in str(r['business_pitch']).splitlines():
                lines.append(f"> {ln}")
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


def write_markdown(db_path=None) -> Path:
    BACKLOG_MD.parent.mkdir(parents=True, exist_ok=True)
    BACKLOG_MD.write_text(render_markdown(db_path), encoding="utf-8")
    return BACKLOG_MD


def upsert_github_issue(repo: str | None = None,
                        title: str = "Business Backlog — Claude+Marketing picks",
                        label: str = "backlog") -> str | None:
    """Create or update the persistent backlog issue.

    Looks for an open issue with the given label; if found, edits its body.
    If none, creates one. Returns the issue URL.
    """
    body_path = write_markdown()
    env = os.environ.copy()
    if not env.get("GH_TOKEN") and env.get("GITHUB_TOKEN"):
        env["GH_TOKEN"] = env["GITHUB_TOKEN"]

    repo_args = ["-R", repo] if repo else []

    # Find existing issue with our label
    try:
        listing = subprocess.run(
            ["gh", "issue", "list", "--label", label, "--state", "open",
             "--json", "number,url"] + repo_args,
            capture_output=True, text=True, env=env, timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("gh CLI failed: %s", e)
        return None

    import json as _json
    existing = _json.loads(listing.stdout) if listing.stdout.strip() else []

    if existing:
        num = existing[0]["number"]
        url = existing[0]["url"]
        subprocess.run(
            ["gh", "issue", "edit", str(num),
             "--title", title, "--body-file", str(body_path)] + repo_args,
            env=env, timeout=60, check=False,
        )
        log.info("Updated backlog issue #%s", num)
        return url

    # Ensure label exists
    subprocess.run(
        ["gh", "label", "create", label, "--color", "1F8B4C",
         "--description", "Hand-curated business backlog (auto-managed)"]
        + repo_args,
        capture_output=True, env=env, timeout=30, check=False,
    )
    res = subprocess.run(
        ["gh", "issue", "create", "--title", title,
         "--body-file", str(body_path), "--label", label] + repo_args,
        capture_output=True, text=True, env=env, timeout=60,
    )
    if res.returncode != 0:
        log.warning("gh issue create failed: %s", res.stderr[:200])
        return None
    return res.stdout.strip().splitlines()[-1]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    p = write_markdown()
    print(f"Wrote {p}")
    url = upsert_github_issue()
    print(f"Issue: {url}")
