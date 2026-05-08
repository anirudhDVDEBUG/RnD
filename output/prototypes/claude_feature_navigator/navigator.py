#!/usr/bin/env python3
"""Claude Feature Navigator — discover, browse, and recommend Claude Code skills.

Maintains an embedded catalog of skills from the ComposioHQ/awesome-claude-skills
list and Composio marketplace. Supports keyword search, category browsing,
top-N rankings, and install instruction generation — all without network access.
"""

import json
import sys
import textwrap

# ---------------------------------------------------------------------------
# Embedded skill catalog (snapshot from awesome-claude-skills + Composio)
# ---------------------------------------------------------------------------

SKILL_CATALOG = [
    {
        "name": "commit-msg",
        "repo": "anthropics/skills/commit-msg",
        "category": "Productivity",
        "description": "Generate concise, conventional-commit-style messages from staged diffs.",
        "stars": 1240,
        "install_type": "skill",
        "tags": ["git", "commit", "automation"],
    },
    {
        "name": "code-review",
        "repo": "anthropics/skills/code-review",
        "category": "Code Quality",
        "description": "Automated PR review: finds bugs, style issues, and security concerns.",
        "stars": 980,
        "install_type": "skill",
        "tags": ["review", "pr", "quality", "linting"],
    },
    {
        "name": "test-gen",
        "repo": "composiohq/awesome-claude-skills/test-gen",
        "category": "Testing",
        "description": "Generate unit and integration tests for Python and TypeScript codebases.",
        "stars": 870,
        "install_type": "skill",
        "tags": ["testing", "unit-test", "coverage", "pytest"],
    },
    {
        "name": "docker-compose-gen",
        "repo": "composiohq/awesome-claude-skills/docker-compose-gen",
        "category": "DevOps",
        "description": "Scaffold docker-compose.yml files from project structure and Dockerfiles.",
        "stars": 640,
        "install_type": "skill",
        "tags": ["docker", "devops", "infrastructure", "containers"],
    },
    {
        "name": "api-docs",
        "repo": "composiohq/awesome-claude-skills/api-docs",
        "category": "Documentation",
        "description": "Auto-generate OpenAPI specs and markdown API docs from route handlers.",
        "stars": 550,
        "install_type": "skill",
        "tags": ["docs", "openapi", "api", "swagger"],
    },
    {
        "name": "changelog",
        "repo": "composiohq/awesome-claude-skills/changelog",
        "category": "Documentation",
        "description": "Build CHANGELOG.md entries from git log using keep-a-changelog format.",
        "stars": 430,
        "install_type": "skill",
        "tags": ["changelog", "release", "docs", "versioning"],
    },
    {
        "name": "ci-fix",
        "repo": "composiohq/awesome-claude-skills/ci-fix",
        "category": "DevOps",
        "description": "Diagnose and fix failing CI pipelines (GitHub Actions, GitLab CI).",
        "stars": 720,
        "install_type": "skill",
        "tags": ["ci", "github-actions", "pipeline", "debugging"],
    },
    {
        "name": "refactor-extract",
        "repo": "composiohq/awesome-claude-skills/refactor-extract",
        "category": "Productivity",
        "description": "Extract functions, classes, or modules from large files with correct imports.",
        "stars": 510,
        "install_type": "skill",
        "tags": ["refactor", "extract", "modules", "clean-code"],
    },
    {
        "name": "seo-agent-pipeline",
        "repo": "loganriebel/seo-agent-pipeline",
        "category": "Productivity",
        "description": "10-stage SEO content pipeline: keyword research through to published article.",
        "stars": 95,
        "install_type": "skill",
        "tags": ["seo", "content", "marketing", "pipeline"],
    },
    {
        "name": "email-design",
        "repo": "cosmoblk/email-design",
        "category": "Productivity",
        "description": "Email design skill: generate responsive HTML email templates.",
        "stars": 45,
        "install_type": "skill",
        "tags": ["email", "design", "html", "templates"],
    },
    {
        "name": "markpdf-skill",
        "repo": "gausoft/markpdf-skill",
        "category": "Documentation",
        "description": "Convert Markdown to styled PDF documents within Claude Code.",
        "stars": 60,
        "install_type": "skill",
        "tags": ["pdf", "markdown", "export", "conversion"],
    },
    {
        "name": "cybrix-skills",
        "repo": "cybrixcc/cybrix-skills",
        "category": "DevOps",
        "description": "Claude Code skills for cybersecurity workflows and auditing.",
        "stars": 110,
        "install_type": "skill",
        "tags": ["security", "audit", "cyber", "pentest"],
    },
    {
        "name": "slack-mcp",
        "repo": "modelcontextprotocol/servers/slack",
        "category": "Integrations",
        "description": "MCP server bridging Claude to Slack: read channels, post messages, search.",
        "stars": 1800,
        "install_type": "mcp",
        "tags": ["slack", "mcp", "messaging", "chat"],
    },
    {
        "name": "github-mcp",
        "repo": "modelcontextprotocol/servers/github",
        "category": "Integrations",
        "description": "MCP server for GitHub: issues, PRs, repos, actions — full API coverage.",
        "stars": 2100,
        "install_type": "mcp",
        "tags": ["github", "mcp", "api", "repos"],
    },
    {
        "name": "postgres-mcp",
        "repo": "modelcontextprotocol/servers/postgres",
        "category": "Integrations",
        "description": "MCP server for PostgreSQL: run queries, inspect schemas, manage migrations.",
        "stars": 1500,
        "install_type": "mcp",
        "tags": ["postgres", "database", "mcp", "sql"],
    },
    {
        "name": "filesystem-mcp",
        "repo": "modelcontextprotocol/servers/filesystem",
        "category": "Integrations",
        "description": "MCP server giving Claude safe, scoped access to local filesystem directories.",
        "stars": 1900,
        "install_type": "mcp",
        "tags": ["filesystem", "mcp", "local", "files"],
    },
    {
        "name": "lint-staged",
        "repo": "composiohq/awesome-claude-skills/lint-staged",
        "category": "Code Quality",
        "description": "Run linters on staged files before commit; auto-fix when possible.",
        "stars": 320,
        "install_type": "skill",
        "tags": ["lint", "eslint", "prettier", "staged"],
    },
    {
        "name": "dep-update",
        "repo": "composiohq/awesome-claude-skills/dep-update",
        "category": "DevOps",
        "description": "Check for outdated npm/pip dependencies and create upgrade PRs.",
        "stars": 280,
        "install_type": "skill",
        "tags": ["dependencies", "npm", "pip", "upgrade"],
    },
]

CATEGORIES = sorted(set(s["category"] for s in SKILL_CATALOG))

# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
BAR = "-" * 64


def _trunc(text: str, maxlen: int = 55) -> str:
    return text[:maxlen - 3] + "..." if len(text) > maxlen else text


def print_table(skills: list[dict], title: str = "") -> None:
    """Print a formatted table of skills."""
    if title:
        print(f"\n{BOLD}{CYAN}{'=' * 64}{RESET}")
        print(f"  {BOLD}{title}{RESET}")
        print(f"{BOLD}{CYAN}{'=' * 64}{RESET}")
    if not skills:
        print("  (no results)\n")
        return
    print(f"  {'Name':<22} {'Category':<15} {'Stars':>5}  {'Type':<6} Description")
    print(f"  {'-'*22} {'-'*15} {'-'*5}  {'-'*6} {'-'*40}")
    for s in skills:
        print(
            f"  {s['name']:<22} {s['category']:<15} {s['stars']:>5}  "
            f"{s['install_type']:<6} {_trunc(s['description'])}"
        )
    print()


def print_detail(skill: dict) -> None:
    """Print full detail + install instructions for one skill."""
    print(f"\n  {BOLD}{CYAN}{'─' * 50}{RESET}")
    print(f"  {BOLD}{skill['name']}{RESET}  ({skill['install_type']})")
    print(f"  {CYAN}{'─' * 50}{RESET}")
    print(f"  Repo     : https://github.com/{skill['repo']}")
    print(f"  Category : {skill['category']}")
    print(f"  Stars    : {skill['stars']}")
    print(f"  Tags     : {', '.join(skill['tags'])}")
    print(f"  {skill['description']}")
    print()
    print(f"  {BOLD}Install:{RESET}")
    if skill["install_type"] == "mcp":
        short = skill["name"].replace("-mcp", "")
        print(f"  Add to ~/.claude.json:")
        print(f'    "mcpServers": {{')
        print(f'      "{short}": {{')
        print(f'        "command": "npx",')
        print(f'        "args": ["-y", "@modelcontextprotocol/server-{short}"],')
        print(f'        "env": {{}}')
        print(f"      }}")
        print(f"    }}")
    else:
        print(f"    git clone https://github.com/{skill['repo']} /tmp/{skill['name']}")
        print(f"    mkdir -p ~/.claude/skills/{skill['name']}")
        print(f"    cp /tmp/{skill['name']}/SKILL.md ~/.claude/skills/{skill['name']}/SKILL.md")
    print()


# ---------------------------------------------------------------------------
# Core search / browse / recommend
# ---------------------------------------------------------------------------

def search(query: str) -> list[dict]:
    """Keyword search across name, description, tags, and category."""
    tokens = query.lower().split()
    scored = []
    for skill in SKILL_CATALOG:
        blob = " ".join([
            skill["name"], skill["description"],
            skill["category"], " ".join(skill["tags"]),
        ]).lower()
        score = sum(1 for t in tokens if t in blob)
        if score > 0:
            scored.append((score, skill))
    scored.sort(key=lambda x: (-x[0], -x[1]["stars"]))
    return [s[1] for s in scored]


def by_category(category: str) -> list[dict]:
    cat_low = category.lower()
    return sorted(
        [s for s in SKILL_CATALOG if s["category"].lower() == cat_low],
        key=lambda s: -s["stars"],
    )


def top_n(n: int = 5) -> list[dict]:
    return sorted(SKILL_CATALOG, key=lambda s: -s["stars"])[:n]


def recommend_for_workflow(workflow: str) -> list[dict]:
    """Recommend skills for a described workflow."""
    WORKFLOW_MAP = {
        "code review": ["code-review", "lint-staged"],
        "deployment": ["docker-compose-gen", "ci-fix", "dep-update"],
        "testing": ["test-gen"],
        "documentation": ["api-docs", "changelog", "markpdf-skill"],
        "git workflow": ["commit-msg", "changelog"],
        "security": ["cybrix-skills"],
        "marketing": ["seo-agent-pipeline", "email-design"],
    }
    wf_low = workflow.lower()
    direct = []
    for key, names in WORKFLOW_MAP.items():
        if key in wf_low:
            direct.extend(names)
    if direct:
        return [s for s in SKILL_CATALOG if s["name"] in direct]
    return search(workflow)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def run_demo():
    print(f"\n{BOLD}{CYAN}{'=' * 64}{RESET}")
    print(f"  {BOLD}CLAUDE FEATURE NAVIGATOR — Skill Discovery Demo{RESET}")
    print(f"  {DIM}Discover, browse & recommend Claude Code skills{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 64}{RESET}")

    # 1) Top skills
    print_table(top_n(5), "Top 5 Skills by Community Stars")

    # 2) Categories overview
    print(f"  {BOLD}Available categories:{RESET} {', '.join(CATEGORIES)}\n")

    # 3) Browse by category
    for cat in ["Code Quality", "DevOps", "Integrations"]:
        print_table(by_category(cat), f"Browse: {cat}")

    # 4) Keyword searches
    for query in ["testing coverage", "docker deploy", "slack messaging", "security audit"]:
        results = search(query)
        print_table(results, f'Search: "{query}"')

    # 5) Workflow recommendations
    print(f"\n{BOLD}{CYAN}{'=' * 64}{RESET}")
    print(f"  {BOLD}Workflow Recommendations{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 64}{RESET}")
    for wf in ["code review", "deployment", "documentation", "marketing"]:
        recs = recommend_for_workflow(wf)
        print(f"\n  {YELLOW}Workflow: {wf}{RESET}")
        for s in recs:
            print(f"    {GREEN}+{RESET} {s['name']:<22} {_trunc(s['description'], 45)}")

    # 6) Detail view with install instructions
    print(f"\n{BOLD}{CYAN}{'=' * 64}{RESET}")
    print(f"  {BOLD}Detailed View + Install Instructions{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 64}{RESET}")
    for name in ["code-review", "github-mcp"]:
        skill = next(s for s in SKILL_CATALOG if s["name"] == name)
        print_detail(skill)

    # 7) JSON export
    print(f"{BOLD}{CYAN}{'=' * 64}{RESET}")
    print(f"  {BOLD}JSON Export (top 3 skills){RESET}")
    print(f"{BOLD}{CYAN}{'=' * 64}{RESET}")
    print(json.dumps(top_n(3), indent=2))

    # 8) Catalog stats
    total = len(SKILL_CATALOG)
    skills_count = sum(1 for s in SKILL_CATALOG if s["install_type"] == "skill")
    mcp_count = sum(1 for s in SKILL_CATALOG if s["install_type"] == "mcp")
    print(f"\n  {BOLD}Catalog stats:{RESET} {total} entries — "
          f"{skills_count} skills, {mcp_count} MCP servers, "
          f"{len(CATEGORIES)} categories")
    total_stars = sum(s["stars"] for s in SKILL_CATALOG)
    print(f"  Total community stars: {total_stars:,}")

    print(f"\n{BOLD}{CYAN}{'=' * 64}{RESET}")
    print(f"  {BOLD}Demo complete.{RESET} See HOW_TO_USE.md for integration details.")
    print(f"{BOLD}{CYAN}{'=' * 64}{RESET}\n")


def interactive():
    """REPL for exploring skills."""
    print("Claude Feature Navigator — Interactive Mode")
    print("Commands: search <query> | category <name> | top [n] | detail <name>")
    print("          recommend <workflow> | categories | quit\n")
    while True:
        try:
            line = input("navigator> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not line:
            continue
        parts = line.split(maxsplit=1)
        cmd, arg = parts[0].lower(), (parts[1] if len(parts) > 1 else "")
        if cmd == "quit":
            break
        elif cmd == "search":
            print_table(search(arg), f'Search: "{arg}"')
        elif cmd == "category":
            print_table(by_category(arg), f"Category: {arg}")
        elif cmd == "top":
            n = int(arg) if arg.isdigit() else 5
            print_table(top_n(n), f"Top {n} Skills")
        elif cmd == "detail":
            matches = [s for s in SKILL_CATALOG if s["name"] == arg]
            print_detail(matches[0]) if matches else print(f"  Not found. Try: search {arg}")
        elif cmd == "recommend":
            recs = recommend_for_workflow(arg)
            print_table(recs, f'Recommended for: "{arg}"')
        elif cmd == "categories":
            print(f"  {', '.join(CATEGORIES)}")
        else:
            print(f"  Unknown command: {cmd}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive()
    else:
        run_demo()
