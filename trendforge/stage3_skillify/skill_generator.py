"""Skill generator — turns a watched item into output/skills/<name>/SKILL.md.

We try the claude CLI first for the highest-quality output. If it's not
available (or returns junk), we fall back to a deterministic SKILL.md
template using the item's title + tags so the pipeline keeps moving.
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from pathlib import Path

from trendforge import store

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]
SKILLS_DIR = ROOT / "output" / "skills"


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.strip().lower()).strip("_")
    return s[:60] or "unnamed_skill"


def _template_skill(item: dict, watch_data: dict | None) -> tuple[str, str]:
    """Deterministic fallback SKILL.md."""
    title = item.get("title") or "Untitled"
    name = slugify(title)
    tags = item.get("tags") or []
    if isinstance(tags, str):
        try:
            tags = json.loads(tags)
        except json.JSONDecodeError:
            tags = []
    triggers = ", ".join(f'"{t}"' for t in tags[:5]) or '"placeholder"'
    summary_lines = []
    if watch_data:
        summary = watch_data.get("summary")
        if isinstance(summary, list):
            summary_lines = summary
        elif summary:
            summary_lines = [str(summary)]
    summary_md = "\n".join(f"- {b}" for b in summary_lines) or "- (no summary available)"
    md = f"""---
name: {name}
description: Auto-generated skill from "{title}". Triggers on: {triggers}
---

# {title}

## Source
- {item.get('url')}
- Tags: {', '.join(tags) if tags else 'none'}

## When to use
{summary_md}

## How to use
This skill is a stub generated from a TrendForge item. Run the prototype in
`output/prototypes/{name}/` and refine this file by hand if you decide to
keep it.

## Notes
Generated automatically — review before relying on it.
"""
    return name, md


def claude_generate_skill(item: dict, watch_data: dict | None) -> tuple[str, str] | None:
    """Ask the claude CLI to produce a skill name + SKILL.md content."""
    payload = {
        "url": item.get("url"),
        "title": item.get("title"),
        "source": item.get("source"),
        "tags": item.get("tags") or [],
        "metadata": item.get("raw_metadata") or {},
        "watch": watch_data or {},
    }
    prompt = f"""You are generating a Claude skill (SKILL.md) from this source:

{json.dumps(payload, ensure_ascii=False)[:8000]}

Output ONLY a JSON object — no fences, no prose — with these keys:
{{
  "name": "snake_case_skill_name (60 chars max)",
  "skill_md": "FULL contents of SKILL.md including YAML frontmatter (name, description with triggers), 'When to use' section with 3-5 trigger phrases, 'How to use' section with concrete steps, and 'References' linking back to the source URL"
}}

Follow Anthropic's skill conventions: https://github.com/anthropics/skills
The skill must be self-contained and runnable.
"""
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True,
            text=True,
            env=env,
            timeout=300,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("Claude unavailable for skillify: %s", e)
        return None
    if result.returncode != 0:
        log.warning("Claude skillify non-zero exit: %s", result.stderr[:200])
        return None
    text = result.stdout.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.DOTALL)
        if not m:
            return None
        try:
            parsed = json.loads(m.group(0))
        except json.JSONDecodeError:
            return None
    name = slugify(parsed.get("name") or item.get("title") or "skill")
    skill_md = parsed.get("skill_md") or ""
    if not skill_md:
        return None
    return name, skill_md


def generate_skill_for_item(item: dict, watch_data: dict | None) -> tuple[str, Path]:
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    result = claude_generate_skill(item, watch_data)
    if result is None:
        log.info("Falling back to template skill for item %s", item["id"])
        name, md = _template_skill(item, watch_data)
    else:
        name, md = result
    skill_dir = SKILLS_DIR / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(md, encoding="utf-8")
    return name, skill_dir


def skillify_watched(db_path=None) -> list[int]:
    """For each status='watched' item, generate a skill. Returns list of new skill IDs."""
    db = db_path or store.DB_PATH
    new_skill_ids: list[int] = []
    with store.get_conn(db) as conn:
        rows = store.get_items_by_status(conn, "watched")
        for raw in rows:
            row = store.row_to_dict(raw)
            assert row is not None
            transcript = store.get_transcript(conn, row["id"])
            watch_data = None
            if transcript and transcript["watch_summary"]:
                try:
                    watch_data = json.loads(transcript["watch_summary"])
                except json.JSONDecodeError:
                    watch_data = {"summary": transcript["watch_summary"]}
            try:
                name, skill_dir = generate_skill_for_item(row, watch_data)
            except Exception as e:
                log.warning("Skillify failed for item %s: %s", row["id"], e)
                store.update_status(conn, row["id"], "skipped")
                continue
            skill_md_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            sid = store.insert_skill(
                conn,
                item_id=row["id"],
                skill_name=name,
                skill_path=str(skill_dir),
                skill_md=skill_md_text,
            )
            new_skill_ids.append(sid)
            store.update_status(conn, row["id"], "skillified")
    log.info("Skillified %d items", len(new_skill_ids))
    return new_skill_ids
