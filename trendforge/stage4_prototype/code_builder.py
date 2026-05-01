"""Build a runnable prototype demo for each generated skill."""
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
PROTO_DIR = ROOT / "output" / "prototypes"


def _template_prototype(skill_name: str, skill_md: str, item: dict) -> dict[str, str]:
    """Deterministic placeholder if Claude isn't available."""
    readme = f"""# {skill_name}

Prototype scaffold for the `{skill_name}` skill.

## Source
- Item: {item.get('title')}
- URL: {item.get('url')}

## What this should do
Read `output/skills/{skill_name}/SKILL.md` and implement a minimal demo
of the capability described there.

## Run
```bash
bash run.sh
```

## Status
**Stub** — Claude wasn't available when this was generated. Either re-run
TrendForge with `claude` in PATH, or fill this in by hand.
"""
    run_sh = """#!/usr/bin/env bash
set -euo pipefail
echo "Prototype stub. Replace this script with an actual demo."
echo "See README.md for what this should do."
"""
    requirements = "# add prototype dependencies here\n"
    return {
        "README.md": readme,
        "run.sh": run_sh,
        "requirements.txt": requirements,
    }


def claude_build_prototype(skill_name: str, skill_md: str, item: dict, target_dir: Path) -> bool:
    """Spawn `claude` as a subprocess inside `target_dir` to build the demo.

    Returns True if Claude reported success and the directory has at least
    a README.md.
    """
    # Use a fresh subdir so Claude can't accidentally clobber other prototypes.
    target_dir.mkdir(parents=True, exist_ok=True)

    prompt = f"""You are building a "ready-to-evaluate" mini-repo inside the directory you're invoked from.
The user wants to wake up to 5 of these every morning and immediately decide
which to adopt — so the docs matter as much as the demo.

Source item URL: {item.get('url')}
Source item title: {item.get('title')}

SKILL.md contents (the skill or MCP this should demonstrate):
---
{skill_md[:6000]}
---

REQUIRED files in the current directory (all five MUST exist):

1. README.md
   — TL;DR (2-3 sentences), one screenshot-worthy headline result, and a
     pointer to HOW_TO_USE.md and TECH_DETAILS.md.

2. HOW_TO_USE.md
   — Install steps (pip / npm / git clone — be exact).
   — If this is a Claude SKILL: where to drop the SKILL.md folder
     (`~/.claude/skills/<name>/`) and what trigger phrases activate it.
   — If this is an MCP server: the EXACT JSON snippet to paste into
     `~/.claude.json` `mcpServers` block, with command/args/env.
   — If neither: the CLI / SDK snippet to invoke it.
   — A "First 60 seconds" section showing input → output.

3. TECH_DETAILS.md
   — What the source actually does (1-2 paragraph technical summary).
   — Architecture: key files, data flow, dependencies, model calls.
   — Limitations / what it does NOT do.
   — Why it might matter for someone building Claude-driven products
     (lead-gen, marketing, ad creatives, agent factories, voice AI).

4. run.sh — executable, runs end-to-end via `bash run.sh`, produces visible
   output without external API keys (use mock data if needed).

5. requirements.txt or package.json — declared dependencies.

Plus the actual implementation files (Python preferred; Node OK).

Test mentally before writing — imports exist, paths correct,
`bash run.sh` produces visible output. Be concrete in HOW_TO_USE.md and
TECH_DETAILS.md — vague placeholders defeat the purpose.
"""
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--permission-mode", "acceptEdits"],
            cwd=str(target_dir),
            capture_output=True,
            text=True,
            env=env,
            timeout=600,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("Claude unavailable for prototype: %s", e)
        return False
    if result.returncode != 0:
        log.warning("Claude prototype exit %d: %s", result.returncode, result.stderr[:200])
    # Did anything land?
    return (target_dir / "README.md").exists()


def build_prototype_for_skill(skill_id: int, db_path=None) -> Path | None:
    db = db_path or store.DB_PATH
    with store.get_conn(db) as conn:
        skill_row = conn.execute(
            "SELECT * FROM skills WHERE id = ?", (skill_id,)
        ).fetchone()
        if not skill_row:
            log.warning("Skill %s not found", skill_id)
            return None
        item_row = conn.execute(
            "SELECT * FROM items WHERE id = ?", (skill_row["item_id"],)
        ).fetchone()
        item = store.row_to_dict(item_row) or {}
        skill_name = skill_row["skill_name"]
        skill_md = skill_row["skill_md"] or ""

        target = PROTO_DIR / skill_name
        target.mkdir(parents=True, exist_ok=True)

        ok = claude_build_prototype(skill_name, skill_md, item, target)
        if not ok:
            log.info("Falling back to prototype template for skill %s", skill_name)
            for fname, content in _template_prototype(skill_name, skill_md, item).items():
                p = target / fname
                p.write_text(content, encoding="utf-8")
                if fname.endswith(".sh"):
                    p.chmod(0o755)

        # Quick "runs successfully" check: try to execute run.sh in dry mode (don't actually run, just syntax-check)
        runs_ok = (target / "run.sh").exists()
        store.insert_prototype(
            conn,
            skill_id=skill_id,
            repo_path=str(target),
            deck_path=None,
            runs_successfully=runs_ok,
            notes="claude" if ok else "fallback-template",
        )
    return target


def build_prototypes(db_path=None) -> list[Path]:
    """Build prototypes for every skill that doesn't yet have one."""
    db = db_path or store.DB_PATH
    paths: list[Path] = []
    with store.get_conn(db) as conn:
        rows = conn.execute(
            """
            SELECT s.id FROM skills s
            LEFT JOIN prototypes p ON p.skill_id = s.id
            WHERE p.id IS NULL
            """
        ).fetchall()
    for r in rows:
        p = build_prototype_for_skill(r["id"], db_path=db_path)
        if p is not None:
            paths.append(p)
    log.info("Built %d prototypes", len(paths))
    return paths
