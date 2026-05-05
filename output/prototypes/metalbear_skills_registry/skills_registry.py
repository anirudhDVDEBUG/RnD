#!/usr/bin/env python3
"""CLI tool to browse, search, and install skills from the MetalBear community registry."""

import argparse
import os
import sys
from pathlib import Path

from registry_data import REGISTRY


def cmd_list(args):
    """List all available skills."""
    print(f"\nAvailable skills ({len(REGISTRY)}):\n")
    # Group by category
    categories = {}
    for skill in REGISTRY:
        cat = skill["category"]
        categories.setdefault(cat, []).append(skill)

    for cat in sorted(categories.keys()):
        print(f"  [{cat}]")
        for skill in categories[cat]:
            print(f"    {skill['name']:<22} {skill['description']}")
        print()


def cmd_search(args):
    """Search skills by keyword."""
    keyword = args.keyword.lower()
    matches = [
        s for s in REGISTRY
        if keyword in s["name"].lower()
        or keyword in s["description"].lower()
        or any(keyword in t for t in s["triggers"])
    ]

    if not matches:
        print(f'\nNo skills found matching "{args.keyword}"')
        return

    print(f'\nFound {len(matches)} skill(s) matching "{args.keyword}":\n')
    for skill in matches:
        print(f"  {skill['name']:<22} {skill['description']}")
    print()


def cmd_show(args):
    """Show details for a specific skill."""
    skill = next((s for s in REGISTRY if s["name"] == args.name), None)
    if not skill:
        print(f'\nSkill "{args.name}" not found. Use "list" to see available skills.')
        return

    print(f"\n{'=' * 60}")
    print(f"  {skill['name']}")
    print(f"{'=' * 60}")
    print(f"\n  Description: {skill['description']}")
    print(f"  Category:    {skill['category']}")
    print(f"  Triggers:    {', '.join(skill['triggers'])}")
    print(f"\n--- SKILL.md preview ---\n")
    print(skill["skill_md"])


def cmd_install(args):
    """Install a skill into .claude/skills/ directory."""
    skill = next((s for s in REGISTRY if s["name"] == args.name), None)
    if not skill:
        print(f'\nSkill "{args.name}" not found. Use "list" to see available skills.')
        return

    if args.global_install:
        target_dir = Path.home() / ".claude" / "skills" / skill["name"]
        target_file = target_dir / "SKILL.md"
    else:
        target_dir = Path(".claude") / "skills"
        target_file = target_dir / f"{skill['name']}.md"

    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(skill["skill_md"])

    print(f'\nInstalled "{skill["name"]}" -> {target_file}')
    print(f"The skill is now active in Claude Code sessions for this {'user' if args.global_install else 'project'}.")


def main():
    parser = argparse.ArgumentParser(
        description="MetalBear Skills Registry - Browse and install Claude Code skills"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # list
    subparsers.add_parser("list", help="List all available skills")

    # search
    search_p = subparsers.add_parser("search", help="Search skills by keyword")
    search_p.add_argument("keyword", help="Keyword to search for")

    # show
    show_p = subparsers.add_parser("show", help="Show details for a skill")
    show_p.add_argument("name", help="Skill name")

    # install
    install_p = subparsers.add_parser("install", help="Install a skill")
    install_p.add_argument("name", help="Skill name to install")
    install_p.add_argument("--global", dest="global_install", action="store_true",
                           help="Install globally (~/.claude/skills/)")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "install":
        cmd_install(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
