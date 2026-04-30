"""Synthesize a research dossier from a corpus."""
from __future__ import annotations

import json
import logging
import os
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)


def _fallback_dossier(topic: str, corpus: dict) -> str:
    db = corpus.get("db", [])
    gh = corpus.get("github", [])
    out = [
        f"# {topic} — Research Dossier (FALLBACK)",
        "",
        "Claude CLI was not available, so this is a deterministic dump of",
        "the corpus. Re-run with `claude` in PATH for the real synthesis.",
        "",
        "## Local DB (top hits by similarity)",
    ]
    for it in db[:30]:
        out.append(f"- [{it.get('title','')[:120]}]({it.get('url','')}) "
                   f"— sim {it.get('_similarity', 0):.2f} · facet `{it.get('_facet','')}`")
    out += ["", "## Live GitHub"]
    for it in gh[:30]:
        md = it.get("raw_metadata") or {}
        out.append(f"- [{it.get('title','')[:120]}]({it.get('url','')}) — {md.get('stars',0)} stars")
    return "\n".join(out)


def synthesize(topic: str, audience: str | None, duration: int | None,
               corpus: dict, output_dir: Path) -> Path:
    """Write dossier.md to output_dir. Returns the path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    dossier_path = output_dir / "dossier.md"

    payload_db = [
        {"id": it.get("id"), "title": it.get("title"), "url": it.get("url"),
         "tags": it.get("tags") or [], "facet": it.get("_facet"),
         "similarity": it.get("_similarity"), "score": it.get("score")}
        for it in corpus.get("db", [])[:60]
    ]
    payload_gh = [
        {"title": it.get("title"), "url": it.get("url"),
         "stars": (it.get("raw_metadata") or {}).get("stars", 0),
         "topics": (it.get("raw_metadata") or {}).get("topics", []),
         "facet": it.get("_facet")}
        for it in corpus.get("github", [])[:40]
    ]

    prompt = f"""You are writing a research dossier on the topic: {topic!r}.
Audience: {audience or 'technical decision-makers'}.
Target talk length: {duration or 30} minutes.

Below are two corpora to synthesize from. Cite items inline by URL.

LOCAL DB HITS (already curated by the user's interests over weeks of cron runs):
{json.dumps(payload_db, ensure_ascii=False)[:18000]}

LIVE GITHUB:
{json.dumps(payload_gh, ensure_ascii=False)[:8000]}

Use your WebSearch tool to fill any gaps and cite 3-5 fresh authoritative sources.

Produce a Markdown dossier with these sections, in order:
1. Executive summary (~1 page)
2. Landscape map — taxonomy of approaches in this space
3. Deep-dives — 2-3 paragraphs per major cluster, with inline citations
4. Connections to Anirudh's projects (PitchBot / ARIA / smart_glasses) — pick the best fit
5. Recommended demo concept — 1 specific buildable thing for the talk
6. Open questions worth raising in Q&A

Write the full dossier inline as your final response. No fences.
"""
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True,
            text=True,
            env=env,
            timeout=1800,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("Claude unavailable for synthesis: %s", e)
        dossier_path.write_text(_fallback_dossier(topic, corpus), encoding="utf-8")
        return dossier_path

    if result.returncode != 0 or not result.stdout.strip():
        dossier_path.write_text(_fallback_dossier(topic, corpus), encoding="utf-8")
        return dossier_path

    dossier_path.write_text(result.stdout.strip(), encoding="utf-8")
    return dossier_path
