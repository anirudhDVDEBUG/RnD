"""Predict 15 likely audience questions and prepare answers."""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from pathlib import Path

log = logging.getLogger(__name__)


def _fallback_qa(topic: str, audience: str | None) -> str:
    return (
        f"# Q&A prep — {topic}\n\n"
        f"Audience: {audience or '(unspecified)'}\n\n"
        "Claude CLI was unavailable, so this is a generic checklist.\n\n"
        "1. What's the simplest thing that works today?\n"
        "2. What are the top three failure modes?\n"
        "3. How does this compare to (most-cited alternative)?\n"
        "4. Cost / latency tradeoffs?\n"
        "5. What's the smallest demo that proves the concept?\n"
        "6. What changes in the next 6 months?\n"
        "7. What's the hardest production lesson learned so far?\n"
        "8. How does this map to your project (PitchBot / ARIA / smart_glasses)?\n"
        "9. What are the security / privacy considerations?\n"
        "10. Where does the open-source ecosystem stand?\n"
        "11. Which papers are essential reading?\n"
        "12. What's hype vs real?\n"
        "13. How do you measure success?\n"
        "14. What would you build differently if starting from scratch?\n"
        "15. Where would a beginner start tomorrow?\n"
    )


def predict(topic: str, audience: str | None, dossier_path: Path,
            output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    dossier = dossier_path.read_text(encoding="utf-8")
    qa_path = output_dir / "qa_prep.md"

    prompt = f"""You are preparing Q&A for a talk on: {topic!r}.
Audience: {audience or 'technical audience'}.

The dossier follows. Generate exactly 15 likely audience questions tuned
to this audience (e.g. JNTU students will ask different questions than
VC partners or VLSI engineers). For each question provide:
- A concise prepared answer (3-5 sentences)
- Source citations (URL or DB id) where applicable
- An "if asked X, pivot to slide Y" navigation hint when relevant

Output as Markdown. No fences.

DOSSIER:
{dossier[:14000]}
"""
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True,
            text=True,
            env=env,
            timeout=900,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("Claude unavailable for Q&A: %s", e)
        qa_path.write_text(_fallback_qa(topic, audience), encoding="utf-8")
        return qa_path
    if result.returncode != 0 or not result.stdout.strip():
        qa_path.write_text(_fallback_qa(topic, audience), encoding="utf-8")
        return qa_path
    qa_path.write_text(result.stdout.strip(), encoding="utf-8")
    return qa_path
