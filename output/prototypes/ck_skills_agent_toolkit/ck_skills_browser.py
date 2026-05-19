#!/usr/bin/env python3
"""
ck-skills Agent Toolkit Browser & Installer

Simulates browsing, searching, and installing skills from the
bestagentkits/ck-skills collection (14 curated Claude Code skills
by GoClaw / AgentBrain).

Works fully offline with embedded catalog data for demo purposes.
In production mode, clones the actual repo.
"""

import json
import os
import shutil
import sys
import textwrap
from pathlib import Path

# ---------------------------------------------------------------------------
# Embedded skill catalog (mirrors bestagentkits/ck-skills repo structure)
# ---------------------------------------------------------------------------
SKILL_CATALOG = [
    {
        "name": "auto-commit",
        "description": "Automatically stages and commits changes with AI-generated messages.",
        "tags": ["git", "automation", "workflow"],
        "author": "GoClaw",
    },
    {
        "name": "code-review",
        "description": "Performs thorough code reviews with security, performance, and style checks.",
        "tags": ["quality", "security", "review"],
        "author": "AgentBrain",
    },
    {
        "name": "deploy-helper",
        "description": "Guides deployment to common platforms (Vercel, Railway, Fly.io).",
        "tags": ["deployment", "devops", "cloud"],
        "author": "GoClaw",
    },
    {
        "name": "doc-generator",
        "description": "Generates README, API docs, and changelogs from source code.",
        "tags": ["documentation", "markdown", "automation"],
        "author": "AgentBrain",
    },
    {
        "name": "env-setup",
        "description": "Bootstraps dev environments with dotfiles, deps, and toolchains.",
        "tags": ["setup", "environment", "onboarding"],
        "author": "GoClaw",
    },
    {
        "name": "error-explainer",
        "description": "Decodes cryptic error messages and suggests targeted fixes.",
        "tags": ["debugging", "errors", "dx"],
        "author": "AgentBrain",
    },
    {
        "name": "git-workflow",
        "description": "Manages branching strategies, rebases, and PR workflows.",
        "tags": ["git", "branching", "collaboration"],
        "author": "GoClaw",
    },
    {
        "name": "migration-helper",
        "description": "Assists database and framework migrations with rollback plans.",
        "tags": ["database", "migration", "frameworks"],
        "author": "AgentBrain",
    },
    {
        "name": "perf-profiler",
        "description": "Profiles code for performance bottlenecks and suggests optimizations.",
        "tags": ["performance", "profiling", "optimization"],
        "author": "GoClaw",
    },
    {
        "name": "project-scaffold",
        "description": "Scaffolds new projects from templates (FastAPI, Next.js, CLI tools).",
        "tags": ["scaffold", "templates", "boilerplate"],
        "author": "AgentBrain",
    },
    {
        "name": "refactor-agent",
        "description": "Identifies and executes safe refactoring patterns across codebases.",
        "tags": ["refactoring", "clean-code", "patterns"],
        "author": "GoClaw",
    },
    {
        "name": "security-scan",
        "description": "Scans for common vulnerabilities (OWASP top 10, secrets, dependencies).",
        "tags": ["security", "scanning", "owasp"],
        "author": "AgentBrain",
    },
    {
        "name": "test-writer",
        "description": "Generates unit, integration, and snapshot tests for existing code.",
        "tags": ["testing", "unit-tests", "coverage"],
        "author": "GoClaw",
    },
    {
        "name": "ticket-drafter",
        "description": "Turns conversations and code diffs into structured Jira/Linear tickets.",
        "tags": ["project-management", "tickets", "agile"],
        "author": "AgentBrain",
    },
]

SKILL_MD_TEMPLATE = textwrap.dedent("""\
    ---
    name: {name}
    description: |
      {description}
    ---

    # {name}

    {description}

    ## When to use

    - Trigger: user mentions "{name}" or related keywords
    - Tags: {tags}

    ## Author

    {author} (via bestagentkits/ck-skills)
""")


def print_banner():
    print("=" * 64)
    print("  ck-skills Agent Toolkit  |  bestagentkits/ck-skills")
    print("  14 curated Claude Code skills by GoClaw / AgentBrain")
    print("=" * 64)
    print()


def list_skills(catalog, tag_filter=None):
    """List all skills, optionally filtering by tag."""
    print(f"{'#':<4} {'Skill':<22} {'Author':<14} {'Tags'}")
    print("-" * 64)
    for i, skill in enumerate(catalog, 1):
        tags = ", ".join(skill["tags"])
        if tag_filter and tag_filter.lower() not in tags.lower():
            continue
        print(f"{i:<4} {skill['name']:<22} {skill['author']:<14} {tags}")
    print()


def search_skills(catalog, query):
    """Search skills by name, description, or tag."""
    query_lower = query.lower()
    results = []
    for skill in catalog:
        searchable = f"{skill['name']} {skill['description']} {' '.join(skill['tags'])}".lower()
        if query_lower in searchable:
            results.append(skill)
    return results


def show_skill_detail(skill):
    """Show detailed info for a single skill."""
    print(f"\n  Skill: {skill['name']}")
    print(f"  Author: {skill['author']}")
    print(f"  Tags: {', '.join(skill['tags'])}")
    print(f"  Description: {skill['description']}")
    print(f"\n  SKILL.md preview:")
    print("  " + "-" * 40)
    md = SKILL_MD_TEMPLATE.format(
        name=skill["name"],
        description=skill["description"],
        tags=", ".join(skill["tags"]),
        author=skill["author"],
    )
    for line in md.splitlines():
        print(f"  {line}")
    print()


def install_skill(skill, target_dir):
    """Install a skill's SKILL.md into the target directory."""
    skill_dir = Path(target_dir) / skill["name"]
    skill_dir.mkdir(parents=True, exist_ok=True)
    md = SKILL_MD_TEMPLATE.format(
        name=skill["name"],
        description=skill["description"],
        tags=", ".join(skill["tags"]),
        author=skill["author"],
    )
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(md)
    return str(skill_file)


def run_demo():
    """Run the full non-interactive demo."""
    print_banner()

    # 1) List all skills
    print("[1/5] Browsing full skill catalog:\n")
    list_skills(SKILL_CATALOG)

    # 2) Search
    print("[2/5] Searching for 'security' skills:\n")
    results = search_skills(SKILL_CATALOG, "security")
    if results:
        list_skills(results)
    else:
        print("  No results found.\n")

    # 3) Show detail
    print("[3/5] Inspecting 'code-review' skill:")
    code_review = next(s for s in SKILL_CATALOG if s["name"] == "code-review")
    show_skill_detail(code_review)

    # 4) Install selected skills
    install_dir = Path("demo_output/.claude/skills")
    print(f"[4/5] Installing 3 skills to {install_dir}/\n")
    for name in ["code-review", "security-scan", "test-writer"]:
        skill = next(s for s in SKILL_CATALOG if s["name"] == name)
        path = install_skill(skill, install_dir)
        print(f"  Installed: {path}")
    print()

    # 5) Verify
    print("[5/5] Verifying installation:\n")
    for p in sorted(install_dir.rglob("SKILL.md")):
        rel = p.relative_to("demo_output")
        print(f"  {rel}")
    print()

    # Summary
    installed = list(install_dir.iterdir())
    print(f"Done! {len(installed)} skills installed to demo_output/.claude/skills/")
    print("In a real project, these would be at .claude/skills/ in your repo root.")
    print()

    # Export catalog as JSON for programmatic use
    catalog_path = Path("demo_output/skill_catalog.json")
    catalog_path.parent.mkdir(parents=True, exist_ok=True)
    catalog_path.write_text(json.dumps(SKILL_CATALOG, indent=2))
    print(f"Full catalog exported to {catalog_path}")


def run_interactive():
    """Run interactive mode for manual browsing."""
    print_banner()
    print("Interactive mode. Commands: list, search <query>, show <name>, install <name>, quit\n")

    install_dir = Path(".claude/skills")

    while True:
        try:
            cmd = input("ck-skills> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if not cmd:
            continue
        parts = cmd.split(maxsplit=1)
        action = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if action == "quit":
            print("Bye!")
            break
        elif action == "list":
            list_skills(SKILL_CATALOG, tag_filter=arg or None)
        elif action == "search" and arg:
            results = search_skills(SKILL_CATALOG, arg)
            if results:
                list_skills(results)
            else:
                print("No skills matched.\n")
        elif action == "show" and arg:
            matches = [s for s in SKILL_CATALOG if arg.lower() in s["name"].lower()]
            if matches:
                show_skill_detail(matches[0])
            else:
                print(f"No skill matching '{arg}'.\n")
        elif action == "install" and arg:
            matches = [s for s in SKILL_CATALOG if arg.lower() in s["name"].lower()]
            if matches:
                path = install_skill(matches[0], install_dir)
                print(f"  Installed: {path}\n")
            else:
                print(f"No skill matching '{arg}'.\n")
        else:
            print("Unknown command. Try: list, search <query>, show <name>, install <name>, quit\n")


if __name__ == "__main__":
    if "--interactive" in sys.argv:
        run_interactive()
    else:
        run_demo()
