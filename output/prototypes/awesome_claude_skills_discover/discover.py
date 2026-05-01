#!/usr/bin/env python3
"""
Awesome Claude Skills Discovery Tool

Fetches, parses, browses, and searches community Claude Skills
from the ComposioHQ/awesome-claude-skills curated list.
Supports installing skills into a local .claude/skills/ directory.
"""

import argparse
import os
import re
import sys
import urllib.request
import urllib.error

CATALOG_URL = "https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/main/README.md"
CACHE_PATH = "/tmp/awesome-claude-skills-catalog.md"

# Fallback sample catalog for offline/demo use
SAMPLE_CATALOG = """\
# Awesome Claude Skills

A curated list of awesome Claude Skills, resources, and tools for customizing Claude AI workflows.

## Table of Contents
- [AI Agents](#ai-agents)
- [Automation](#automation)
- [Code Quality](#code-quality)
- [DevOps](#devops)
- [MCP Servers](#mcp-servers)
- [SaaS Integrations](#saas-integrations)
- [Workflow Automation](#workflow-automation)

## AI Agents

- [claude-agent-router](https://github.com/example/claude-agent-router) - Routes tasks to specialized sub-agents based on intent classification. ⭐ 2,340
- [multi-agent-orchestrator](https://github.com/example/multi-agent-orchestrator) - Orchestrate multiple Claude agents working together on complex tasks. ⭐ 1,890
- [agent-memory-skill](https://github.com/example/agent-memory-skill) - Persistent memory management for Claude agent sessions. ⭐ 1,120

## Automation

- [ci-cd-skill](https://github.com/example/ci-cd-skill) - Automate CI/CD pipeline creation and management with Claude. ⭐ 3,210
- [deploy-assistant](https://github.com/example/deploy-assistant) - One-command deployment automation for cloud platforms. ⭐ 2,780
- [cron-scheduler](https://github.com/example/cron-scheduler) - Schedule and manage recurring tasks through Claude. ⭐ 1,450

## Code Quality

- [test-generator](https://github.com/example/test-generator) - Automatically generate unit and integration tests for your codebase. ⭐ 4,560
- [lint-fixer](https://github.com/example/lint-fixer) - Detect and auto-fix linting issues across multiple languages. ⭐ 2,100
- [code-reviewer](https://github.com/example/code-reviewer) - AI-powered code review with actionable feedback. ⭐ 3,890
- [refactor-skill](https://github.com/example/refactor-skill) - Intelligent code refactoring suggestions and automation. ⭐ 1,670

## DevOps

- [docker-skill](https://github.com/example/docker-skill) - Manage Docker containers, images, and compose files. ⭐ 5,120
- [kubernetes-skill](https://github.com/example/kubernetes-skill) - Kubernetes cluster management and debugging. ⭐ 4,230
- [terraform-skill](https://github.com/example/terraform-skill) - Infrastructure as Code with Terraform through Claude. ⭐ 2,890
- [monitoring-skill](https://github.com/example/monitoring-skill) - Set up and manage application monitoring and alerting. ⭐ 1,340

## MCP Servers

- [mcp-github](https://github.com/example/mcp-github) - GitHub MCP server for repository management. ⭐ 6,780
- [mcp-slack](https://github.com/example/mcp-slack) - Slack MCP server for messaging and channel management. ⭐ 3,450
- [mcp-database](https://github.com/example/mcp-database) - Database MCP server supporting PostgreSQL, MySQL, SQLite. ⭐ 4,120
- [mcp-filesystem](https://github.com/example/mcp-filesystem) - Enhanced filesystem operations via MCP. ⭐ 2,560

## SaaS Integrations

- [slack-notifier](https://github.com/example/slack-notifier) - Send Slack notifications and manage channels from Claude. ⭐ 2,340
- [github-actions-skill](https://github.com/example/github-actions-skill) - Create and manage GitHub Actions workflows. ⭐ 3,120
- [jira-skill](https://github.com/example/jira-skill) - Manage Jira tickets, sprints, and boards. ⭐ 1,890
- [notion-skill](https://github.com/example/notion-skill) - Read and write Notion pages and databases. ⭐ 2,670

## Workflow Automation

- [git-workflow](https://github.com/example/git-workflow) - Automated git branching, merging, and PR workflows. ⭐ 3,560
- [file-organizer](https://github.com/example/file-organizer) - Intelligent file organization and cleanup. ⭐ 1,230
- [project-scaffolder](https://github.com/example/project-scaffolder) - Generate project boilerplate from templates. ⭐ 2,890
- [release-manager](https://github.com/example/release-manager) - Automate versioning, changelogs, and releases. ⭐ 1,780
"""


def fetch_catalog(use_cache=True):
    """Fetch the awesome-claude-skills catalog from GitHub or cache."""
    if use_cache and os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            content = f.read()
        if content.strip():
            print(f"[+] Loaded catalog from cache: {CACHE_PATH}")
            return content

    print(f"[*] Fetching catalog from {CATALOG_URL} ...")
    try:
        req = urllib.request.Request(CATALOG_URL, headers={"User-Agent": "awesome-claude-skills-discover/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8")
        with open(CACHE_PATH, "w") as f:
            f.write(content)
        print(f"[+] Catalog fetched and cached ({len(content)} bytes)")
        return content
    except (urllib.error.URLError, OSError) as e:
        print(f"[!] Could not fetch catalog: {e}")
        print("[*] Using built-in sample catalog for demo purposes")
        return SAMPLE_CATALOG


def parse_skills(catalog_text):
    """Parse skills from the markdown catalog into structured entries."""
    skills = []
    current_category = "Uncategorized"

    for line in catalog_text.splitlines():
        # Detect category headings (## Level)
        heading_match = re.match(r'^##\s+(.+)', line)
        if heading_match:
            cat = heading_match.group(1).strip()
            # Skip non-category headings
            if cat.lower() not in ("table of contents", "contents", "contributing", "license"):
                current_category = cat

        # Detect skill entries: - [name](url) - description
        skill_match = re.match(
            r'^\s*[-*]\s+\[([^\]]+)\]\(([^)]+)\)\s*[-–—:]\s*(.+)', line
        )
        if skill_match:
            name = skill_match.group(1).strip()
            url = skill_match.group(2).strip()
            desc = skill_match.group(3).strip()

            # Extract star count if present
            stars = 0
            star_match = re.search(r'[⭐★]\s*([\d,]+)', desc)
            if star_match:
                stars = int(star_match.group(1).replace(",", ""))

            skills.append({
                "name": name,
                "url": url,
                "description": desc,
                "category": current_category,
                "stars": stars,
            })

    return skills


def search_skills(skills, keyword):
    """Search skills by keyword in name, description, or category."""
    keyword_lower = keyword.lower()
    results = []
    for s in skills:
        if (keyword_lower in s["name"].lower()
                or keyword_lower in s["description"].lower()
                or keyword_lower in s["category"].lower()):
            results.append(s)
    return results


def list_categories(skills):
    """List all unique categories with skill counts."""
    cats = {}
    for s in skills:
        cats[s["category"]] = cats.get(s["category"], 0) + 1
    return cats


def print_skills(skills, title="Results"):
    """Pretty-print a list of skills."""
    print(f"\n{'=' * 60}")
    print(f"  {title} ({len(skills)} skills)")
    print(f"{'=' * 60}")
    for s in skills:
        stars_str = f" [{s['stars']}★]" if s["stars"] else ""
        print(f"\n  [{s['category']}]{stars_str}")
        print(f"  {s['name']}")
        print(f"  {s['url']}")
        print(f"  {s['description']}")
    print()


def install_skill(skill, install_dir=".claude/skills"):
    """Simulate installing a skill by creating a stub SKILL.md."""
    os.makedirs(install_dir, exist_ok=True)
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', skill["name"])
    filepath = os.path.join(install_dir, f"{safe_name}.md")

    content = f"""---
name: {skill['name']}
source: {skill['url']}
category: {skill['category']}
---

# {skill['name']}

{skill['description']}

Installed from: {skill['url']}
Category: {skill['category']}

> To complete installation, fetch the full SKILL.md from the source repository:
> curl -sL {skill['url'].replace('github.com', 'raw.githubusercontent.com').rstrip('/')}/main/SKILL.md -o {filepath}
"""
    with open(filepath, "w") as f:
        f.write(content)
    print(f"[+] Installed skill stub: {filepath}")
    return filepath


def demo_run():
    """Run a full demonstration of the discovery tool."""
    print("=" * 60)
    print("  Awesome Claude Skills Discovery Tool")
    print("  Demo Run")
    print("=" * 60)

    # Step 1: Fetch catalog
    print("\n--- Step 1: Fetch Skill Catalog ---")
    catalog = fetch_catalog(use_cache=False)

    # Step 2: Parse skills
    print("\n--- Step 2: Parse Skills ---")
    skills = parse_skills(catalog)
    print(f"[+] Parsed {len(skills)} skills from catalog")

    if not skills:
        print("[!] No skills found in catalog. Using sample catalog.")
        skills = parse_skills(SAMPLE_CATALOG)
        print(f"[+] Parsed {len(skills)} skills from sample catalog")

    # Step 3: List categories
    print("\n--- Step 3: Browse Categories ---")
    cats = list_categories(skills)
    for cat, count in sorted(cats.items()):
        print(f"  - {cat}: {count} skills")

    # Step 4: Search for skills
    search_terms = ["docker", "git", "test", "mcp"]
    for term in search_terms:
        print(f"\n--- Step 4: Search for '{term}' ---")
        results = search_skills(skills, term)
        if results:
            print_skills(results, title=f"Search: '{term}'")
        else:
            print(f"  No skills found matching '{term}'")

    # Step 5: Install a skill
    print("\n--- Step 5: Install a Skill ---")
    # Pick the first skill with the most stars, or just the first one
    top_skill = max(skills, key=lambda s: s["stars"]) if skills else None
    if top_skill:
        print(f"[*] Installing top skill: {top_skill['name']} ({top_skill['stars']}★)")
        path = install_skill(top_skill)
        print(f"\n[+] Installed skill contents:")
        with open(path, "r") as f:
            print(f.read())

    # Step 6: Verify installation
    print("--- Step 6: Verify Installation ---")
    install_dir = ".claude/skills"
    if os.path.isdir(install_dir):
        files = os.listdir(install_dir)
        print(f"[+] Skills directory: {install_dir}/")
        for fn in files:
            size = os.path.getsize(os.path.join(install_dir, fn))
            print(f"    {fn} ({size} bytes)")
    else:
        print("[!] No skills directory found")

    print("\n" + "=" * 60)
    print("  Demo complete!")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Discover, browse, and install community Claude Skills"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("demo", help="Run full demo")
    sub.add_parser("browse", help="Browse all categories")
    sub.add_parser("list", help="List all skills")

    sp_search = sub.add_parser("search", help="Search skills by keyword")
    sp_search.add_argument("keyword", help="Search keyword")

    sp_install = sub.add_parser("install", help="Install a skill by name")
    sp_install.add_argument("name", help="Skill name to install")

    args = parser.parse_args()

    if args.command == "demo" or args.command is None:
        demo_run()
        return

    catalog = fetch_catalog()
    skills = parse_skills(catalog)
    if not skills:
        skills = parse_skills(SAMPLE_CATALOG)

    if args.command == "browse":
        cats = list_categories(skills)
        print(f"\nCategories ({len(cats)}):")
        for cat, count in sorted(cats.items()):
            print(f"  - {cat}: {count} skills")

    elif args.command == "list":
        print_skills(skills, title="All Skills")

    elif args.command == "search":
        results = search_skills(skills, args.keyword)
        if results:
            print_skills(results, title=f"Search: '{args.keyword}'")
        else:
            print(f"No skills found matching '{args.keyword}'")

    elif args.command == "install":
        matches = [s for s in skills if args.name.lower() in s["name"].lower()]
        if matches:
            install_skill(matches[0])
        else:
            print(f"No skill found matching '{args.name}'")


if __name__ == "__main__":
    main()
