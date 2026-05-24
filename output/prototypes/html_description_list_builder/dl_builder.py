#!/usr/bin/env python3
"""
HTML Description List Builder

Generates semantic, accessible HTML <dl> markup from structured data.
Supports multiple <dd> per <dt>, optional <div> grouping, and ARIA labeling.
"""

import json
import sys
from typing import Optional


def build_dl(
    items: list[dict],
    wrap_divs: bool = False,
    heading_id: Optional[str] = None,
    indent: int = 2,
) -> str:
    """Build an HTML description list from structured data.

    Args:
        items: List of dicts with "term" (str) and "descriptions" (str or list[str]).
        wrap_divs: Wrap each dt/dd group in a <div> for CSS hooks.
        heading_id: If set, adds aria-labelledby to the <dl>.
        indent: Number of spaces per indent level.

    Returns:
        Formatted HTML string.
    """
    sp = " " * indent
    sp2 = " " * (indent * 2)

    aria = f' aria-labelledby="{heading_id}"' if heading_id else ""
    lines = [f"<dl{aria}>"]

    for item in items:
        term = item["term"]
        descs = item["descriptions"]
        if isinstance(descs, str):
            descs = [descs]

        if wrap_divs:
            lines.append(f"{sp}<div>")
            lines.append(f"{sp2}<dt>{term}</dt>")
            for d in descs:
                lines.append(f"{sp2}<dd>{d}</dd>")
            lines.append(f"{sp}</div>")
        else:
            lines.append(f"{sp}<dt>{term}</dt>")
            for d in descs:
                lines.append(f"{sp}<dd>{d}</dd>")

    lines.append("</dl>")
    return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            config = json.load(f)
    else:
        config = json.load(sys.stdin)

    heading_id = config.get("heading_id")
    wrap_divs = config.get("wrap_divs", False)
    items = config["items"]

    if heading_id:
        tag = config.get("heading_tag", "h2")
        heading_text = config.get("heading_text", heading_id.replace("-", " ").title())
        print(f'<{tag} id="{heading_id}">{heading_text}</{tag}>')

    print(build_dl(items, wrap_divs=wrap_divs, heading_id=heading_id))


if __name__ == "__main__":
    main()
