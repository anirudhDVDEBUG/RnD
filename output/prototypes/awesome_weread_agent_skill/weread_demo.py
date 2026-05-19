#!/usr/bin/env python3
"""
Awesome WeRead Agent Skill Demo
================================
Demonstrates three capabilities of the WeRead ecosystem:
1. Browse the curated project catalog
2. Export mock WeRead highlights to Obsidian-compatible markdown
3. Generate MCP server configuration for Claude integration
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ── Mock WeRead ecosystem catalog ────────────────────────────────────────────

CATALOG = [
    {
        "name": "weread-mcp-server",
        "category": "MCP Server",
        "description": "Expose WeRead highlights, bookshelf, and annotations to AI agents via MCP",
        "language": "JavaScript",
        "stars": 342,
        "url": "https://github.com/example/weread-mcp-server",
        "tags": ["mcp-server", "weread", "agent-skill"],
    },
    {
        "name": "weread-obsidian-sync",
        "category": "Note Sync",
        "description": "Sync WeRead highlights and annotations into Obsidian vaults as structured markdown",
        "language": "Python",
        "stars": 521,
        "url": "https://github.com/example/weread-obsidian-sync",
        "tags": ["obsidian", "sync", "weread"],
    },
    {
        "name": "weread-flomo-bridge",
        "category": "Note Sync",
        "description": "Push WeRead reading notes to Flomo for spaced review and knowledge management",
        "language": "JavaScript",
        "stars": 198,
        "url": "https://github.com/example/weread-flomo-bridge",
        "tags": ["flomo", "sync", "weread"],
    },
    {
        "name": "weread-export-cli",
        "category": "Data Utility",
        "description": "Export highlights and annotations in Markdown, JSON, or CSV formats",
        "language": "Python",
        "stars": 415,
        "url": "https://github.com/example/weread-export-cli",
        "tags": ["export", "cli", "weread"],
    },
    {
        "name": "weread-stats-dashboard",
        "category": "Data Utility",
        "description": "Reading statistics and progress dashboards from WeRead data",
        "language": "TypeScript",
        "stars": 167,
        "url": "https://github.com/example/weread-stats-dashboard",
        "tags": ["dashboard", "statistics", "weread"],
    },
    {
        "name": "weread-notion-sync",
        "category": "Note Sync",
        "description": "Two-way sync between WeRead annotations and Notion databases",
        "language": "Python",
        "stars": 289,
        "url": "https://github.com/example/weread-notion-sync",
        "tags": ["notion", "sync", "weread"],
    },
]

# ── Mock WeRead reading data ─────────────────────────────────────────────────

MOCK_BOOKS = [
    {
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "progress": 78,
        "highlights": [
            {
                "text": "Nothing in life is as important as you think it is, while you are thinking about it.",
                "chapter": "Chapter 38: Thinking About Life",
                "page": 402,
                "date": "2026-05-10",
                "note": "Focusing illusion - relevant to product design decisions",
            },
            {
                "text": "A reliable way to make people believe in falsehoods is frequent repetition.",
                "chapter": "Chapter 5: Cognitive Ease",
                "page": 62,
                "date": "2026-05-08",
                "note": "",
            },
            {
                "text": "We can be blind to the obvious, and we are also blind to our blindness.",
                "chapter": "Chapter 2: Attention and Effort",
                "page": 24,
                "date": "2026-05-05",
                "note": "Core insight for building better AI interfaces",
            },
        ],
    },
    {
        "title": "The Design of Everyday Things",
        "author": "Don Norman",
        "progress": 100,
        "highlights": [
            {
                "text": "Design is really an act of communication, which means having a deep understanding of the person with whom the designer is communicating.",
                "chapter": "Chapter 1: The Psychopathology of Everyday Things",
                "page": 8,
                "date": "2026-04-28",
                "note": "Applies directly to agent skill UX",
            },
            {
                "text": "Good design is actually a lot harder to notice than poor design, in part because good designs fit our needs so well that the design is invisible.",
                "chapter": "Chapter 1: The Psychopathology of Everyday Things",
                "page": 12,
                "date": "2026-04-29",
                "note": "",
            },
        ],
    },
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "progress": 45,
        "highlights": [
            {
                "text": "You do not rise to the level of your goals. You fall to the level of your systems.",
                "chapter": "Chapter 1: The Surprising Power of Atomic Habits",
                "page": 27,
                "date": "2026-05-15",
                "note": "System thinking for agent workflows",
            },
        ],
    },
]


def print_header(title: str) -> None:
    width = 60
    print("\n" + "=" * width)
    print(f"  {title}")
    print("=" * width)


def browse_catalog(category_filter: str | None = None) -> None:
    """Display the curated WeRead ecosystem catalog."""
    print_header("WeRead Ecosystem Catalog")

    items = CATALOG
    if category_filter:
        items = [c for c in CATALOG if c["category"].lower() == category_filter.lower()]

    # Group by category
    categories: dict[str, list] = {}
    for item in items:
        categories.setdefault(item["category"], []).append(item)

    for cat, projects in categories.items():
        print(f"\n  [{cat}]")
        print(f"  {'─' * 50}")
        for p in sorted(projects, key=lambda x: -x["stars"]):
            print(f"  ★ {p['stars']:>4}  {p['name']}")
            print(f"         {p['description']}")
            print(f"         Lang: {p['language']}  Tags: {', '.join(p['tags'])}")

    print(f"\n  Total: {len(items)} projects across {len(categories)} categories")


def export_to_obsidian(output_dir: str = "output/obsidian_vault") -> None:
    """Export mock WeRead highlights to Obsidian-compatible markdown files."""
    print_header("Export WeRead Highlights -> Obsidian")

    vault_path = Path(output_dir)
    vault_path.mkdir(parents=True, exist_ok=True)

    total_highlights = 0

    for book in MOCK_BOOKS:
        safe_title = book["title"].replace(" ", "_").replace(",", "")
        filepath = vault_path / f"{safe_title}.md"

        lines = [
            f"# {book['title']}",
            f"",
            f"- **Author**: {book['author']}",
            f"- **Reading Progress**: {book['progress']}%",
            f"- **Highlights**: {len(book['highlights'])}",
            f"- **Synced from**: WeRead (微信读书)",
            f"- **Last sync**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"",
            f"---",
            f"",
            f"## Highlights",
            f"",
        ]

        for i, hl in enumerate(book["highlights"], 1):
            lines.append(f"### Highlight {i}")
            lines.append(f"")
            lines.append(f"> {hl['text']}")
            lines.append(f"")
            lines.append(f"- **Chapter**: {hl['chapter']}")
            lines.append(f"- **Page**: {hl['page']}")
            lines.append(f"- **Date**: {hl['date']}")
            if hl["note"]:
                lines.append(f"- **Note**: {hl['note']}")
            lines.append(f"")
            total_highlights += 1

        # Add backlinks section for Obsidian graph
        lines.extend([
            "---",
            "",
            "## Related",
            "",
            f"- [[WeRead Reading Log]]",
            f"- [[{book['author']}]]",
            "",
        ])

        filepath.write_text("\n".join(lines), encoding="utf-8")
        print(f"  [OK] {filepath}  ({len(book['highlights'])} highlights)")

    # Create index file
    index_path = vault_path / "WeRead_Reading_Log.md"
    index_lines = [
        "# WeRead Reading Log",
        "",
        f"*Auto-synced from WeRead on {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "| Book | Author | Progress | Highlights |",
        "|------|--------|----------|------------|",
    ]
    for book in MOCK_BOOKS:
        safe_title = book["title"].replace(" ", "_").replace(",", "")
        index_lines.append(
            f"| [[{safe_title}]] | {book['author']} | {book['progress']}% | {len(book['highlights'])} |"
        )
    index_lines.append("")
    index_path.write_text("\n".join(index_lines), encoding="utf-8")
    print(f"  [OK] {index_path}  (index)")

    print(f"\n  Exported {total_highlights} highlights from {len(MOCK_BOOKS)} books")
    print(f"  Vault location: {vault_path.resolve()}")


def export_json(output_dir: str = "output") -> None:
    """Export highlights as structured JSON."""
    print_header("Export WeRead Data -> JSON")

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    export_data = {
        "exported_at": datetime.now().isoformat(),
        "source": "WeRead (微信读书)",
        "books": MOCK_BOOKS,
        "stats": {
            "total_books": len(MOCK_BOOKS),
            "total_highlights": sum(len(b["highlights"]) for b in MOCK_BOOKS),
            "books_completed": sum(1 for b in MOCK_BOOKS if b["progress"] == 100),
            "avg_progress": round(
                sum(b["progress"] for b in MOCK_BOOKS) / len(MOCK_BOOKS), 1
            ),
        },
    }

    json_path = out_path / "weread_export.json"
    json_path.write_text(json.dumps(export_data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"  [OK] {json_path}")
    print(f"\n  Stats:")
    for k, v in export_data["stats"].items():
        label = k.replace("_", " ").title()
        print(f"    {label}: {v}")


def generate_mcp_config() -> None:
    """Generate example MCP server config for Claude integration."""
    print_header("MCP Server Config for Claude")

    config = {
        "mcpServers": {
            "weread": {
                "command": "node",
                "args": ["path/to/weread-mcp-server/index.js"],
                "env": {
                    "WEREAD_TOKEN": "your-weread-token-here",
                    "WEREAD_COOKIE": "your-weread-cookie-here",
                },
            }
        }
    }

    print("\n  Add this to ~/.claude.json or ~/.claude/settings.json:\n")
    print(json.dumps(config, indent=2))

    out_path = Path("output/mcp_config_example.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"\n  [OK] Saved to {out_path}")


def reading_stats() -> None:
    """Display reading statistics summary."""
    print_header("WeRead Reading Statistics")

    total_hl = sum(len(b["highlights"]) for b in MOCK_BOOKS)
    completed = sum(1 for b in MOCK_BOOKS if b["progress"] == 100)
    in_progress = len(MOCK_BOOKS) - completed
    avg_progress = sum(b["progress"] for b in MOCK_BOOKS) / len(MOCK_BOOKS)
    notes_count = sum(
        1 for b in MOCK_BOOKS for h in b["highlights"] if h["note"]
    )

    print(f"""
  Books in Library:    {len(MOCK_BOOKS)}
  Completed:           {completed}
  In Progress:         {in_progress}
  Average Progress:    {avg_progress:.0f}%
  Total Highlights:    {total_hl}
  Annotated Notes:     {notes_count}

  Most Highlighted:    {max(MOCK_BOOKS, key=lambda b: len(b['highlights']))['title']}
  Latest Activity:     {max(h['date'] for b in MOCK_BOOKS for h in b['highlights'])}
""")


def main() -> None:
    print("\n" + "=" * 60)
    print("  Awesome WeRead Agent Skill Demo")
    print("  WeRead (微信读书) Ecosystem Explorer")
    print("=" * 60)

    # 1. Browse catalog
    browse_catalog()

    # 2. Show reading stats
    reading_stats()

    # 3. Export to Obsidian
    export_to_obsidian()

    # 4. Export JSON
    export_json()

    # 5. Generate MCP config
    generate_mcp_config()

    # Final summary
    print_header("Summary")
    print("""
  This demo showed:
  1. Browsing the curated WeRead ecosystem (6 projects, 3 categories)
  2. Reading statistics from mock WeRead data
  3. Exporting highlights to Obsidian-compatible markdown
  4. Exporting structured JSON for downstream processing
  5. Generating MCP server config for Claude integration

  Next steps:
  - Install a real WeRead MCP server from the catalog
  - Configure authentication with your WeRead account
  - Set up automated sync to your note-taking tool

  See HOW_TO_USE.md for detailed setup instructions.
""")


if __name__ == "__main__":
    main()
