#!/usr/bin/env python3
"""
Super GEO & Agent Readiness Auditor
Audits a website (or mock site) for Generative Engine Optimization
and AI agent discoverability.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

@dataclass
class CheckResult:
    name: str
    passed: bool
    score: float          # 0-100
    detail: str
    recommendation: str = ""

@dataclass
class AuditReport:
    site_url: str
    checks: list = field(default_factory=list)

    @property
    def overall_score(self) -> float:
        if not self.checks:
            return 0.0
        return sum(c.score for c in self.checks) / len(self.checks)

    def summary_table(self) -> str:
        lines = []
        lines.append("")
        lines.append("=" * 72)
        lines.append(f"  GEO & Agent Readiness Audit  --  {self.site_url}")
        lines.append("=" * 72)
        lines.append(f"{'Check':<30} {'Score':>6}  {'Status':<6}  Detail")
        lines.append("-" * 72)
        for c in self.checks:
            status = "PASS" if c.passed else "FAIL"
            lines.append(f"{c.name:<30} {c.score:>5.0f}%  {status:<6}  {c.detail}")
        lines.append("-" * 72)
        lines.append(f"{'OVERALL':<30} {self.overall_score:>5.1f}%")
        lines.append("=" * 72)
        return "\n".join(lines)

    def recommendations(self) -> str:
        recs = [c for c in self.checks if not c.passed and c.recommendation]
        if not recs:
            return "\nNo critical recommendations -- site is well-optimized!\n"
        lines = ["\nRecommendations:"]
        for i, c in enumerate(recs, 1):
            lines.append(f"  {i}. [{c.name}] {c.recommendation}")
        return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Mock site loader  (reads from sample_site/ directory)
# ---------------------------------------------------------------------------

class MockSite:
    """Loads files from a local directory to simulate fetching a live site."""

    def __init__(self, root: str):
        self.root = Path(root)

    def get(self, path: str) -> Optional[str]:
        fp = self.root / path.lstrip("/")
        if fp.is_file():
            return fp.read_text()
        return None

    def exists(self, path: str) -> bool:
        return (self.root / path.lstrip("/")).is_file()


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_llms_txt(site: MockSite) -> CheckResult:
    content = site.get("/llms.txt")
    if content is None:
        return CheckResult("llms.txt", False, 0,
                           "Not found",
                           "Create /llms.txt with site summary, doc links, and API refs.")
    has_heading = content.startswith("#")
    has_links = bool(re.search(r'\[.*\]\(.*\)', content))
    has_description = ">" in content
    score = 40 + (20 if has_heading else 0) + (20 if has_links else 0) + (20 if has_description else 0)
    detail = f"Found ({len(content)} bytes)"
    if score < 100:
        detail += "; missing "
        missing = []
        if not has_heading:
            missing.append("heading")
        if not has_links:
            missing.append("doc links")
        if not has_description:
            missing.append("description block")
        detail += ", ".join(missing)
    return CheckResult("llms.txt", score >= 60, score, detail,
                        "Add heading, description, and doc links per llmstxt.org spec." if score < 100 else "")


def check_llms_full_txt(site: MockSite) -> CheckResult:
    content = site.get("/llms-full.txt")
    if content is None:
        return CheckResult("llms-full.txt", False, 0,
                           "Not found",
                           "Create /llms-full.txt with expanded content for deeper AI context.")
    score = min(100, 50 + len(content) // 100)
    return CheckResult("llms-full.txt", True, score, f"Found ({len(content)} bytes)")


def check_mcp_manifest(site: MockSite) -> CheckResult:
    content = site.get("/.well-known/mcp.json")
    if content is None:
        return CheckResult("MCP manifest", False, 0,
                           "/.well-known/mcp.json not found",
                           "Expose an MCP manifest at /.well-known/mcp.json with tool schemas.")
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return CheckResult("MCP manifest", False, 20, "Invalid JSON",
                           "Fix JSON syntax in /.well-known/mcp.json.")
    has_tools = "tools" in data
    has_name = "name" in data
    score = 40 + (30 if has_tools else 0) + (30 if has_name else 0)
    detail = f"Valid JSON; tools={'yes' if has_tools else 'no'}, name={'yes' if has_name else 'no'}"
    return CheckResult("MCP manifest", score >= 70, score, detail,
                        "Add 'tools' and 'name' fields." if score < 100 else "")


def check_schema_org(site: MockSite) -> CheckResult:
    html = site.get("/index.html")
    if html is None:
        return CheckResult("Schema.org markup", False, 0,
                           "No index.html found",
                           "Add JSON-LD structured data in <script type='application/ld+json'>.")
    ld_blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.DOTALL)
    if not ld_blocks:
        return CheckResult("Schema.org markup", False, 0,
                           "No JSON-LD blocks found",
                           "Add at least one JSON-LD block (Article, FAQPage, HowTo, or Product).")
    types_found = set()
    for block in ld_blocks:
        try:
            data = json.loads(block)
            t = data.get("@type", "")
            if isinstance(t, list):
                types_found.update(t)
            else:
                types_found.add(t)
        except json.JSONDecodeError:
            pass
    ai_useful = {"FAQPage", "HowTo", "Article", "Product", "Organization", "WebSite"}
    matched = types_found & ai_useful
    score = min(100, 30 + len(matched) * 20)
    detail = f"{len(ld_blocks)} JSON-LD block(s); types: {', '.join(types_found) or 'none parsed'}"
    return CheckResult("Schema.org markup", score >= 50, score, detail,
                        f"Add more AI-friendly types: {', '.join(ai_useful - matched)}" if score < 100 else "")


def check_robots_txt(site: MockSite) -> CheckResult:
    content = site.get("/robots.txt")
    if content is None:
        return CheckResult("robots.txt", False, 0,
                           "Not found",
                           "Create /robots.txt allowing GPTBot, PerplexityBot, Google-Extended.")
    ai_bots = ["GPTBot", "PerplexityBot", "Google-Extended", "ClaudeBot", "Amazonbot"]
    allowed = [b for b in ai_bots if b.lower() in content.lower() and "disallow" not in content.lower().split(b.lower())[0].split("\n")[-1]]
    # Simpler heuristic: check that bots are NOT disallowed
    blocked = []
    for bot in ai_bots:
        pattern = re.compile(rf'User-agent:\s*{re.escape(bot)}.*?Disallow:\s*/\s*$', re.MULTILINE | re.IGNORECASE)
        if pattern.search(content):
            blocked.append(bot)
    allowed_count = len(ai_bots) - len(blocked)
    score = int(allowed_count / len(ai_bots) * 100)
    detail = f"Blocked: {', '.join(blocked) if blocked else 'none'}"
    return CheckResult("robots.txt", score >= 60, score, detail,
                        f"Unblock: {', '.join(blocked)}" if blocked else "")


def check_oauth(site: MockSite) -> CheckResult:
    content = site.get("/.well-known/oauth-authorization-server")
    if content is None:
        return CheckResult("OAuth discovery", False, 0,
                           "/.well-known/oauth-authorization-server not found",
                           "Add OAuth 2.0 server metadata for secure agent auth.")
    try:
        data = json.loads(content)
        has_issuer = "issuer" in data
        has_endpoint = "authorization_endpoint" in data or "token_endpoint" in data
        score = 30 + (35 if has_issuer else 0) + (35 if has_endpoint else 0)
        detail = f"issuer={'yes' if has_issuer else 'no'}, endpoints={'yes' if has_endpoint else 'no'}"
        return CheckResult("OAuth discovery", score >= 65, score, detail)
    except json.JSONDecodeError:
        return CheckResult("OAuth discovery", False, 20, "Invalid JSON",
                           "Fix JSON in OAuth discovery document.")


def check_sitemap(site: MockSite) -> CheckResult:
    content = site.get("/sitemap.xml")
    if content is None:
        return CheckResult("sitemap.xml", False, 0,
                           "Not found",
                           "Create /sitemap.xml for content discovery by AI crawlers.")
    url_count = len(re.findall(r'<loc>', content))
    score = min(100, 50 + url_count * 10)
    return CheckResult("sitemap.xml", True, score, f"Found with {url_count} URL(s)")


def check_content_quality(site: MockSite) -> CheckResult:
    html = site.get("/index.html")
    if html is None:
        return CheckResult("Content quality", False, 0, "No index.html", "Create landing page.")
    score = 0
    details = []
    # Direct answers (sentences ending with period after a question-like heading)
    if re.search(r'<h[1-3]>.*\?</h[1-3]>', html):
        score += 25
        details.append("Q&A headings")
    # Lists
    if "<ul>" in html or "<ol>" in html:
        score += 25
        details.append("lists")
    # Tables
    if "<table>" in html:
        score += 25
        details.append("tables")
    # Citations / sources
    if re.search(r'(source|citation|according to|reference)', html, re.I):
        score += 25
        details.append("citations")
    detail = f"Signals: {', '.join(details)}" if details else "No AI-friendly content signals"
    return CheckResult("Content quality", score >= 50, score, detail,
                        "Add Q&A headings, lists, tables, and citations." if score < 100 else "")


# ---------------------------------------------------------------------------
# Generate sample llms.txt
# ---------------------------------------------------------------------------

def generate_llms_txt(site_name: str, description: str) -> str:
    return f"""# {site_name}
> {description}

## Docs
- [API Reference](/docs/api): Full API documentation
- [Getting Started](/docs/start): Quick start guide
- [Authentication](/docs/auth): OAuth and API key setup

## Optional
- [Examples](/examples): Code examples and tutorials
- [Changelog](/changelog): Version history and updates
"""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_audit(site_dir: str, site_url: str = "https://example.com") -> AuditReport:
    site = MockSite(site_dir)
    report = AuditReport(site_url=site_url)

    report.checks.append(check_llms_txt(site))
    report.checks.append(check_llms_full_txt(site))
    report.checks.append(check_mcp_manifest(site))
    report.checks.append(check_schema_org(site))
    report.checks.append(check_robots_txt(site))
    report.checks.append(check_oauth(site))
    report.checks.append(check_sitemap(site))
    report.checks.append(check_content_quality(site))

    return report


def main():
    site_dir = os.path.join(os.path.dirname(__file__), "sample_site")
    if len(sys.argv) > 1:
        site_dir = sys.argv[1]

    print("Super GEO & Agent Readiness Auditor")
    print(f"Scanning: {site_dir}\n")

    report = run_audit(site_dir, site_url="https://demo-saas.example.com")

    print(report.summary_table())
    print(report.recommendations())

    # Demo: generate llms.txt for a site that doesn't have one
    print("-" * 72)
    print("Generated llms.txt template:")
    print("-" * 72)
    print(generate_llms_txt("Demo SaaS App",
                            "A project management tool with REST API and AI integrations."))

    # Exit code: 0 if score >= 50, 1 otherwise
    sys.exit(0 if report.overall_score >= 50 else 1)


if __name__ == "__main__":
    main()
