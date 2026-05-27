#!/usr/bin/env python3
"""
Trending Claude Skills Leaderboard
Fetches and displays the most popular claude-skill repositories from GitHub.
Falls back to mock data when no network/API key is available.
"""

import json
import sys
import os
from datetime import datetime, timezone
from typing import Optional

# Try to import requests; fall back gracefully
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

GITHUB_TOPICS = [
    "claude-skills",
    "claude-code",
    "mcp-server",
    "ai-agents",
    "coding-agent",
    "ai-workflow",
]

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"

MOCK_DATA = [
    {"full_name": "anthropics/claude-code", "description": "Claude Code - an agentic coding tool", "stargazers_count": 28500, "forks_count": 1820, "language": "TypeScript", "pushed_at": "2026-05-26T18:00:00Z", "html_url": "https://github.com/anthropics/claude-code", "topics": ["claude-code", "ai-agents"]},
    {"full_name": "modelcontextprotocol/servers", "description": "Reference MCP server implementations", "stargazers_count": 19200, "forks_count": 2100, "language": "TypeScript", "pushed_at": "2026-05-26T14:30:00Z", "html_url": "https://github.com/modelcontextprotocol/servers", "topics": ["mcp-server", "claude-code"]},
    {"full_name": "punkpeye/awesome-mcp-servers", "description": "Curated list of MCP servers", "stargazers_count": 12400, "forks_count": 890, "language": "Markdown", "pushed_at": "2026-05-25T22:00:00Z", "html_url": "https://github.com/punkpeye/awesome-mcp-servers", "topics": ["mcp-server", "ai-agents"]},
    {"full_name": "linny006/trending-claude-skills", "description": "Auto-updated leaderboard of trending claude-skills repos", "stargazers_count": 480, "forks_count": 62, "language": "Python", "pushed_at": "2026-05-27T01:15:00Z", "html_url": "https://github.com/linny006/trending-claude-skills", "topics": ["claude-skills", "ai-agents"]},
    {"full_name": "pcx-wave/skill-router", "description": "A meta-skill for Claude Code that routes to other skills", "stargazers_count": 310, "forks_count": 28, "language": "Python", "pushed_at": "2026-05-21T09:00:00Z", "html_url": "https://github.com/pcx-wave/skill-router", "topics": ["claude-skills", "claude-code"]},
    {"full_name": "lipefur/sprint-orchestrator", "description": "Portable multi-chat sprint orchestrator for Claude", "stargazers_count": 275, "forks_count": 34, "language": "Python", "pushed_at": "2026-05-21T11:00:00Z", "html_url": "https://github.com/lipefur/sprint-orchestrator", "topics": ["claude-skills", "ai-workflow"]},
    {"full_name": "nexu-io/html-anything", "description": "The agentic HTML editor", "stargazers_count": 245, "forks_count": 19, "language": "TypeScript", "pushed_at": "2026-05-15T16:00:00Z", "html_url": "https://github.com/nexu-io/html-anything", "topics": ["claude-skills", "coding-agent"]},
    {"full_name": "andyshaman/premortem", "description": "Premortem skill for Claude Code", "stargazers_count": 198, "forks_count": 15, "language": "Markdown", "pushed_at": "2026-05-10T08:00:00Z", "html_url": "https://github.com/andyshaman/premortem", "topics": ["claude-skills"]},
    {"full_name": "fourleafai/clover-public", "description": "Open source Claude skill for business intelligence", "stargazers_count": 165, "forks_count": 22, "language": "Python", "pushed_at": "2026-05-24T19:00:00Z", "html_url": "https://github.com/fourleafai/clover-public", "topics": ["claude-skills", "ai-workflow"]},
    {"full_name": "h4ckologic/bughunter-ai", "description": "Autonomous bug bounty hunting agent", "stargazers_count": 152, "forks_count": 31, "language": "Python", "pushed_at": "2026-05-15T12:00:00Z", "html_url": "https://github.com/h4ckologic/bughunter-ai", "topics": ["claude-skills", "ai-agents"]},
    {"full_name": "gusellerm/trustgraph-skill", "description": "Claude skill that maps trust graphs", "stargazers_count": 130, "forks_count": 10, "language": "Python", "pushed_at": "2026-05-22T07:00:00Z", "html_url": "https://github.com/gusellerm/trustgraph-skill", "topics": ["claude-skills"]},
    {"full_name": "001tmf/agentic-science", "description": "Skillpack for agentic scientific research", "stargazers_count": 115, "forks_count": 14, "language": "Python", "pushed_at": "2026-05-23T10:00:00Z", "html_url": "https://github.com/001tmf/agentic-science", "topics": ["claude-skills", "ai-workflow"]},
]


def fetch_github_repos(topic: str, token: Optional[str] = None, per_page: int = 10) -> list[dict]:
    """Fetch repos for a given GitHub topic, sorted by stars."""
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    params = {
        "q": f"topic:{topic}",
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }
    resp = requests.get(GITHUB_SEARCH_URL, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json().get("items", [])


def fetch_all_topics(token: Optional[str] = None, per_page: int = 10) -> list[dict]:
    """Fetch repos across all tracked topics, deduplicate by full_name."""
    seen = set()
    results = []
    for topic in GITHUB_TOPICS:
        try:
            repos = fetch_github_repos(topic, token=token, per_page=per_page)
            for r in repos:
                if r["full_name"] not in seen:
                    seen.add(r["full_name"])
                    results.append(r)
        except Exception as e:
            print(f"  [warn] Failed to fetch topic '{topic}': {e}", file=sys.stderr)
    return results


def days_ago(iso_date: str) -> int:
    """Return how many days ago an ISO date was."""
    dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
    delta = datetime.now(timezone.utc) - dt
    return max(0, delta.days)


def render_leaderboard(repos: list[dict], top_n: int = 20, source: str = "live") -> str:
    """Render a formatted leaderboard table."""
    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:top_n]

    lines = []
    lines.append("")
    lines.append("=" * 72)
    lines.append("  TRENDING CLAUDE SKILLS LEADERBOARD")
    lines.append(f"  Source: {source} | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("=" * 72)
    lines.append("")
    lines.append(f"  {'#':<4} {'Repository':<40} {'Stars':>7} {'Lang':<12} {'Active'}")
    lines.append(f"  {'─'*4} {'─'*40} {'─'*7} {'─'*12} {'─'*10}")

    for i, repo in enumerate(sorted_repos, 1):
        name = repo["full_name"]
        if len(name) > 38:
            name = name[:35] + "..."
        stars = repo.get("stargazers_count", 0)
        lang = (repo.get("language") or "?")[:10]
        pushed = repo.get("pushed_at", "")
        age = days_ago(pushed) if pushed else "?"
        active = f"{age}d ago" if isinstance(age, int) else "?"

        lines.append(f"  {i:<4} {name:<40} {stars:>7,} {lang:<12} {active}")

    lines.append("")
    lines.append(f"  Topics tracked: {', '.join(GITHUB_TOPICS)}")
    lines.append(f"  Total unique repos: {len(repos)}")
    lines.append("=" * 72)
    lines.append("")
    return "\n".join(lines)


def render_json(repos: list[dict], top_n: int = 20) -> str:
    """Render leaderboard as JSON."""
    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:top_n]
    output = []
    for r in sorted_repos:
        output.append({
            "repo": r["full_name"],
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "language": r.get("language"),
            "pushed_at": r.get("pushed_at"),
            "url": r.get("html_url", ""),
            "description": r.get("description", ""),
        })
    return json.dumps(output, indent=2)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Trending Claude Skills Leaderboard")
    parser.add_argument("--live", action="store_true", help="Fetch live data from GitHub API")
    parser.add_argument("--top", type=int, default=15, help="Number of repos to display (default: 15)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--topic", type=str, help="Filter to a single topic")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")

    if args.live:
        if not HAS_REQUESTS:
            print("Error: 'requests' package required for live mode. pip install requests", file=sys.stderr)
            sys.exit(1)
        print("Fetching live data from GitHub...", file=sys.stderr)
        if args.topic:
            repos = fetch_github_repos(args.topic, token=token, per_page=args.top)
        else:
            repos = fetch_all_topics(token=token, per_page=args.top)
        source = "GitHub API (live)"
    else:
        repos = MOCK_DATA
        if args.topic:
            repos = [r for r in repos if args.topic in r.get("topics", [])]
        source = "mock data (use --live for real results)"

    if not repos:
        print("No repos found.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(render_json(repos, top_n=args.top))
    else:
        print(render_leaderboard(repos, top_n=args.top, source=source))


if __name__ == "__main__":
    main()
