"""Render the daily brief markdown for output/briefs/YYYY-MM-DD.md."""
from __future__ import annotations

import json
import logging
from datetime import date
from pathlib import Path

from trendforge import store
from trendforge.stage2_distill.brief import one_line

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
BRIEFS_DIR = ROOT / "output" / "briefs"


def _bullets(item: dict, watch_data: dict | None) -> list[str]:
    if watch_data and watch_data.get("summary"):
        s = watch_data["summary"]
        if isinstance(s, list):
            return [str(b) for b in s][:5]
        return [str(s)[:200]]
    md = item.get("raw_metadata") or {}
    summary = md.get("summary") or md.get("description") or ""
    if summary:
        return [str(summary)[:200]]
    return [(item.get("title") or "—")[:200]]


def render_brief(db_path=None, digest_date: str | None = None) -> tuple[str, list[int]]:
    """Render the brief markdown. Returns (markdown, list_of_top_item_ids)."""
    db = db_path or store.DB_PATH
    today = digest_date or date.today().isoformat()
    with store.get_conn(db) as conn:
        recent = store.get_recent_items(conn, hours=24)
        top_rows = conn.execute(
            "SELECT * FROM skills WHERE date(generated_at) = date('now') ORDER BY id"
        ).fetchall()
        top_items: list[tuple[dict, dict, dict | None]] = []
        for sk in top_rows:
            item = store.row_to_dict(
                conn.execute("SELECT * FROM items WHERE id = ?", (sk["item_id"],)).fetchone()
            ) or {}
            proto = conn.execute(
                "SELECT * FROM prototypes WHERE skill_id = ? ORDER BY id DESC LIMIT 1",
                (sk["id"],),
            ).fetchone()
            transcript = store.get_transcript(conn, sk["item_id"])
            watch_data = None
            if transcript and transcript["watch_summary"]:
                try:
                    watch_data = json.loads(transcript["watch_summary"])
                except json.JSONDecodeError:
                    watch_data = None
            top_items.append((dict(sk), item, dict(proto) if proto else None))

        skipped = [
            store.row_to_dict(r)
            for r in conn.execute(
                "SELECT * FROM items WHERE status = 'skipped' AND date(fetched_at) = date('now') LIMIT 20"
            ).fetchall()
        ]

    by_source: dict[str, int] = {}
    for r in recent:
        by_source[r["source"]] = by_source.get(r["source"], 0) + 1

    md = [f"# TrendForge Daily — {today}", "", "## TL;DR"]
    if top_items:
        for sk, item, _proto in top_items:
            md.append(f"- {one_line(item)}")
    else:
        md.append("- No top picks today (insufficient signal).")

    md += ["", "## What dropped in the last 24h", f"- Total items ingested: {len(recent)}"]
    src_str = ", ".join(f"{k}={v}" for k, v in sorted(by_source.items()))
    md.append(f"- Sources: {src_str}")

    md += ["", "## Top picks (with prototypes built)"]
    for i, (sk, item, proto) in enumerate(top_items, 1):
        name = sk["skill_name"]
        url = item.get("url", "")
        score = item.get("score") or 0.0
        md.append(f"\n### {i}. {item.get('title') or '(untitled)'}")
        md.append(f"- **Source:** {url}")
        md.append(f"- **Score:** {score:.3f}")
        md.append(f"- **Skill:** [`{name}`](../skills/{name}/SKILL.md)")
        if proto:
            md.append(f"- **Prototype:** [`prototypes/{name}/`](../prototypes/{name}/)")
            if proto.get("deck_path"):
                deck_name = Path(proto["deck_path"]).name
                md.append(f"- **Deck:** [`decks/{deck_name}`](../decks/{deck_name})")
        md.append("- **Why it matters:**")
        md.append(f"    - {item.get('score_reasoning') or '(no reasoning)'}")

    if skipped:
        md += ["", "## Skipped (low score)"]
        for it in skipped:
            if it is None:
                continue
            md.append(f"- {it.get('title','')[:120]} — score {it.get('score') or 0:.2f}")

    text = "\n".join(md)

    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = BRIEFS_DIR / f"{today}.md"
    out_path.write_text(text, encoding="utf-8")

    # Persist
    with store.get_conn(db) as conn:
        store.insert_digest(conn, digest_date=today, brief_md=text)

    top_ids = [item["id"] for _sk, item, _p in top_items if item.get("id") is not None]
    return text, top_ids
