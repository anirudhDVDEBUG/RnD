"""Vault writer — emits the Obsidian-compatible topic-folder layout.

Layout (relative to repo root):
    topics/
      <topic-slug>/
        _index.md                       # topic landing page (auto)
        _daily/
          <YYYY-MM-DD>.md               # that day's items in this topic
        items/
          <YYYY-MM-DD>_<slug>.md        # one note per item, with frontmatter
                                        # + wikilinks to skill+prototype
    prototypes/<slug>/                  # full code (only for quality items)

Notes use [[wikilinks]] which work in BOTH Obsidian and GitHub. Frontmatter
is YAML for compatibility with Obsidian's metadata + Dataview.
"""
from __future__ import annotations

import json
import logging
import re
from datetime import date
from pathlib import Path
from typing import Any

from trendforge import store
from trendforge.config_loader import load_interests
from trendforge.topics import classify, topic_label, all_topic_slugs, selection_config

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[1]
TOPICS_DIR = ROOT / "topics"
PROTO_DIR = ROOT / "output" / "prototypes"
SKILLS_DIR = ROOT / "output" / "skills"


def _slug(s: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", (s or "").strip().lower()).strip("-")
    return (s[:maxlen] or "item").rstrip("-")


def _short_title(title: str, maxlen: int = 100) -> str:
    """Trim title for headers / frontmatter (some sources prepend the full README)."""
    t = (title or "").strip()
    # Strip the velocity prefix that github_fetcher tacks on
    t = re.sub(r"^⭐\s*velocity:\s*", "", t)
    # If there's an em-dash separator, keep just the lead
    if " — " in t:
        t = t.split(" — ", 1)[0]
    if len(t) > maxlen:
        t = t[: maxlen - 1].rstrip() + "…"
    return t


def _skill_lookup(db_path) -> dict[int, dict]:
    """Map item_id -> {skill_name, has_prototype} for today's skills."""
    out: dict[int, dict] = {}
    with store.get_conn(db_path) as conn:
        for r in conn.execute(
            """SELECT s.item_id, s.skill_name,
                      EXISTS(SELECT 1 FROM prototypes p WHERE p.skill_id = s.id) AS has_proto
               FROM skills s"""
        ).fetchall():
            out[r["item_id"]] = {
                "skill_name": r["skill_name"],
                "has_prototype": bool(r["has_proto"]),
            }
    return out


def _frontmatter(d: dict[str, Any]) -> str:
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for it in v:
                lines.append(f"  - {it}")
        elif isinstance(v, str) and ("\n" in v or '"' in v):
            esc = v.replace('"', '\\"').replace("\n", " ")
            lines.append(f'{k}: "{esc}"')
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines)


def _item_note(item: dict, topic: str, today: str,
               skill_info: dict | None) -> tuple[str, str]:
    """Return (filename, markdown) for a single-item note."""
    raw_title = (item.get("title") or "(untitled)").strip()
    short = _short_title(raw_title, maxlen=100)
    file_slug = _slug(short, maxlen=50)
    fname = f"{today}_{file_slug}.md"

    fm = {
        "title": short.replace('"', "'"),
        "date": today,
        "topic": topic,
        "source": item.get("source") or "",
        "score": round(float(item.get("score") or 0), 3),
        "url": item.get("url") or "",
        "tags": [topic, item.get("source") or "unknown"],
    }

    md_block = item.get("raw_metadata") or {}
    summary = md_block.get("summary") or md_block.get("description") or ""
    summary = (summary or "").strip()[:600]

    body = [_frontmatter(fm), "", f"# {short}", ""]
    body.append(f"**Source:** {item.get('url','')}")
    body.append(f"**Topic:** [[{topic}/_index|{topic_label(topic)}]]")
    body.append(f"**Score:** {fm['score']}")
    body.append("")
    if summary:
        body += ["## Summary", "", summary, ""]
    body += ["## Why it matters", "",
             item.get("score_reasoning") or "_(no reasoning recorded)_", ""]

    if skill_info and skill_info.get("has_prototype"):
        sn = skill_info["skill_name"]
        body += [
            "## Mini-repo",
            "",
            f"- Skill: [[../../output/skills/{sn}/SKILL|SKILL.md]]",
            f"- How to use: [[../../output/prototypes/{sn}/HOW_TO_USE|HOW_TO_USE.md]]",
            f"- Tech details: [[../../output/prototypes/{sn}/TECH_DETAILS|TECH_DETAILS.md]]",
            f"- Demo: `output/prototypes/{sn}/run.sh`",
            "",
        ]
    elif skill_info:
        sn = skill_info["skill_name"]
        body += [
            "## Skill",
            "",
            f"- [[../../output/skills/{sn}/SKILL|SKILL.md]] (prototype not built — score below 0.5 threshold)",
            "",
        ]
    else:
        body += [
            "## Mini-repo",
            "",
            "_No skill or prototype generated for this item (link only)._",
            "",
        ]

    body += ["## Backlinks", "",
             f"- Topic daily: [[{topic}/_daily/{today}]]",
             f"- All in topic: [[{topic}/_index]]",
             ""]

    return fname, "\n".join(body)


def _topic_index(topic: str, item_files: list[Path]) -> str:
    """Topic landing page: lists all dates, newest first."""
    lbl = topic_label(topic)
    lines = [
        _frontmatter({"topic": topic, "label": lbl, "auto": "true"}),
        "",
        f"# {lbl}",
        "",
        f"All TrendForge items classified as `{topic}`, newest first.",
        "",
    ]

    by_date: dict[str, list[Path]] = {}
    for p in item_files:
        m = re.match(r"(\d{4}-\d{2}-\d{2})_", p.name)
        if not m:
            continue
        by_date.setdefault(m.group(1), []).append(p)

    for d in sorted(by_date.keys(), reverse=True):
        lines.append(f"## {d}")
        lines.append("")
        for p in sorted(by_date[d]):
            stem = p.stem.split("_", 1)[1] if "_" in p.stem else p.stem
            lines.append(f"- [[items/{p.stem}|{stem.replace('-', ' ')}]]")
        lines.append("")

    return "\n".join(lines)


def _daily_topic_note(topic: str, today: str, item_files: list[Path]) -> str:
    lbl = topic_label(topic)
    lines = [
        _frontmatter({"topic": topic, "date": today, "auto": "true"}),
        "",
        f"# {lbl} — {today}",
        "",
    ]
    if not item_files:
        lines.append("_No items today._")
        return "\n".join(lines)
    for p in sorted(item_files):
        stem = p.stem.split("_", 1)[1] if "_" in p.stem else p.stem
        lines.append(f"- [[../items/{p.stem}|{stem.replace('-', ' ')}]]")
    lines.append("")
    return "\n".join(lines)


def _vault_readme(today: str, counts: dict[str, int]) -> str:
    lines = [
        _frontmatter({"vault": "trendforge", "auto": "true"}),
        "",
        "# TrendForge Knowledge Vault",
        "",
        "Daily AI/LLM intelligence, organized by topic. Open this folder",
        "as an [Obsidian](https://obsidian.md) vault for full graph view +",
        "backlinks, or browse on GitHub — wikilinks render in both.",
        "",
        f"Last regenerated: **{today}**",
        "",
        "## Topics",
        "",
    ]
    for slug in all_topic_slugs():
        n = counts.get(slug, 0)
        if n == 0 and slug == "other":
            continue
        lines.append(f"- [[topics/{slug}/_index|{topic_label(slug)}]] — {n} items")
    lines += ["", "## Layout", "", "- `topics/<topic>/_index.md` — landing page",
              "- `topics/<topic>/_daily/<date>.md` — daily index",
              "- `topics/<topic>/items/<date>_<slug>.md` — one note per item",
              "- `output/prototypes/<slug>/` — full mini-repo (quality items only)",
              "- `output/skills/<slug>/SKILL.md` — Claude skill",
              "- `output/graph.html` — interactive knowledge graph (Graphify)",
              "- `output/backlog.md` — pinned business backlog",
              ""]
    return "\n".join(lines)


def write_vault(db_path=None, digest_date: str | None = None) -> dict[str, Any]:
    """Build the topic-folder vault from DB. Returns summary stats."""
    db = db_path or store.DB_PATH
    today = digest_date or date.today().isoformat()
    interests = load_interests()
    cfg = selection_config(interests)
    proto_min = cfg["prototype_min_score"]

    TOPICS_DIR.mkdir(parents=True, exist_ok=True)

    with store.get_conn(db) as conn:
        # Today's selected items (all topics)
        rows = conn.execute(
            """
            SELECT * FROM items
            WHERE status IN ('selected','watched','skillified','dropped')
              AND date(fetched_at) = date(?)
            """,
            (today,),
        ).fetchall()
        selected = [
            store.row_to_dict(r)
            for r in rows
            if r["status"] in ("selected", "watched", "skillified")
        ]

    skill_lookup = _skill_lookup(db)
    by_topic: dict[str, list[Path]] = {}
    written = 0

    for item in selected:
        if item is None:
            continue
        topic = classify(item, interests)
        topic_dir = TOPICS_DIR / topic
        items_dir = topic_dir / "items"
        items_dir.mkdir(parents=True, exist_ok=True)

        skill_info = skill_lookup.get(item.get("id"))
        # Quality gate: prototype only if score >= proto_min AND a prototype exists
        if skill_info and float(item.get("score") or 0) < proto_min:
            skill_info = {**skill_info, "has_prototype": False}

        fname, md = _item_note(item, topic, today, skill_info=skill_info)
        out_path = items_dir / fname
        out_path.write_text(md, encoding="utf-8")
        by_topic.setdefault(topic, []).append(out_path)
        written += 1

    # Daily + index per topic
    counts: dict[str, int] = {}
    for slug in all_topic_slugs(interests):
        topic_dir = TOPICS_DIR / slug
        items_dir = topic_dir / "items"
        daily_dir = topic_dir / "_daily"
        topic_dir.mkdir(parents=True, exist_ok=True)
        daily_dir.mkdir(parents=True, exist_ok=True)

        today_files = by_topic.get(slug, [])
        all_files = list(items_dir.glob("*.md")) if items_dir.exists() else []
        counts[slug] = len(all_files)

        (daily_dir / f"{today}.md").write_text(
            _daily_topic_note(slug, today, today_files), encoding="utf-8"
        )
        (topic_dir / "_index.md").write_text(
            _topic_index(slug, all_files), encoding="utf-8"
        )

    (ROOT / "VAULT_README.md").write_text(_vault_readme(today, counts), encoding="utf-8")

    log.info("Vault: wrote %d item notes across %d topics", written, len(by_topic))
    return {
        "written_items": written,
        "topics": {k: len(v) for k, v in by_topic.items()},
        "totals_by_topic": counts,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    s = write_vault()
    print(json.dumps(s, indent=2))
