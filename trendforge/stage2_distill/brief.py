"""One-line summary per item (used in the digest email)."""
from __future__ import annotations

from typing import Any


def one_line(item: dict[str, Any]) -> str:
    title = (item.get("title") or "(untitled)").strip()
    md = item.get("raw_metadata") or {}
    src = item["source"]
    if src == "github":
        stars = md.get("stars")
        delta = md.get("stars_delta_today")
        suffix = ""
        if stars is not None:
            suffix = f" ({stars}★"
            if delta is not None:
                suffix += f", +{delta} today"
            suffix += ")"
        return f"{title}{suffix}"
    if src == "hn":
        pts = md.get("points")
        return f"{title} ({pts} points)" if pts else title
    if src == "youtube":
        return f"{item.get('author') or 'YT'}: {title}"
    return title
