"""Expand a topic into 5-8 search facets via Claude (or a heuristic fallback)."""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess

log = logging.getLogger(__name__)


def _heuristic_expand(topic: str) -> list[str]:
    base = topic.strip()
    return [
        base,
        f"{base} survey",
        f"{base} benchmark",
        f"{base} architecture",
        f"{base} open source",
        f"{base} comparison",
        f"{base} 2026",
    ]


def expand(topic: str) -> list[str]:
    """Return a list of search facets covering the topic."""
    prompt = (
        f'Expand the research topic "{topic}" into 5-8 specific, complementary '
        "search facets. Each facet should narrow on a different angle "
        "(e.g. survey papers, leading open-source projects, benchmarks, "
        "comparison frameworks, recent advances).\n\n"
        "Return ONLY a JSON array of strings. No prose, no fences."
    )
    env = os.environ.copy()
    env.pop("ANTHROPIC_API_KEY", None)
    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "text"],
            capture_output=True,
            text=True,
            env=env,
            timeout=180,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        log.warning("Claude unavailable for topic expansion: %s", e)
        return _heuristic_expand(topic)
    if result.returncode != 0:
        return _heuristic_expand(topic)
    text = result.stdout.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE)
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(x) for x in parsed if x]
    except json.JSONDecodeError:
        m = re.search(r"\[.*\]", text, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(0))
                if isinstance(parsed, list):
                    return [str(x) for x in parsed if x]
            except json.JSONDecodeError:
                pass
    return _heuristic_expand(topic)
