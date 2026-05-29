"""
prompt_cache_analyzer.py — Analyzes LLM agent configurations for prompt-caching issues
and applies optimizations to reduce token costs by 50-80%.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CacheIssue:
    severity: str  # "high", "medium", "low"
    location: str
    description: str
    fix: str


@dataclass
class AnalysisResult:
    harness: str
    issues: list = field(default_factory=list)
    estimated_savings_pct: float = 0.0
    cache_eligible_tokens: int = 0
    total_tokens: int = 0


# ---------------------------------------------------------------------------
# Pattern detectors
# ---------------------------------------------------------------------------

_DYNAMIC_PATTERNS = [
    (re.compile(r"\{timestamp\}|\{now\}|\{date\}|datetime\.now|Date\.now", re.I),
     "Dynamic timestamp in cached prefix"),
    (re.compile(r"\{uuid\}|\{request_id\}|uuid4|uuidv4|nanoid", re.I),
     "Random ID in cached prefix"),
    (re.compile(r"\{session_id\}|\{run_id\}", re.I),
     "Session-specific ID in cached prefix"),
]

_MIN_CACHE_TOKENS = {
    "claude-3-5": 1024,
    "claude-3-opus": 2048,
    "claude-3-haiku": 1024,
    "claude-4": 1024,
    "default": 1024,
}


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English."""
    return max(1, len(text) // 4)


def detect_dynamic_content(text: str, location: str = "system_prompt") -> list[CacheIssue]:
    issues = []
    for pattern, desc in _DYNAMIC_PATTERNS:
        if pattern.search(text):
            issues.append(CacheIssue(
                severity="high",
                location=location,
                description=desc,
                fix=f"Move dynamic element out of the cached prefix into the final user message or a non-cached block.",
            ))
    return issues


def check_message_ordering(messages: list[dict]) -> list[CacheIssue]:
    """Verify cacheable content comes before dynamic content."""
    issues = []
    saw_user = False
    for i, msg in enumerate(messages):
        role = msg.get("role", "")
        if role == "user":
            saw_user = True
        if role == "system" and saw_user:
            issues.append(CacheIssue(
                severity="high",
                location=f"messages[{i}]",
                description="System message appears after user message — breaks prefix caching.",
                fix="Move all system messages before user messages: system -> tools -> history -> user.",
            ))
    return issues


def check_cache_breakpoints(messages: list[dict]) -> list[CacheIssue]:
    """Check if explicit cache_control breakpoints are set."""
    issues = []
    has_breakpoint = False
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and "cache_control" in block:
                    has_breakpoint = True
        elif isinstance(msg, dict) and "cache_control" in msg:
            has_breakpoint = True

    if not has_breakpoint and len(messages) > 1:
        issues.append(CacheIssue(
            severity="medium",
            location="messages",
            description="No explicit cache_control breakpoints found.",
            fix='Add {"cache_control": {"type": "ephemeral"}} after system prompt and tool definitions.',
        ))
    return issues


def check_prefix_stability(system_prompt: str) -> list[CacheIssue]:
    """Check if system prompt is stable across requests."""
    issues = detect_dynamic_content(system_prompt, "system_prompt")

    tokens = estimate_tokens(system_prompt)
    if tokens < _MIN_CACHE_TOKENS["default"]:
        issues.append(CacheIssue(
            severity="medium",
            location="system_prompt",
            description=f"System prompt is only ~{tokens} tokens. Minimum for caching is 1,024.",
            fix="Combine system prompt with tool definitions to exceed the 1,024-token minimum.",
        ))
    return issues


# ---------------------------------------------------------------------------
# Harness-specific analyzers
# ---------------------------------------------------------------------------

def analyze_claude_code_config(config: dict) -> AnalysisResult:
    result = AnalysisResult(harness="Claude Code")
    system = config.get("system_prompt", "")
    messages = config.get("messages", [])
    tools = config.get("tools", [])

    result.total_tokens = estimate_tokens(system) + sum(
        estimate_tokens(json.dumps(m)) for m in messages
    ) + sum(estimate_tokens(json.dumps(t)) for t in tools)

    result.issues.extend(check_prefix_stability(system))
    result.issues.extend(check_message_ordering(messages))
    result.issues.extend(check_cache_breakpoints(messages))

    # Check CLAUDE.md references
    if "CLAUDE.md" in system and "{" in system:
        result.issues.append(CacheIssue(
            severity="medium",
            location="system_prompt (CLAUDE.md)",
            description="CLAUDE.md content may be interpolated with dynamic values, busting cache.",
            fix="Keep CLAUDE.md content static. Move dynamic project state to a separate non-cached context block.",
        ))

    cacheable = estimate_tokens(system) + sum(estimate_tokens(json.dumps(t)) for t in tools)
    result.cache_eligible_tokens = cacheable
    high_issues = sum(1 for i in result.issues if i.severity == "high")
    if high_issues == 0:
        result.estimated_savings_pct = min(80.0, (cacheable / max(1, result.total_tokens)) * 90)
    else:
        result.estimated_savings_pct = 0.0

    return result


def analyze_aider_config(config: dict) -> AnalysisResult:
    result = AnalysisResult(harness="Aider")
    system = config.get("system_prompt", "")
    messages = config.get("messages", [])
    repo_map = config.get("repo_map", "")

    result.total_tokens = estimate_tokens(system) + estimate_tokens(repo_map) + sum(
        estimate_tokens(json.dumps(m)) for m in messages
    )

    result.issues.extend(check_prefix_stability(system))
    result.issues.extend(check_message_ordering(messages))

    if repo_map:
        repo_tokens = estimate_tokens(repo_map)
        if repo_tokens > 500:
            result.issues.append(CacheIssue(
                severity="medium",
                location="repo_map",
                description=f"Repo map (~{repo_tokens} tokens) changes between requests, busting cache.",
                fix="Pin repo map content and only update it when files actually change. Place it after the system prompt in a cached block.",
            ))

    cacheable = estimate_tokens(system)
    result.cache_eligible_tokens = cacheable
    high_issues = sum(1 for i in result.issues if i.severity == "high")
    result.estimated_savings_pct = 0.0 if high_issues else min(70.0, (cacheable / max(1, result.total_tokens)) * 90)
    return result


def analyze_generic_config(config: dict) -> AnalysisResult:
    result = AnalysisResult(harness="Generic Agent")
    system = config.get("system_prompt", "")
    messages = config.get("messages", [])

    result.total_tokens = estimate_tokens(system) + sum(
        estimate_tokens(json.dumps(m)) for m in messages
    )

    result.issues.extend(check_prefix_stability(system))
    result.issues.extend(check_message_ordering(messages))
    result.issues.extend(check_cache_breakpoints(messages))

    cacheable = estimate_tokens(system)
    result.cache_eligible_tokens = cacheable
    high_issues = sum(1 for i in result.issues if i.severity == "high")
    result.estimated_savings_pct = 0.0 if high_issues else min(75.0, (cacheable / max(1, result.total_tokens)) * 90)
    return result


# ---------------------------------------------------------------------------
# Optimizer — applies fixes to a config
# ---------------------------------------------------------------------------

def optimize_config(config: dict, harness: str = "generic") -> dict:
    """Return a patched copy of the config with cache optimizations applied."""
    import copy
    patched = copy.deepcopy(config)

    # 1. Remove dynamic content from system prompt
    system = patched.get("system_prompt", "")
    dynamic_removals = []
    for pattern, desc in _DYNAMIC_PATTERNS:
        matches = pattern.findall(system)
        if matches:
            dynamic_removals.extend(matches)
            system = pattern.sub("[MOVED_TO_USER_CONTEXT]", system)
    patched["system_prompt"] = system

    # 2. Reorder messages: system first, then assistant/tool, then user
    messages = patched.get("messages", [])
    system_msgs = [m for m in messages if m.get("role") == "system"]
    other_msgs = [m for m in messages if m.get("role") != "system"]
    patched["messages"] = system_msgs + other_msgs

    # 3. Add cache_control breakpoints
    if messages:
        # Add breakpoint to last system message
        for msg in reversed(patched["messages"]):
            if msg.get("role") == "system":
                if isinstance(msg.get("content"), str):
                    msg["content"] = [
                        {"type": "text", "text": msg["content"],
                         "cache_control": {"type": "ephemeral"}}
                    ]
                break

    # 4. Add breakpoint after tools
    tools = patched.get("tools", [])
    if tools:
        patched["_cache_after_tools"] = True

    patched["_optimized"] = True
    patched["_dynamic_elements_moved"] = dynamic_removals
    return patched


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze(config: dict, harness: str = "auto") -> AnalysisResult:
    if harness == "auto":
        if "CLAUDE.md" in json.dumps(config) or config.get("harness") == "claude_code":
            harness = "claude_code"
        elif "repo_map" in config or config.get("harness") == "aider":
            harness = "aider"
        else:
            harness = "generic"

    analyzers = {
        "claude_code": analyze_claude_code_config,
        "aider": analyze_aider_config,
        "generic": analyze_generic_config,
    }
    return analyzers.get(harness, analyze_generic_config)(config)


def format_report(result: AnalysisResult) -> str:
    lines = []
    lines.append(f"{'='*60}")
    lines.append(f"  Prompt Cache Analysis: {result.harness}")
    lines.append(f"{'='*60}")
    lines.append(f"  Total tokens (est.):          {result.total_tokens:,}")
    lines.append(f"  Cache-eligible tokens (est.):  {result.cache_eligible_tokens:,}")
    lines.append(f"  Estimated savings:             {result.estimated_savings_pct:.0f}%")
    lines.append(f"  Issues found:                  {len(result.issues)}")
    lines.append(f"{'='*60}")

    if result.issues:
        lines.append("")
        for i, issue in enumerate(result.issues, 1):
            icon = {"high": "[!]", "medium": "[~]", "low": "[.]"}[issue.severity]
            lines.append(f"  {icon} Issue #{i} ({issue.severity.upper()}) — {issue.location}")
            lines.append(f"      {issue.description}")
            lines.append(f"      Fix: {issue.fix}")
            lines.append("")
    else:
        lines.append("\n  No issues found. Caching looks healthy!\n")

    if result.estimated_savings_pct > 0:
        lines.append(f"  -> After fixes, expect ~{result.estimated_savings_pct:.0f}% cost reduction on cached turns.")
    else:
        lines.append(f"  -> Fix HIGH-severity issues above to unlock caching savings.")

    lines.append(f"{'='*60}")
    return "\n".join(lines)
