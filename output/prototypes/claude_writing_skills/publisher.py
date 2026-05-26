"""Publish markdown with frontmatter and TOC."""

import os
import re
from datetime import date


def generate_frontmatter(title: str, tags: list[str], description: str = "") -> str:
    """Generate YAML frontmatter block."""
    tag_str = ', '.join(f'"{t}"' for t in tags)
    return f"""---
title: "{title}"
date: {date.today().isoformat()}
tags: [{tag_str}]
description: "{description}"
---
"""


def generate_toc(content: str) -> str:
    """Generate a table of contents from markdown headings."""
    lines = content.split('\n')
    toc_lines = ["## Table of Contents\n"]
    for line in lines:
        match = re.match(r'^(#{2,3})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2)
            anchor = re.sub(r'[^a-z0-9\s-]', '', title.lower())
            anchor = re.sub(r'\s+', '-', anchor.strip())
            indent = "  " * (level - 2)
            toc_lines.append(f"{indent}- [{title}](#{anchor})")
    toc_lines.append("")
    return '\n'.join(toc_lines)


def publish(title: str, content: str, tags: list[str], output_dir: str = "output/published") -> str:
    """Assemble and write the final published markdown file."""
    os.makedirs(output_dir, exist_ok=True)

    description = content.split('\n\n')[0][:150].replace('"', "'") if content else ""
    frontmatter = generate_frontmatter(title, tags, description)
    toc = generate_toc(content)
    full_doc = frontmatter + "\n" + toc + "\n" + content

    filename = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') + '.md'
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        f.write(full_doc)

    return filepath
