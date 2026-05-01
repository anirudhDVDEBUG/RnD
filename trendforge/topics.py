"""Topic classifier — assigns each item to ONE primary topic.

Uses the structured `topics:` block in interests.yaml. Each item gets the
topic whose keywords it matches most strongly; ties are broken by topic
order (earlier topics in the YAML win).

Public API:
    classify(item, interests=None) -> str   # topic slug, or "other"
    topic_label(slug, interests=None) -> str
    all_topic_slugs(interests=None) -> list[str]
"""
from __future__ import annotations

import json
from typing import Any

from trendforge.config_loader import load_interests

OTHER = "other"


def _item_text(item: dict) -> str:
    parts = [
        item.get("title") or "",
        json.dumps(item.get("raw_metadata") or {}),
        " ".join(item.get("tags") or []) if isinstance(item.get("tags"), list) else "",
    ]
    return " ".join(parts).lower()


def _topics_block(interests: dict | None) -> dict[str, dict]:
    interests = interests or load_interests()
    return interests.get("topics") or {}


def classify(item: dict, interests: dict | None = None) -> str:
    """Return primary-topic slug for `item`. Falls back to 'other'."""
    topics = _topics_block(interests)
    if not topics:
        return OTHER
    text = _item_text(item)
    best_slug = OTHER
    best_count = 0
    for slug, cfg in topics.items():
        kws = cfg.get("keywords") or []
        hits = sum(1 for k in kws if k.lower() in text)
        if hits > best_count:
            best_count = hits
            best_slug = slug
    return best_slug if best_count > 0 else OTHER


def topic_label(slug: str, interests: dict | None = None) -> str:
    if slug == OTHER:
        return "Other"
    topics = _topics_block(interests)
    return (topics.get(slug) or {}).get("label", slug)


def all_topic_slugs(interests: dict | None = None) -> list[str]:
    topics = _topics_block(interests)
    return list(topics.keys()) + [OTHER]


def selection_config(interests: dict | None = None) -> dict:
    """Read quality gates from interests.yaml (with sane defaults)."""
    interests = interests or load_interests()
    sel = interests.get("selection") or {}
    return {
        "per_topic_top_k": int(sel.get("per_topic_top_k", 5)),
        "min_score": float(sel.get("min_score", 0.30)),
        "prototype_min_score": float(sel.get("prototype_min_score", 0.50)),
    }
