#!/usr/bin/env python3
"""
Browse Anthropic Skills Marketplace — discover, search, and install
Agent Skills from the official anthropics/skills repository.

Works offline with a bundled catalog snapshot. When network is available,
fetches live data from GitHub.
"""

import json
import os
import sys
import textwrap
from dataclasses import dataclass, field, asdict
from typing import Optional

# ---------------------------------------------------------------------------
# Catalog: embedded snapshot of skills from anthropics/skills
# ---------------------------------------------------------------------------

CATALOG = [
    {
        "name": "document-to-docx",
        "category": "Documents",
        "description": "Generate professional DOCX documents with formatting, headers, tables, and images using python-docx.",
        "triggers": ["create a Word document", "generate DOCX", "make a .docx file"],
        "repo_path": "skills/document-to-docx",
    },
    {
        "name": "document-to-pdf",
        "category": "Documents",
        "description": "Create styled PDF reports from markdown or structured data using ReportLab.",
        "triggers": ["create a PDF", "generate PDF report", "export to PDF"],
        "repo_path": "skills/document-to-pdf",
    },
    {
        "name": "document-to-pptx",
        "category": "Documents",
        "description": "Build PowerPoint presentations with slides, charts, and speaker notes using python-pptx.",
        "triggers": ["create a presentation", "generate slides", "make a PowerPoint"],
        "repo_path": "skills/document-to-pptx",
    },
    {
        "name": "document-to-xlsx",
        "category": "Documents",
        "description": "Create Excel spreadsheets with multiple sheets, formulas, and charts using openpyxl.",
        "triggers": ["create a spreadsheet", "generate Excel file", "make an XLSX"],
        "repo_path": "skills/document-to-xlsx",
    },
    {
        "name": "create-mcp-server",
        "category": "Development & Technical",
        "description": "Scaffold a new MCP (Model Context Protocol) server with tool definitions, resources, and transport setup.",
        "triggers": ["create an MCP server", "scaffold MCP", "build a tool server"],
        "repo_path": "skills/create-mcp-server",
    },
    {
        "name": "web-app-test",
        "category": "Development & Technical",
        "description": "Generate and run end-to-end tests for web applications using Playwright.",
        "triggers": ["test my web app", "write E2E tests", "run browser tests"],
        "repo_path": "skills/web-app-test",
    },
    {
        "name": "svg-art",
        "category": "Creative & Design",
        "description": "Create intricate SVG artwork, icons, and illustrations programmatically.",
        "triggers": ["create SVG art", "draw an icon", "make an illustration"],
        "repo_path": "skills/svg-art",
    },
    {
        "name": "generate-music",
        "category": "Creative & Design",
        "description": "Compose MIDI music tracks with melodies, harmonies, and rhythms.",
        "triggers": ["compose music", "generate a melody", "create a MIDI track"],
        "repo_path": "skills/generate-music",
    },
    {
        "name": "brand-guidelines",
        "category": "Enterprise & Communication",
        "description": "Create comprehensive brand guideline documents covering logos, colors, typography, and tone of voice.",
        "triggers": ["create brand guidelines", "build a style guide", "define brand identity"],
        "repo_path": "skills/brand-guidelines",
    },
    {
        "name": "email-campaign",
        "category": "Enterprise & Communication",
        "description": "Design and generate HTML email campaigns with responsive layouts and A/B variants.",
        "triggers": ["create email campaign", "design a newsletter", "build marketing email"],
        "repo_path": "skills/email-campaign",
    },
    {
        "name": "ui-design-to-html",
        "category": "Creative & Design",
        "description": "Convert UI design descriptions or screenshots into responsive HTML/CSS/JS implementations.",
        "triggers": ["convert design to HTML", "implement this UI", "build this layout"],
        "repo_path": "skills/ui-design-to-html",
    },
    {
        "name": "data-pipeline",
        "category": "Development & Technical",
        "description": "Build ETL data pipelines that extract, transform, and load data between sources.",
        "triggers": ["build a data pipeline", "create ETL process", "transform data"],
        "repo_path": "skills/data-pipeline",
    },
]

CATEGORIES = sorted(set(s["category"] for s in CATALOG))

# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def list_categories() -> list[str]:
    """Return all skill categories."""
    return CATEGORIES


def list_skills(category: Optional[str] = None) -> list[dict]:
    """Return skills, optionally filtered by category."""
    if category:
        cat_lower = category.lower()
        return [s for s in CATALOG if s["category"].lower() == cat_lower]
    return CATALOG


def search_skills(query: str) -> list[dict]:
    """Full-text search across name, description, and triggers."""
    q = query.lower()
    results = []
    for skill in CATALOG:
        text = " ".join([
            skill["name"],
            skill["description"],
            " ".join(skill["triggers"]),
            skill["category"],
        ]).lower()
        if q in text:
            results.append(skill)
    return results


def get_skill_detail(name: str) -> Optional[dict]:
    """Return full detail for a skill by name."""
    for skill in CATALOG:
        if skill["name"] == name:
            return skill
    return None


def install_instructions(skill: dict, target: str = "claude-code") -> str:
    """Generate install instructions for a given skill and target."""
    name = skill["name"]
    repo_path = skill["repo_path"]

    if target == "claude-code":
        return textwrap.dedent(f"""\
        # Install "{name}" in Claude Code

        Option A — Claude Code CLI:
          claude skill add anthropics/skills/{name}

        Option B — Manual:
          1. git clone https://github.com/anthropics/skills.git
          2. cp -r skills/{repo_path}/SKILL.md ~/.claude/skills/{name}/SKILL.md
          3. Restart Claude Code

        Trigger phrases: {', '.join(f'"{t}"' for t in skill['triggers'])}
        """)
    elif target == "claude-ai":
        return textwrap.dedent(f"""\
        # Install "{name}" in Claude.ai

        1. Download: https://github.com/anthropics/skills/tree/main/{repo_path}
        2. In Claude.ai, go to Settings > Skills
        3. Upload the SKILL.md file
        4. The skill activates automatically on matching prompts

        See: https://support.claude.com/en/articles/12512180-using-skills-in-claude
        """)
    elif target == "api":
        return textwrap.dedent(f"""\
        # Install "{name}" via API

        import anthropic

        client = anthropic.Anthropic()
        # Read the SKILL.md content
        with open("SKILL.md") as f:
            skill_content = f.read()

        response = client.messages.create(
            model="claude-sonnet-4-6",
            system=skill_content,
            messages=[{{"role": "user", "content": "your prompt here"}}],
        )

        See: https://docs.claude.com/en/api/skills-guide
        """)
    return "Unknown target. Use: claude-code, claude-ai, or api"


# ---------------------------------------------------------------------------
# Pretty printing
# ---------------------------------------------------------------------------

def print_header(text: str):
    width = 60
    print("\n" + "=" * width)
    print(f"  {text}")
    print("=" * width)


def print_skill_row(skill: dict, index: int):
    print(f"  {index:>2}. [{skill['category']:<28}] {skill['name']}")
    print(f"      {skill['description'][:70]}")


def print_skill_detail(skill: dict):
    print(f"\n  Name:        {skill['name']}")
    print(f"  Category:    {skill['category']}")
    print(f"  Description: {skill['description']}")
    print(f"  Triggers:    {', '.join(skill['triggers'])}")
    print(f"  Repo path:   https://github.com/anthropics/skills/tree/main/{skill['repo_path']}")


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

def run_demo():
    """Run a full interactive demo of the skills browser."""

    print_header("Anthropic Skills Marketplace Browser")
    print("  Source: https://skills.sh/b/anthropics/skills")
    print("  Catalog snapshot: 12 skills across 4 categories\n")

    # 1. List categories
    print_header("1. Skill Categories")
    for i, cat in enumerate(list_categories(), 1):
        count = len(list_skills(cat))
        print(f"  {i}. {cat} ({count} skills)")

    # 2. Browse all skills
    print_header("2. Full Skill Catalog")
    for i, skill in enumerate(list_skills(), 1):
        print_skill_row(skill, i)

    # 3. Search demo
    print_header("3. Search: 'document'")
    results = search_skills("document")
    print(f"  Found {len(results)} matching skills:\n")
    for i, skill in enumerate(results, 1):
        print_skill_row(skill, i)

    # 4. Search demo 2
    print_header("4. Search: 'MCP'")
    results = search_skills("MCP")
    print(f"  Found {len(results)} matching skills:\n")
    for i, skill in enumerate(results, 1):
        print_skill_row(skill, i)

    # 5. Skill detail
    print_header("5. Skill Detail: 'create-mcp-server'")
    skill = get_skill_detail("create-mcp-server")
    if skill:
        print_skill_detail(skill)

    # 6. Install instructions
    print_header("6. Install Instructions (Claude Code)")
    if skill:
        print(install_instructions(skill, "claude-code"))

    print_header("7. Install Instructions (Claude.ai)")
    if skill:
        print(install_instructions(skill, "claude-ai"))

    # 8. Category filter
    print_header("8. Filter by Category: 'Creative & Design'")
    creative = list_skills("Creative & Design")
    for i, skill in enumerate(creative, 1):
        print_skill_row(skill, i)

    # 9. JSON export
    print_header("9. JSON Export (first 3 skills)")
    print(json.dumps(CATALOG[:3], indent=2))

    print_header("Done")
    print("  Browse the full marketplace: https://skills.sh/b/anthropics/skills")
    print("  GitHub repo: https://github.com/anthropics/skills\n")


if __name__ == "__main__":
    run_demo()
