#!/usr/bin/env python3
"""
Customer Request to Code Pipeline

Converts customer feature requests, bug reports, and support tickets into
structured implementation plans with generated code changes — no API keys needed.
"""

import json
import re
import sys
import textwrap
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from mock_codebase import CODEBASE, KEYWORD_FILE_MAP

# ── Data Models ──────────────────────────────────────────────────────────────

@dataclass
class CustomerRequest:
    id: str
    source: str
    customer: str
    title: str
    body: str
    priority_signals: dict
    submitted_at: str

    @property
    def request_type(self) -> str:
        body_lower = self.body.lower()
        title_lower = self.title.lower()
        combined = f"{title_lower} {body_lower}"
        if self.source == "bug_report" or any(w in combined for w in ["bug", "error", "broken", "wrong", "instead of"]):
            return "bug_fix"
        if any(w in combined for w in ["add", "new", "support", "need to"]):
            return "new_feature"
        return "improvement"


@dataclass
class ParsedRequest:
    request: CustomerRequest
    what: str
    why: str
    where: str
    complexity: str
    affected_files: list = field(default_factory=list)
    change_reasons: dict = field(default_factory=dict)


@dataclass
class ImplementationPlan:
    parsed: ParsedRequest
    steps: list = field(default_factory=list)
    tests: list = field(default_factory=list)
    risks: list = field(default_factory=list)
    generated_code: dict = field(default_factory=dict)
    priority_score: float = 0.0


# ── Step 1: Parse ────────────────────────────────────────────────────────────

def parse_request(req: CustomerRequest) -> ParsedRequest:
    """Extract structured info from raw customer input."""
    body = req.body
    title = req.title

    # Extract WHAT
    what = title

    # Extract WHY — look for reasoning patterns
    why_patterns = [
        r"(?:because|so that|need to|requires?|blocking)\s+(.+?)(?:\.|$)",
        r"(?:Our .+? (?:needs?|requires?|depends?))\s+(.+?)(?:\.|$)",
    ]
    why = ""
    for pat in why_patterns:
        m = re.search(pat, body, re.IGNORECASE)
        if m:
            why = m.group(0).strip().rstrip(".")
            break
    if not why:
        sentences = [s.strip() for s in body.split(".") if s.strip()]
        why = sentences[-1] if len(sentences) > 1 else sentences[0] if sentences else title

    # Extract WHERE — map to codebase
    combined = f"{title} {body}".lower()
    affected = set()
    for keyword, files in KEYWORD_FILE_MAP.items():
        if keyword in combined:
            affected.update(files)

    # Determine complexity
    if len(affected) <= 2:
        complexity = "small"
    elif len(affected) <= 4:
        complexity = "medium"
    else:
        complexity = "large"

    # Determine WHERE description
    if affected:
        primary = sorted(affected)[0]
        where = CODEBASE.get(primary, {}).get("description", primary)
    else:
        where = "Unknown — requires manual triage"

    # Build change reasons
    change_reasons = {}
    for f in sorted(affected):
        info = CODEBASE.get(f, {})
        desc = info.get("description", f)
        req_type = req.request_type
        if "test" in f:
            change_reasons[f] = f"Add test coverage for {what.lower()}"
        elif req_type == "bug_fix":
            change_reasons[f] = f"Fix: {desc.lower()} — correct behavior per customer report"
        elif req_type == "new_feature":
            change_reasons[f] = f"Add: new capability in {desc.lower()}"
        else:
            change_reasons[f] = f"Modify: {desc.lower()} to support request"

    return ParsedRequest(
        request=req,
        what=what,
        why=why,
        where=where,
        complexity=complexity,
        affected_files=sorted(affected),
        change_reasons=change_reasons,
    )


# ── Step 2: Prioritize ──────────────────────────────────────────────────────

def compute_priority(parsed: ParsedRequest) -> float:
    """Score 0-100 based on requesters, revenue, urgency, and complexity."""
    signals = parsed.request.priority_signals
    score = 0.0

    # Requesters (0-30)
    requesters = signals.get("requesters", 1)
    score += min(30, requesters * 2.5)

    # Revenue (0-35)
    rev_str = signals.get("revenue_impact", "$0")
    rev = float(re.sub(r"[^\d.]", "", rev_str.replace("k", "000").replace("K", "000")))
    score += min(35, rev / 20000)

    # Urgency (0-25)
    urgency_map = {"low": 5, "medium": 15, "high": 25}
    score += urgency_map.get(signals.get("urgency", "medium"), 15)

    # Complexity bonus — simpler = faster to ship (0-10)
    complexity_bonus = {"small": 10, "medium": 6, "large": 2}
    score += complexity_bonus.get(parsed.complexity, 5)

    return round(min(100, score), 1)


# ── Step 3: Generate Implementation Plan ─────────────────────────────────────

CODE_TEMPLATES = {
    "csv_export": '''\
# src/exporters/csv_export.py
import csv
import io
from typing import List, Dict

def export_to_csv(data: List[Dict], columns: List[str] | None = None) -> str:
    """Export analytics data to CSV format."""
    if not data:
        return ""
    columns = columns or list(data[0].keys())
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


# Add to src/api/routes.py:
# @app.get("/api/analytics/export")
# async def export_analytics(format: str = "csv"):
#     data = await get_dashboard_data()
#     if format == "csv":
#         csv_content = export_to_csv(data)
#         return Response(csv_content, media_type="text/csv",
#                         headers={"Content-Disposition": "attachment; filename=analytics.csv"})
''',

    "webhook_retry": '''\
# src/services/webhook_retry.py
import asyncio
import logging
from typing import Callable

logger = logging.getLogger(__name__)

async def deliver_with_retry(
    deliver_fn: Callable,
    payload: dict,
    endpoint: str,
    max_retries: int = 3,
    base_delay: float = 60.0,  # 1 minute
) -> bool:
    """Deliver webhook with exponential backoff retry."""
    for attempt in range(max_retries + 1):
        try:
            await deliver_fn(payload, endpoint)
            if attempt > 0:
                logger.info(f"Webhook delivered on retry {attempt} to {endpoint}")
            return True
        except Exception as e:
            if attempt == max_retries:
                logger.error(f"Webhook delivery failed after {max_retries} retries: {e}")
                return False
            delay = base_delay * (2 ** attempt)  # 60s, 120s, 240s
            logger.warning(f"Webhook attempt {attempt+1} failed, retrying in {delay}s: {e}")
            await asyncio.sleep(delay)
    return False
''',

    "search_cache_invalidation": '''\
# Patch for src/services/search.py — delete_from_index()
def delete_from_index(item_id: str) -> bool:
    """Delete item from search index and immediately invalidate cache."""
    success = _remove_from_index(item_id)
    if success:
        # Invalidate cached search results containing this item
        invalidate_cache(pattern=f"*item:{item_id}*")
        # Also invalidate any full-page result caches
        invalidate_cache(pattern="search:results:*")
    return success
''',

    "rbac_api_keys": '''\
# src/models/api_key.py — extended with RBAC
from enum import Flag, auto
from dataclasses import dataclass
import secrets
import hashlib

class Permission(Flag):
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    ADMIN = READ | WRITE | DELETE

ROLE_PRESETS = {
    "analytics": Permission.READ,
    "integration": Permission.READ | Permission.WRITE,
    "admin": Permission.ADMIN,
}

@dataclass
class ScopedApiKey:
    key_id: str
    key_hash: str
    permissions: Permission
    label: str
    created_by: str

    def has_permission(self, required: Permission) -> bool:
        return required in self.permissions

def generate_scoped_key(role: str, label: str, created_by: str) -> tuple:
    """Generate a new API key with role-based permissions."""
    raw_key = f"sk_{secrets.token_urlsafe(32)}"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    permissions = ROLE_PRESETS.get(role, Permission.READ)
    api_key = ScopedApiKey(
        key_id=raw_key[:12],
        key_hash=key_hash,
        permissions=permissions,
        label=label,
        created_by=created_by,
    )
    return raw_key, api_key
''',

    "rate_limit_fix": '''\
# Patch for src/api/middleware.py — check_rate_limit()
from starlette.responses import JSONResponse

async def check_rate_limit(request, call_next):
    """Rate limiting middleware — returns 429 (not 500) when limit exceeded."""
    client_ip = request.client.host
    limit_key = f"ratelimit:{client_ip}"

    current = await redis.incr(limit_key)
    if current == 1:
        await redis.expire(limit_key, 60)

    if current > RATE_LIMIT_PER_MINUTE:
        remaining = await redis.ttl(limit_key)
        return JSONResponse(
            status_code=429,  # Fixed: was incorrectly raising 500
            content={"error": "rate_limit_exceeded", "retry_after": remaining},
            headers={"Retry-After": str(remaining)},
        )

    response = await call_next(request)
    return response
''',
}

REQUEST_CODE_MAP = {
    "csv": "csv_export",
    "export": "csv_export",
    "webhook": "webhook_retry",
    "retry": "webhook_retry",
    "backoff": "webhook_retry",
    "search": "search_cache_invalidation",
    "stale": "search_cache_invalidation",
    "cache": "search_cache_invalidation",
    "delete": "search_cache_invalidation",
    "rbac": "rbac_api_keys",
    "role": "rbac_api_keys",
    "permission": "rbac_api_keys",
    "api key": "rbac_api_keys",
    "scoped": "rbac_api_keys",
    "rate limit": "rate_limit_fix",
    "429": "rate_limit_fix",
    "500": "rate_limit_fix",
}


def generate_plan(parsed: ParsedRequest) -> ImplementationPlan:
    """Create implementation plan with concrete steps and code."""
    req = parsed.request
    plan = ImplementationPlan(parsed=parsed)
    plan.priority_score = compute_priority(parsed)

    # Generate steps based on request type
    req_type = req.request_type
    if req_type == "bug_fix":
        plan.steps = [
            f"Reproduce the issue: {parsed.what.lower()}",
            f"Identify root cause in {', '.join(parsed.affected_files[:2])}",
            "Implement fix with minimal change footprint",
            "Add regression test to prevent recurrence",
            "Verify fix resolves original customer scenario",
        ]
    elif req_type == "new_feature":
        plan.steps = [
            f"Design API/interface for: {parsed.what.lower()}",
            f"Implement core logic in {parsed.affected_files[0] if parsed.affected_files else 'new module'}",
            "Wire into existing routes/services",
            "Add comprehensive test coverage",
            "Update API documentation",
        ]
    else:
        plan.steps = [
            f"Analyze current behavior of {parsed.where}",
            "Implement improvement with backward compatibility",
            "Add tests for new behavior",
            "Performance test if applicable",
        ]

    # Generate tests
    for f in parsed.affected_files:
        if "test" in f:
            plan.tests.append(f"Update existing tests in {f}")
        else:
            test_file = f.replace("src/", "tests/test_").replace("/", "_")
            plan.tests.append(f"Add test in {test_file} for {parsed.what.lower()}")

    # Assess risks
    if parsed.complexity == "large":
        plan.risks.append("Cross-cutting change — coordinate with multiple team owners")
    if "middleware" in " ".join(parsed.affected_files):
        plan.risks.append("Middleware change affects all API requests — requires load testing")
    if req_type == "bug_fix" and parsed.request.priority_signals.get("urgency") == "high":
        plan.risks.append("High-urgency fix — consider hotfix branch + expedited review")
    if any("model" in f for f in parsed.affected_files):
        plan.risks.append("Model change may require database migration")
    if not plan.risks:
        plan.risks.append("Low risk — isolated change with clear scope")

    # Map to code template
    combined = f"{req.title} {req.body}".lower()
    generated = {}
    for keyword, template_key in REQUEST_CODE_MAP.items():
        if keyword in combined and template_key not in generated:
            generated[template_key] = CODE_TEMPLATES[template_key]
    plan.generated_code = generated

    return plan


# ── Step 4: Render Output ────────────────────────────────────────────────────

COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "red": "\033[31m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_red": "\033[41m",
}

def c(text: str, *styles: str) -> str:
    codes = "".join(COLORS.get(s, "") for s in styles)
    return f"{codes}{text}{COLORS['reset']}"


def render_plan(plan: ImplementationPlan) -> str:
    """Render a full implementation plan as formatted text."""
    p = plan.parsed
    req = p.request
    lines = []

    # Header
    priority_color = "bg_green" if plan.priority_score >= 70 else "bg_yellow" if plan.priority_score >= 40 else "bg_red"
    type_label = req.request_type.replace("_", " ").upper()
    lines.append(c(f" {type_label} ", "bold", priority_color) + " " + c(req.id, "bold", "cyan") + " " + c(f"Priority: {plan.priority_score}/100", "bold"))
    lines.append(c(f"  Customer: {req.customer}", "dim") + "  " + c(f"Source: {req.source}", "dim"))
    lines.append("")

    # Request summary
    lines.append(c("## Request Summary", "bold", "blue"))
    lines.append(f"  {p.what}")
    lines.append("")
    lines.append(c("  WHY: ", "bold") + p.why)
    lines.append(c("  WHERE: ", "bold") + p.where)
    lines.append(c("  COMPLEXITY: ", "bold") + c(p.complexity.upper(), "yellow" if p.complexity != "small" else "green"))
    lines.append("")

    # Priority signals
    signals = req.priority_signals
    lines.append(c("## Priority Signals", "bold", "blue"))
    lines.append(f"  Requesters: {c(str(signals.get('requesters', '?')), 'bold')}")
    lines.append(f"  Revenue:    {c(signals.get('revenue_impact', '?'), 'bold')}")
    lines.append(f"  Urgency:    {c(signals.get('urgency', '?'), 'bold')}")
    lines.append("")

    # Affected files
    lines.append(c("## Affected Files", "bold", "blue"))
    for f in p.affected_files:
        reason = p.change_reasons.get(f, "")
        lines.append(f"  {c(f, 'cyan')} — {reason}")
    lines.append("")

    # Implementation steps
    lines.append(c("## Implementation Steps", "bold", "blue"))
    for i, step in enumerate(plan.steps, 1):
        lines.append(f"  {c(str(i) + '.', 'bold')} {step}")
    lines.append("")

    # Testing
    lines.append(c("## Testing Strategy", "bold", "blue"))
    for t in plan.tests:
        lines.append(f"  - {t}")
    lines.append("")

    # Risks
    lines.append(c("## Risks & Considerations", "bold", "blue"))
    for r in plan.risks:
        lines.append(f"  {c('!', 'bold', 'yellow')} {r}")
    lines.append("")

    # Generated code
    if plan.generated_code:
        lines.append(c("## Generated Code", "bold", "green"))
        for name, code in plan.generated_code.items():
            lines.append(c(f"  ── {name} ", "bold", "magenta") + c("─" * 50, "dim"))
            for line in code.strip().split("\n"):
                lines.append(f"  {c(line, 'dim')}")
            lines.append("")

    lines.append(c("─" * 72, "dim"))
    return "\n".join(lines)


def render_summary_table(plans: "list[ImplementationPlan]") -> str:
    """Render a priority-sorted summary table."""
    lines = []
    lines.append("")
    lines.append(c("=" * 72, "bold"))
    lines.append(c(" CUSTOMER REQUEST → CODE PIPELINE — TRIAGE SUMMARY", "bold", "cyan"))
    lines.append(c("=" * 72, "bold"))
    lines.append("")
    lines.append(c(f" {'ID':<10} {'PRI':>5}  {'TYPE':<14} {'COMPLEXITY':<10} {'CUSTOMER':<16} TITLE", "bold"))
    lines.append(c(" " + "─" * 70, "dim"))

    for plan in sorted(plans, key=lambda p: p.priority_score, reverse=True):
        req = plan.parsed.request
        pri = plan.priority_score
        pri_color = "green" if pri >= 70 else "yellow" if pri >= 40 else "red"
        type_label = req.request_type.replace("_", " ")
        lines.append(
            f" {c(req.id, 'cyan'):<22}"
            f" {c(f'{pri:>5.1f}', 'bold', pri_color)}"
            f"  {type_label:<14}"
            f" {c(plan.parsed.complexity, 'yellow' if plan.parsed.complexity != 'small' else 'green'):<22}"
            f" {req.customer:<16}"
            f" {req.title[:30]}"
        )

    lines.append("")
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "sample_requests.json"
    path = Path(input_file)
    if not path.exists():
        print(f"Error: {input_file} not found", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        raw_requests = json.load(f)

    requests = [CustomerRequest(**r) for r in raw_requests]

    # Pipeline: Parse → Prioritize → Plan → Render
    plans = []
    for req in requests:
        parsed = parse_request(req)
        plan = generate_plan(parsed)
        plans.append(plan)

    # Output summary table
    print(render_summary_table(plans))

    # Output each plan
    for plan in sorted(plans, key=lambda p: p.priority_score, reverse=True):
        print(render_plan(plan))
        print()

    # Write markdown output
    output_path = Path("output_plans.md")
    with open(output_path, "w") as f:
        f.write("# Customer Request → Code Pipeline Output\n\n")
        f.write(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n")
        f.write(f"## Triage Summary\n\n")
        f.write(f"| ID | Priority | Type | Complexity | Customer | Title |\n")
        f.write(f"|---|---|---|---|---|---|\n")
        for plan in sorted(plans, key=lambda p: p.priority_score, reverse=True):
            req = plan.parsed.request
            f.write(f"| {req.id} | {plan.priority_score} | {req.request_type} | {plan.parsed.complexity} | {req.customer} | {req.title} |\n")
        f.write("\n---\n\n")
        for plan in sorted(plans, key=lambda p: p.priority_score, reverse=True):
            p = plan.parsed
            req = p.request
            f.write(f"## {req.id}: {p.what}\n\n")
            f.write(f"**Customer:** {req.customer} | **Type:** {req.request_type} | **Priority:** {plan.priority_score}/100\n\n")
            f.write(f"**Why:** {p.why}\n\n")
            f.write(f"**Where:** {p.where}\n\n")
            f.write(f"### Affected Files\n\n")
            for af in p.affected_files:
                f.write(f"- `{af}` — {p.change_reasons.get(af, '')}\n")
            f.write(f"\n### Steps\n\n")
            for i, step in enumerate(plan.steps, 1):
                f.write(f"{i}. {step}\n")
            f.write(f"\n### Tests\n\n")
            for t in plan.tests:
                f.write(f"- {t}\n")
            f.write(f"\n### Risks\n\n")
            for r in plan.risks:
                f.write(f"- {r}\n")
            if plan.generated_code:
                f.write(f"\n### Generated Code\n\n")
                for name, code in plan.generated_code.items():
                    f.write(f"#### {name}\n\n```python\n{code.strip()}\n```\n\n")
            f.write("\n---\n\n")

    print(c(f"\n Markdown report saved to: {output_path}", "bold", "green"))
    print(c(f" Processed {len(plans)} customer requests", "bold"))
    print(c(f" Top priority: {sorted(plans, key=lambda p: p.priority_score, reverse=True)[0].parsed.request.id}", "bold", "cyan"))


if __name__ == "__main__":
    main()
