"""Stage 2: distill (score + tag)."""
from __future__ import annotations

from .score import score_pending
from .tagger import tag_pending


def run_distill(db_path=None, top_k: int = 3, use_claude_tagging: bool = True):
    selected = score_pending(db_path=db_path, top_k=top_k)
    tag_pending(db_path=db_path, use_claude=use_claude_tagging)
    return selected
