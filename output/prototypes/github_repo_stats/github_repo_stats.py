#!/usr/bin/env python3
"""
GitHub Repo Stats — fetch and display key metrics for any GitHub repository.

Usage:
    python3 github_repo_stats.py owner/repo
    python3 github_repo_stats.py https://github.com/owner/repo
    python3 github_repo_stats.py --mock          # demo with built-in mock data
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error


# ---------------------------------------------------------------------------
# Mock data for offline demo
# ---------------------------------------------------------------------------

MOCK_REPO = {
    "full_name": "simonw/datasette",
    "description": "An open source multi-tool for exploring and publishing data",
    "stargazers_count": 9842,
    "forks_count": 702,
    "open_issues_count": 318,
    "language": "Python",
    "license": {"spdx_id": "Apache-2.0"},
    "created_at": "2017-11-13T16:23:33Z",
    "pushed_at": "2026-05-06T09:14:22Z",
    "default_branch": "main",
    "archived": False,
    "size": 45320,
}

MOCK_COMMIT_COUNT = 4217

MOCK_LANGUAGES = {
    "Python": 1482360,
    "JavaScript": 119450,
    "HTML": 67200,
    "CSS": 24100,
    "Shell": 3200,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_repo_id(raw: str) -> tuple:
    """Extract (owner, repo) from a URL or 'owner/repo' string."""
    raw = raw.strip().rstrip("/")
    m = re.match(r"(?:https?://github\.com/)?([^/]+)/([^/?#]+)", raw)
    if not m:
        print(f"Error: cannot parse repo identifier: {raw}", file=sys.stderr)
        sys.exit(1)
    return m.group(1), m.group(2).removesuffix(".git")


def gh_request(url: str, method: str = "GET") -> tuple:
    """Make a GitHub API request. Returns (body_str, headers_dict)."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode() if method == "GET" else ""
            return body, dict(resp.headers)
    except urllib.error.HTTPError as e:
        print(f"GitHub API error: {e.code} {e.reason} — {url}", file=sys.stderr)
        sys.exit(1)


def get_commit_count(owner: str, repo: str) -> int:
    """Estimate total commits on default branch via Link header pagination."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=1"
    _, headers = gh_request(url, method="GET")
    link = headers.get("Link", "")
    m = re.search(r'page=(\d+)>;\s*rel="last"', link)
    if m:
        return int(m.group(1))
    # No Link header means <= 1 page; count directly
    body, _ = gh_request(
        f"https://api.github.com/repos/{owner}/{repo}/commits?per_page=100"
    )
    return len(json.loads(body))


def format_number(n: int) -> str:
    return f"{n:,}"


def language_breakdown(langs: dict) -> str:
    total = sum(langs.values())
    if total == 0:
        return "N/A"
    parts = []
    for lang, bytes_ in sorted(langs.items(), key=lambda x: -x[1]):
        pct = bytes_ / total * 100
        if pct >= 1.0:
            parts.append(f"{lang} {pct:.1f}%")
    return ", ".join(parts) if parts else "N/A"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(owner: str, repo: str, use_mock: bool = False):
    if use_mock:
        info = MOCK_REPO
        commits = MOCK_COMMIT_COUNT
        langs = MOCK_LANGUAGES
    else:
        # Fetch repo metadata
        body, _ = gh_request(f"https://api.github.com/repos/{owner}/{repo}")
        info = json.loads(body)

        # Fetch commit count
        commits = get_commit_count(owner, repo)

        # Fetch languages
        body, _ = gh_request(f"https://api.github.com/repos/{owner}/{repo}/languages")
        langs = json.loads(body)

    # Build table
    license_id = (info.get("license") or {}).get("spdx_id", "N/A")
    created = info["created_at"][:10]
    pushed = info["pushed_at"][:10]
    archived = "Yes" if info.get("archived") else "No"

    rows = [
        ("Description", info.get("description") or "N/A"),
        ("Stars", format_number(info["stargazers_count"])),
        ("Forks", format_number(info["forks_count"])),
        ("Total Commits", format_number(commits)),
        ("Open Issues", format_number(info["open_issues_count"])),
        ("Primary Language", info.get("language") or "N/A"),
        ("License", license_id),
        ("Created", created),
        ("Last Push", pushed),
        ("Size", f"{format_number(info['size'])} KB"),
        ("Archived", archived),
        ("Top Languages", language_breakdown(langs)),
    ]

    full_name = info.get("full_name", f"{owner}/{repo}")
    print(f"\n## {full_name}\n")
    print(f"| {'Metric':<18} | {'Value':<50} |")
    print(f"|{'-'*20}|{'-'*52}|")
    for label, value in rows:
        # Truncate very long values
        display = value if len(value) <= 50 else value[:47] + "..."
        print(f"| {label:<18} | {display:<50} |")
    print()


def main():
    use_mock = "--mock" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--mock"]

    if use_mock:
        owner, repo = "simonw", "datasette"
    elif args:
        owner, repo = parse_repo_id(args[0])
    else:
        print(__doc__.strip())
        sys.exit(1)

    run(owner, repo, use_mock=use_mock)


if __name__ == "__main__":
    main()
