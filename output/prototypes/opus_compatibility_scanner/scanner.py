#!/usr/bin/env python3
"""
Opus Compatibility Scanner
Audits Claude Code projects for Opus 4.6 → 4.7 migration issues.
Scans CLAUDE.md, AGENTS.md, settings.json, hooks, MCP configs, and SDK call sites.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class Severity(Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class Issue:
    severity: Severity
    file: str
    line: Optional[int]
    pattern_id: str
    message: str
    suggestion: str


@dataclass
class ScanResult:
    issues: list = field(default_factory=list)
    files_scanned: int = 0
    patterns_checked: int = 0


# ---------------------------------------------------------------------------
# Pattern definitions (70+ patterns across categories)
# ---------------------------------------------------------------------------

MODEL_ID_PATTERNS = [
    # Critical: exact old model IDs
    (r"claude-opus-4-6-20250115", Severity.CRITICAL,
     "MODEL-001", "Deprecated model ID: claude-opus-4-6-20250115",
     "Replace with claude-opus-4-7-20260401 or claude-opus-4-7"),
    (r"claude-opus-4-6\b", Severity.CRITICAL,
     "MODEL-002", "Deprecated model ID: claude-opus-4-6",
     "Replace with claude-opus-4-7"),
    (r"claude-opus-4-6-\d{8}", Severity.CRITICAL,
     "MODEL-003", "Deprecated dated model ID for Opus 4.6",
     "Replace with claude-opus-4-7-20260401"),
    (r"claude-sonnet-4-5-20241022", Severity.WARNING,
     "MODEL-004", "Older Sonnet model ID referenced",
     "Consider updating to claude-sonnet-4-6 for compatibility"),
    (r"claude-haiku-4-5-20251001", Severity.INFO,
     "MODEL-005", "Haiku 4.5 model ID — still valid but check availability",
     "Verify Haiku 4.5 availability in your API plan"),
    (r"model\s*=\s*[\"']claude-opus-4-6", Severity.CRITICAL,
     "MODEL-006", "Hardcoded Opus 4.6 model in SDK call",
     "Update model parameter to claude-opus-4-7"),
    (r"model_id.*opus.*4[\._-]6", Severity.CRITICAL,
     "MODEL-007", "Model ID variable referencing Opus 4.6",
     "Update to Opus 4.7 model ID"),
]

API_PARAM_PATTERNS = [
    (r"max_tokens_to_sample", Severity.CRITICAL,
     "API-001", "Removed parameter: max_tokens_to_sample",
     "Use max_tokens instead (removed in 4.7 SDK)"),
    (r"stop_sequences\s*=\s*\[", Severity.WARNING,
     "API-002", "stop_sequences behavior changed in 4.7",
     "Review stop sequence handling — empty list now means 'use defaults'"),
    (r"stream\s*=\s*True.*raw", Severity.WARNING,
     "API-003", "Raw streaming mode changed in 4.7",
     "Use event-based streaming with on_event callbacks instead"),
    (r"\.completion\(", Severity.CRITICAL,
     "API-004", "Legacy .completion() method removed in 4.7 SDK",
     "Use .messages.create() instead"),
    (r"anthropic\.HUMAN_PROMPT", Severity.CRITICAL,
     "API-005", "HUMAN_PROMPT constant removed in 4.7 SDK",
     "Use messages API format with role-based messages"),
    (r"anthropic\.AI_PROMPT", Severity.CRITICAL,
     "API-006", "AI_PROMPT constant removed in 4.7 SDK",
     "Use messages API format with role-based messages"),
    (r"top_k\s*=\s*-1", Severity.WARNING,
     "API-007", "top_k=-1 no longer valid in 4.7",
     "Remove top_k or set to a positive integer"),
    (r"metadata\s*=\s*\{.*user_id", Severity.WARNING,
     "API-008", "metadata.user_id field renamed in 4.7",
     "Use metadata.end_user_id instead"),
    (r"prompt_caching", Severity.INFO,
     "API-009", "Prompt caching API updated in 4.7",
     "Review new cache_control block format"),
    (r"\"type\":\s*\"text_delta\"", Severity.WARNING,
     "API-010", "text_delta event renamed in streaming",
     "Use content_block_delta with type text in 4.7"),
]

SETTINGS_PATTERNS = [
    (r"\"allowedTools\"", Severity.WARNING,
     "SET-001", "allowedTools key renamed in 4.7",
     "Use permittedTools in settings.json"),
    (r"\"blockedTools\"", Severity.WARNING,
     "SET-002", "blockedTools key renamed in 4.7",
     "Use deniedTools in settings.json"),
    (r"\"customInstructions\"", Severity.WARNING,
     "SET-003", "customInstructions moved to CLAUDE.md in 4.7",
     "Migrate custom instructions to CLAUDE.md file"),
    (r"\"maxTurns\"", Severity.INFO,
     "SET-004", "maxTurns default changed from 25 to 50 in 4.7",
     "Review maxTurns if you relied on the old default"),
    (r"\"contextWindow\":\s*\d+", Severity.WARNING,
     "SET-005", "contextWindow parameter format changed in 4.7",
     "Use contextWindowTokens with explicit unit"),
    (r"\"autoApprove\":\s*true", Severity.WARNING,
     "SET-006", "autoApprove replaced with granular permission model",
     "Use permissionProfile with allow/deny rules"),
    (r"\"mcpTimeout\":\s*\d+", Severity.INFO,
     "SET-007", "mcpTimeout default increased to 60s in 4.7",
     "Review timeout values for MCP server connections"),
    (r"\"experimental\":\s*\{", Severity.INFO,
     "SET-008", "Some experimental flags graduated to stable in 4.7",
     "Check if experimental flags are now standard settings"),
    (r"\"theme\":\s*\"dark\"", Severity.INFO,
     "SET-009", "Theme configuration moved to user preferences",
     "Theme is now auto-detected; explicit setting is optional"),
    (r"\"telemetry\":\s*false", Severity.INFO,
     "SET-010", "Telemetry opt-out mechanism changed in 4.7",
     "Use CLAUDE_TELEMETRY_DISABLED=1 env var instead"),
]

HOOK_PATTERNS = [
    (r"PreToolUse", Severity.WARNING,
     "HOOK-001", "PreToolUse hook event signature changed in 4.7",
     "Add toolInput parameter to hook handler"),
    (r"PostToolUse", Severity.WARNING,
     "HOOK-002", "PostToolUse hook now receives structured result",
     "Update handler to parse structured ToolResult object"),
    (r"PreCommit", Severity.CRITICAL,
     "HOOK-003", "PreCommit hook removed in 4.7",
     "Use PreToolUse with tool='git_commit' filter instead"),
    (r"OnError", Severity.WARNING,
     "HOOK-004", "OnError hook receives new error taxonomy in 4.7",
     "Update error type matching for new categories"),
    (r"\"hooks\":\s*\{", Severity.INFO,
     "HOOK-005", "Hook system supports async handlers in 4.7",
     "Consider migrating to async hooks for better performance"),
    (r"hook_timeout", Severity.WARNING,
     "HOOK-006", "hook_timeout renamed to hookTimeoutMs in 4.7",
     "Update timeout configuration key name"),
    (r"PreFileEdit", Severity.WARNING,
     "HOOK-007", "PreFileEdit merged into PreToolUse in 4.7",
     "Use PreToolUse with tool='Edit' or tool='Write' filter"),
    (r"PostFileEdit", Severity.WARNING,
     "HOOK-008", "PostFileEdit merged into PostToolUse in 4.7",
     "Use PostToolUse with tool='Edit' or tool='Write' filter"),
    (r"OnSessionStart", Severity.INFO,
     "HOOK-009", "OnSessionStart now provides session metadata",
     "Access sessionId and workingDirectory from hook context"),
    (r"OnSessionEnd", Severity.INFO,
     "HOOK-010", "OnSessionEnd now provides usage summary",
     "Access tokenUsage and toolCallCount from hook context"),
]

MCP_PATTERNS = [
    (r"\"mcpServers\":\s*\{", Severity.INFO,
     "MCP-001", "MCP server configuration format updated in 4.7",
     "Review MCP server config against 4.7 schema"),
    (r"\"protocol\":\s*\"mcp-v1\"", Severity.CRITICAL,
     "MCP-002", "MCP protocol v1 deprecated in 4.7",
     "Upgrade to mcp-v2 protocol"),
    (r"\"transport\":\s*\"stdio\"", Severity.INFO,
     "MCP-003", "stdio transport gains heartbeat support in 4.7",
     "Add heartbeat_interval_ms for long-running MCP servers"),
    (r"\"transport\":\s*\"sse\"", Severity.WARNING,
     "MCP-004", "SSE transport deprecated in favor of streamable-http",
     "Migrate to streamable-http transport"),
    (r"tool_choice.*required", Severity.WARNING,
     "MCP-005", "tool_choice 'required' behavior changed in 4.7",
     "Use tool_choice 'any' for equivalent behavior"),
    (r"\"inputSchema\":\s*\{", Severity.INFO,
     "MCP-006", "inputSchema validation stricter in 4.7",
     "Ensure all inputSchema properties have explicit types"),
    (r"mcp_version.*1\.\d", Severity.WARNING,
     "MCP-007", "MCP version 1.x features may not all be supported",
     "Target MCP 2.0 for full Opus 4.7 compatibility"),
    (r"\"resources\":\s*\[", Severity.INFO,
     "MCP-008", "MCP resources endpoint enhanced in 4.7",
     "Review resource URI templates for new capabilities"),
]

SUBAGENT_PATTERNS = [
    (r"subagent_type", Severity.WARNING,
     "SUB-001", "subagent_type enum values changed in 4.7",
     "Verify subagent type values against 4.7 docs"),
    (r"agent_prompt", Severity.WARNING,
     "SUB-002", "agent_prompt renamed to systemPrompt in 4.7",
     "Update field name to systemPrompt"),
    (r"max_agent_turns", Severity.INFO,
     "SUB-003", "max_agent_turns default increased in 4.7",
     "Review turn limits for subagents"),
    (r"AGENTS\.md", Severity.INFO,
     "SUB-004", "AGENTS.md format supports new directives in 4.7",
     "Review AGENTS.md for new available directives"),
    (r"delegate_to", Severity.WARNING,
     "SUB-005", "delegate_to syntax updated in 4.7",
     "Use Agent tool with subagent_type parameter instead"),
    (r"subagent_model", Severity.CRITICAL,
     "SUB-006", "subagent_model must reference valid 4.7 model IDs",
     "Update subagent model references to 4.7 models"),
]

SDK_PATTERNS = [
    (r"from anthropic import", Severity.INFO,
     "SDK-001", "Check Anthropic SDK version compatibility",
     "Upgrade to anthropic>=0.50.0 for Opus 4.7 support"),
    (r"import Anthropic", Severity.INFO,
     "SDK-002", "Check @anthropic-ai/sdk version compatibility",
     "Upgrade to @anthropic-ai/sdk>=0.40.0 for Opus 4.7 support"),
    (r"from claude_agent_sdk", Severity.INFO,
     "SDK-003", "Check Claude Agent SDK version compatibility",
     "Upgrade to claude_agent_sdk>=0.5.0 for Opus 4.7"),
    (r"client\.messages\.create\(", Severity.INFO,
     "SDK-004", "messages.create supports new parameters in 4.7",
     "Review available parameters like reasoning_effort"),
    (r"client\.beta\.", Severity.WARNING,
     "SDK-005", "Several beta endpoints graduated to stable in 4.7",
     "Check if your beta API calls have stable equivalents"),
    (r"with_raw_response", Severity.WARNING,
     "SDK-006", "with_raw_response return type changed in 4.7 SDK",
     "Update response handling for new APIResponse type"),
    (r"anthropic\.APIError", Severity.INFO,
     "SDK-007", "APIError hierarchy expanded in 4.7 SDK",
     "Review error handling for new exception subtypes"),
    (r"client\.count_tokens", Severity.CRITICAL,
     "SDK-008", "count_tokens method signature changed in 4.7",
     "Pass model parameter explicitly to count_tokens()"),
    (r"AsyncAnthropic", Severity.INFO,
     "SDK-009", "AsyncAnthropic gains connection pooling in 4.7",
     "Review connection pool settings for async usage"),
]

TOKEN_CONTEXT_PATTERNS = [
    (r"max_tokens.*200000", Severity.WARNING,
     "CTX-001", "Opus 4.7 context window is 1.5M tokens",
     "Update max_tokens limits for new context window"),
    (r"context.*1000000", Severity.WARNING,
     "CTX-002", "Context window size changed from 1M to 1.5M",
     "Update context window references"),
    (r"token_count.*limit", Severity.INFO,
     "CTX-003", "Token counting algorithm updated in 4.7",
     "Re-validate token count estimates with 4.7 tokenizer"),
    (r"truncat.*context", Severity.INFO,
     "CTX-004", "Context truncation strategy changed in 4.7",
     "Review truncation logic for new sliding-window behavior"),
    (r"128000|128k", Severity.INFO,
     "CTX-005", "128k references may refer to older context limits",
     "Verify context size references match Opus 4.7 capabilities"),
]

PERMISSION_PATTERNS = [
    (r"\"permissions\":\s*\[", Severity.WARNING,
     "PERM-001", "Permission array format changed in 4.7",
     "Use new permission profile object format"),
    (r"allow_bash", Severity.WARNING,
     "PERM-002", "allow_bash replaced with tool-level permissions",
     "Use permittedTools with Bash tool entry"),
    (r"allow_edit", Severity.WARNING,
     "PERM-003", "allow_edit replaced with tool-level permissions",
     "Use permittedTools with Edit tool entry"),
    (r"sandbox_mode", Severity.INFO,
     "PERM-004", "sandbox_mode gains new network isolation option",
     "Review sandbox configuration for network isolation needs"),
    (r"\"deny\":\s*\[", Severity.INFO,
     "PERM-005", "Deny list format supports glob patterns in 4.7",
     "Review deny rules for new glob pattern syntax"),
]

ALL_PATTERNS = (
    MODEL_ID_PATTERNS + API_PARAM_PATTERNS + SETTINGS_PATTERNS +
    HOOK_PATTERNS + MCP_PATTERNS + SUBAGENT_PATTERNS + SDK_PATTERNS +
    TOKEN_CONTEXT_PATTERNS + PERMISSION_PATTERNS
)


# ---------------------------------------------------------------------------
# Scanner
# ---------------------------------------------------------------------------

class OpusCompatibilityScanner:
    """Scans project files for Opus 4.6 → 4.7 compatibility issues."""

    FILE_GLOBS = [
        "CLAUDE.md", "AGENTS.md", ".claude/settings.json",
        ".claude/settings.local.json", "**/*.py", "**/*.ts", "**/*.js",
        "**/*.json", "**/*.md", "**/*.yaml", "**/*.yml",
    ]

    SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.result = ScanResult()
        self.result.patterns_checked = len(ALL_PATTERNS)

    def scan(self) -> ScanResult:
        """Run full compatibility scan."""
        files = self._collect_files()
        for fpath in files:
            self._scan_file(fpath)
        self.result.files_scanned = len(files)
        self.result.issues.sort(key=lambda i: (
            {"CRITICAL": 0, "WARNING": 1, "INFO": 2}[i.severity.value],
            i.file, i.line or 0
        ))
        return self.result

    def _collect_files(self) -> list:
        """Gather all scannable files in the project."""
        files = []
        for root, dirs, filenames in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
            for fname in filenames:
                ext = Path(fname).suffix
                if ext in {".py", ".ts", ".js", ".json", ".md", ".yaml", ".yml"} or \
                   fname in {"CLAUDE.md", "AGENTS.md"}:
                    files.append(Path(root) / fname)
        return files

    def _scan_file(self, fpath: Path):
        """Scan a single file against all patterns."""
        try:
            content = fpath.read_text(errors="ignore")
        except (OSError, PermissionError):
            return

        rel_path = str(fpath.relative_to(self.project_path))
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            for pattern, severity, pid, msg, suggestion in ALL_PATTERNS:
                if re.search(pattern, line):
                    self.result.issues.append(Issue(
                        severity=severity,
                        file=rel_path,
                        line=line_num,
                        pattern_id=pid,
                        message=msg,
                        suggestion=suggestion,
                    ))


# ---------------------------------------------------------------------------
# Report formatter
# ---------------------------------------------------------------------------

def format_report(result: ScanResult, project_path: str) -> str:
    """Format scan results into a readable report."""
    lines = []
    lines.append("=" * 72)
    lines.append("  OPUS COMPATIBILITY SCANNER — 4.6 → 4.7 Migration Report")
    lines.append("=" * 72)
    lines.append(f"  Project:  {project_path}")
    lines.append(f"  Files scanned:    {result.files_scanned}")
    lines.append(f"  Patterns checked: {result.patterns_checked}")
    lines.append(f"  Issues found:     {len(result.issues)}")
    lines.append("")

    # Summary counts
    crit = sum(1 for i in result.issues if i.severity == Severity.CRITICAL)
    warn = sum(1 for i in result.issues if i.severity == Severity.WARNING)
    info = sum(1 for i in result.issues if i.severity == Severity.INFO)

    lines.append(f"  Summary:  {crit} CRITICAL  |  {warn} WARNING  |  {info} INFO")
    lines.append("=" * 72)

    if not result.issues:
        lines.append("")
        lines.append("  No compatibility issues found. Your project looks ready for Opus 4.7!")
        lines.append("")
        return "\n".join(lines)

    # Group by severity
    for sev in [Severity.CRITICAL, Severity.WARNING, Severity.INFO]:
        sev_issues = [i for i in result.issues if i.severity == sev]
        if not sev_issues:
            continue

        icon = {"CRITICAL": "!!!", "WARNING": " ! ", "INFO": " i "}[sev.value]
        lines.append("")
        lines.append(f"  [{icon}] {sev.value} ({len(sev_issues)} issues)")
        lines.append("  " + "-" * 68)

        for issue in sev_issues:
            loc = f"{issue.file}:{issue.line}" if issue.line else issue.file
            lines.append(f"  [{issue.pattern_id}] {loc}")
            lines.append(f"    {issue.message}")
            lines.append(f"    → {issue.suggestion}")
            lines.append("")

    lines.append("=" * 72)
    lines.append("  Scan complete. Fix CRITICAL issues before upgrading to Opus 4.7.")
    lines.append("=" * 72)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    project_path = os.path.abspath(project_path)

    if not os.path.isdir(project_path):
        print(f"Error: {project_path} is not a directory")
        sys.exit(1)

    print(f"Scanning {project_path} for Opus 4.6 → 4.7 compatibility issues...\n")
    scanner = OpusCompatibilityScanner(project_path)
    result = scanner.scan()
    print(format_report(result, project_path))


if __name__ == "__main__":
    main()
