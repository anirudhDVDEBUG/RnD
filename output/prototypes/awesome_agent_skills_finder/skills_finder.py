#!/usr/bin/env python3
"""
Awesome Agent Skills Finder
Browse, search, and install community agent skills from VoltAgent/awesome-agent-skills.
"""

import re
import sys
import os
import argparse
import urllib.request
import urllib.error
import shutil

CATALOG_URL = "https://raw.githubusercontent.com/VoltAgent/awesome-agent-skills/main/README.md"

# Fallback mock catalog for offline/demo use
MOCK_CATALOG = """# Awesome Agent Skills

A curated collection of 1000+ agent skills from official dev teams and the community.

## Categories

### DevOps
- [docker-debug](https://github.com/example/docker-debug) - Debug Docker containers interactively. `devops` `docker`
- [k8s-helper](https://github.com/example/k8s-helper) - Kubernetes cluster management and troubleshooting. `devops` `kubernetes`
- [ci-cd-optimizer](https://github.com/example/ci-cd-optimizer) - Optimize CI/CD pipeline configurations. `devops` `ci-cd`
- [terraform-assist](https://github.com/example/terraform-assist) - Terraform plan review and resource management. `devops` `terraform`

### Database
- [sql-query-builder](https://github.com/example/sql-query-builder) - Build and optimize SQL queries interactively. `database` `sql`
- [db-migration-helper](https://github.com/example/db-migration-helper) - Database migration planning and execution. `database` `migration`
- [redis-inspector](https://github.com/example/redis-inspector) - Inspect and manage Redis keys and data. `database` `redis`

### Testing
- [test-generator](https://github.com/example/test-generator) - Generate unit and integration tests automatically. `testing` `unit-test`
- [coverage-analyzer](https://github.com/example/coverage-analyzer) - Analyze test coverage and suggest improvements. `testing` `coverage`
- [e2e-playwright](https://github.com/example/e2e-playwright) - End-to-end testing with Playwright. `testing` `e2e`

### Frontend
- [react-component-gen](https://github.com/example/react-component-gen) - Generate React components from descriptions. `frontend` `react`
- [css-debugger](https://github.com/example/css-debugger) - Debug CSS layout and styling issues. `frontend` `css`
- [a11y-checker](https://github.com/example/a11y-checker) - Check and fix accessibility issues. `frontend` `accessibility`

### Backend
- [api-designer](https://github.com/example/api-designer) - Design RESTful and GraphQL APIs. `backend` `api`
- [auth-setup](https://github.com/example/auth-setup) - Set up authentication and authorization flows. `backend` `auth`
- [perf-profiler](https://github.com/example/perf-profiler) - Profile and optimize backend performance. `backend` `performance`

### Security
- [vuln-scanner](https://github.com/example/vuln-scanner) - Scan code for common security vulnerabilities. `security` `scanning`
- [secret-detector](https://github.com/example/secret-detector) - Detect hardcoded secrets and credentials. `security` `secrets`
- [dep-audit](https://github.com/example/dep-audit) - Audit dependencies for known CVEs. `security` `dependencies`

### Documentation
- [readme-gen](https://github.com/example/readme-gen) - Generate README files from code analysis. `docs` `readme`
- [api-docs](https://github.com/example/api-docs) - Generate API documentation from code. `docs` `api`
- [changelog-writer](https://github.com/example/changelog-writer) - Write changelogs from git history. `docs` `changelog`
"""

MOCK_SKILL_MD = """---
name: {name}
description: |
  {description}
  TRIGGER when: user asks about {category} tasks.
---

# {name}

{description}

## When to use
- Ask about {category} related tasks
- Need help with {name} workflows

## How to use
Run the skill by mentioning relevant trigger phrases in your Claude Code session.

## Requirements
- No external dependencies required
"""


def fetch_catalog():
    """Fetch the awesome-agent-skills README catalog, with offline fallback."""
    print("[*] Fetching skill catalog from VoltAgent/awesome-agent-skills...")
    try:
        req = urllib.request.Request(CATALOG_URL, headers={"User-Agent": "SkillsFinder/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8")
            print("[+] Live catalog fetched successfully.")
            return content
    except (urllib.error.URLError, OSError) as e:
        print(f"[!] Could not fetch live catalog ({e}). Using offline mock data.")
        return MOCK_CATALOG


def parse_skills(catalog_text):
    """Parse skill entries from the markdown catalog."""
    skills = []
    current_category = "Uncategorized"
    # Match lines like: - [name](url) - description `tag1` `tag2`
    entry_re = re.compile(
        r"^-\s+\[([^\]]+)\]\(([^)]+)\)\s*[-:—]?\s*(.+)$"
    )
    category_re = re.compile(r"^#{2,3}\s+(.+)$")

    for line in catalog_text.splitlines():
        cat_match = category_re.match(line.strip())
        if cat_match:
            current_category = cat_match.group(1).strip()
            continue

        entry_match = entry_re.match(line.strip())
        if entry_match:
            name = entry_match.group(1).strip()
            url = entry_match.group(2).strip()
            desc_raw = entry_match.group(3).strip()
            # Extract tags
            tags = re.findall(r"`([^`]+)`", desc_raw)
            desc = re.sub(r"\s*`[^`]+`", "", desc_raw).strip().rstrip(".")
            skills.append({
                "name": name,
                "url": url,
                "description": desc,
                "category": current_category,
                "tags": tags,
            })
    return skills


def search_skills(skills, query):
    """Search skills by name, description, category, or tags."""
    query_lower = query.lower()
    results = []
    for s in skills:
        searchable = f"{s['name']} {s['description']} {s['category']} {' '.join(s['tags'])}".lower()
        if query_lower in searchable:
            results.append(s)
    return results


def display_skills(skills, title="Skills"):
    """Pretty-print a list of skills."""
    print(f"\n{'=' * 60}")
    print(f" {title} ({len(skills)} found)")
    print(f"{'=' * 60}")
    for i, s in enumerate(skills, 1):
        tags = ", ".join(s["tags"]) if s["tags"] else "none"
        print(f"\n  {i}. {s['name']}")
        print(f"     Category: {s['category']}")
        print(f"     Tags:     {tags}")
        print(f"     Desc:     {s['description']}")
        print(f"     URL:      {s['url']}")
    print()


def install_skill(skill, global_install=False):
    """Install a skill by creating a SKILL.md in the appropriate directory."""
    if global_install:
        target_dir = os.path.expanduser("~/.claude/skills")
    else:
        target_dir = os.path.join(os.getcwd(), ".claude", "skills")

    os.makedirs(target_dir, exist_ok=True)
    filename = f"{skill['name']}.md"
    filepath = os.path.join(target_dir, filename)

    # Generate a SKILL.md (in a real scenario, we'd fetch from the repo)
    content = MOCK_SKILL_MD.format(
        name=skill["name"],
        description=skill["description"],
        category=skill["category"],
    )

    with open(filepath, "w") as f:
        f.write(content)

    print(f"[+] Installed skill '{skill['name']}' to: {filepath}")
    return filepath


def list_categories(skills):
    """List all unique categories."""
    cats = {}
    for s in skills:
        cats.setdefault(s["category"], 0)
        cats[s["category"]] += 1
    print(f"\n{'=' * 40}")
    print(f" Skill Categories")
    print(f"{'=' * 40}")
    for cat, count in sorted(cats.items()):
        print(f"  - {cat} ({count} skills)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Browse, search, and install agent skills from awesome-agent-skills"
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("browse", help="Browse all skills in the catalog")
    sub.add_parser("categories", help="List skill categories")

    sp_search = sub.add_parser("search", help="Search for skills by keyword")
    sp_search.add_argument("query", help="Search keyword (e.g. 'docker', 'testing', 'security')")

    sp_install = sub.add_parser("install", help="Install a skill by name")
    sp_install.add_argument("name", help="Skill name to install")
    sp_install.add_argument("--global", dest="global_install", action="store_true",
                            help="Install globally to ~/.claude/skills/")

    sp_demo = sub.add_parser("demo", help="Run full demo workflow")

    args = parser.parse_args()

    if not args.command:
        args.command = "demo"

    catalog = fetch_catalog()
    skills = parse_skills(catalog)

    if not skills:
        print("[!] No skills found in catalog.")
        sys.exit(1)

    print(f"[+] Parsed {len(skills)} skills from catalog.")

    if args.command == "browse":
        display_skills(skills, "All Skills")

    elif args.command == "categories":
        list_categories(skills)

    elif args.command == "search":
        results = search_skills(skills, args.query)
        if results:
            display_skills(results, f"Search results for '{args.query}'")
        else:
            print(f"\n[!] No skills found matching '{args.query}'.")

    elif args.command == "install":
        matches = [s for s in skills if s["name"].lower() == args.name.lower()]
        if not matches:
            matches = search_skills(skills, args.name)
        if matches:
            skill = matches[0]
            print(f"\n[*] Installing skill: {skill['name']}")
            install_skill(skill, global_install=args.global_install)
        else:
            print(f"\n[!] Skill '{args.name}' not found.")

    elif args.command == "demo":
        print("\n" + "=" * 60)
        print(" DEMO: Awesome Agent Skills Finder")
        print("=" * 60)

        # Step 1: List categories
        print("\n--- Step 1: List Categories ---")
        list_categories(skills)

        # Step 2: Search for skills
        for query in ["docker", "testing", "security"]:
            print(f"--- Step 2: Search for '{query}' ---")
            results = search_skills(skills, query)
            display_skills(results, f"Results for '{query}'")

        # Step 3: Install a skill (project-level)
        print("--- Step 3: Install a skill (project-level) ---")
        target = search_skills(skills, "docker")
        if target:
            filepath = install_skill(target[0])
            print(f"\n[*] Installed SKILL.md contents:")
            with open(filepath) as f:
                print(f.read())

        # Cleanup demo install
        demo_skills_dir = os.path.join(os.getcwd(), ".claude", "skills")
        if os.path.exists(demo_skills_dir):
            shutil.rmtree(os.path.join(os.getcwd(), ".claude"))
            print("[*] Cleaned up demo installation.")

        print("=" * 60)
        print(" Demo complete!")
        print("=" * 60)


if __name__ == "__main__":
    main()
