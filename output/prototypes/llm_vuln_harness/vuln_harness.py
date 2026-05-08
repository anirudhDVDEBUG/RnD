#!/usr/bin/env python3
"""
LLM Vulnerability Research Harness — Demo Scanner

Implements Mozilla's "Steer, Scale, Stack" methodology for automated
vulnerability discovery. This demo uses pattern-based heuristics to
simulate what Claude does when pointed at real C/C++ codebases.

In production, each analysis pass would be an LLM call with focused
prompts for specific vulnerability classes.
"""

import re
import sys
import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Optional


class Severity(Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class VulnClass(Enum):
    HEAP_BUFFER_OVERFLOW = "Heap Buffer Overflow"
    USE_AFTER_FREE = "Use-After-Free"
    DOUBLE_FREE = "Double Free"
    INTEGER_OVERFLOW = "Integer Overflow"
    FORMAT_STRING = "Format String"
    NULL_DEREF = "Null Pointer Dereference"
    TOCTOU = "TOCTOU Race Condition"
    OOB_READ = "Out-of-Bounds Read"
    UNTRUSTED_LENGTH = "Untrusted Length Field"


@dataclass
class Finding:
    vuln_class: str
    severity: str
    file: str
    line: int
    function: str
    description: str
    root_cause: str
    trigger: str
    suggested_fix: str
    mitigations: list = field(default_factory=list)
    pass_number: int = 1  # which analysis pass found it
    validated: bool = False


# ---------------------------------------------------------------------------
# STEER: vulnerability-class-specific detectors
# Each detector targets one class, mimicking a focused LLM prompt.
# ---------------------------------------------------------------------------

def detect_buffer_overflow(lines: list[str], filename: str) -> list[Finding]:
    """Pass 1: scan for unbounded copies into fixed buffers."""
    findings = []
    for i, line in enumerate(lines, 1):
        # Pattern: loop copying without bounds check near a fixed buffer
        if re.search(r'tag_name\[j\+\+\]\s*=', line):
            findings.append(Finding(
                vuln_class=VulnClass.HEAP_BUFFER_OVERFLOW.value,
                severity=Severity.CRITICAL.value,
                file=filename, line=i,
                function="parse_tag",
                description="Unbounded copy into fixed-size buffer tag_name[MAX_TAG_LEN]. "
                            "Loop copies from input until '>' without checking j < MAX_TAG_LEN.",
                root_cause="Missing bounds check on destination index j against MAX_TAG_LEN (64).",
                trigger="Send a tag with name longer than 64 bytes: '<' + 'A'*200 + '>'",
                suggested_fix="Add `&& j < MAX_TAG_LEN - 1` to the while condition.",
            ))
    return findings


def detect_use_after_free(lines: list[str], filename: str) -> list[Finding]:
    """Pass 1: detect access to freed memory."""
    findings = []
    in_function = None
    freed_vars = set()

    for i, line in enumerate(lines, 1):
        # Track function context
        func_match = re.search(r'(?:void|int|char)\s+(\w+)\s*\(', line)
        if func_match:
            in_function = func_match.group(1)
            freed_vars = set()

        # Track free/release calls
        release_match = re.search(r'(?:free|release_attribute)\s*\(\s*(\w+)\s*\)', line)
        if release_match:
            freed_vars.add(release_match.group(1))

        # Check for use of freed variable
        for var in list(freed_vars):
            if var in line and 'free' not in line and 'release' not in line:
                if re.search(rf'{var}\s*->', line):
                    findings.append(Finding(
                        vuln_class=VulnClass.USE_AFTER_FREE.value,
                        severity=Severity.CRITICAL.value,
                        file=filename, line=i,
                        function=in_function or "unknown",
                        description=f"Variable '{var}' accessed after being freed/released. "
                                    f"Dereferencing freed memory leads to UAF.",
                        root_cause=f"release_attribute() frees '{var}', but subsequent "
                                   f"code still dereferences {var}->value.",
                        trigger="Call process_attributes() with any input — the freed "
                                "pointer is always dereferenced.",
                        suggested_fix=f"Move the printf before release_attribute(), "
                                      f"or copy the value before releasing.",
                    ))
                    freed_vars.discard(var)  # report once
    return findings


def detect_integer_overflow(lines: list[str], filename: str) -> list[Finding]:
    """Pass 1: detect unchecked arithmetic used in allocations."""
    findings = []
    for i, line in enumerate(lines, 1):
        if re.search(r'=\s*\w+\s*\*\s*\w+', line) and ('unsigned' not in lines[i-2] if i > 2 else True):
            # Check if result feeds into malloc
            for j in range(i, min(i + 3, len(lines))):
                if 'malloc' in lines[j - 1] and 'total' in lines[j - 1]:
                    findings.append(Finding(
                        vuln_class=VulnClass.INTEGER_OVERFLOW.value,
                        severity=Severity.HIGH.value,
                        file=filename, line=i,
                        function="allocate_buffer",
                        description="Multiplication of unsigned ints can wrap to a small value. "
                                    "malloc() allocates a tiny buffer, memset overflows it.",
                        root_cause="count * element_size overflows for large inputs "
                                   "(e.g., count=0x10000, element_size=0x10000).",
                        trigger="Call allocate_buffer(0x10000, 0x10000) — total wraps to 0, "
                                "malloc(0) succeeds, memset writes to undersized buffer.",
                        suggested_fix="Check for overflow: if (element_size && count > SIZE_MAX / element_size) return NULL;",
                    ))
                    break
    return findings


def detect_double_free(lines: list[str], filename: str) -> list[Finding]:
    """Pass 1: detect double-free on error paths."""
    findings = []
    in_function = None
    free_sites = {}  # var -> line number of first free

    for i, line in enumerate(lines, 1):
        func_match = re.search(r'(?:void|int|char)\s+(\w+)\s*\(', line)
        if func_match:
            in_function = func_match.group(1)
            free_sites = {}

        free_match = re.search(r'free\s*\(\s*(\w+)\s*\)', line)
        if free_match:
            var = free_match.group(1)
            if var in free_sites:
                findings.append(Finding(
                    vuln_class=VulnClass.DOUBLE_FREE.value,
                    severity=Severity.HIGH.value,
                    file=filename, line=i,
                    function=in_function or "unknown",
                    description=f"'{var}' freed at line {free_sites[var]} and again at line {i}. "
                                f"Error path falls through to second free().",
                    root_cause="When parse_tag() fails, working_copy is freed in the error "
                               "handler but execution continues to the second free().",
                    trigger="Pass input that doesn't start with '<' to parse_document().",
                    suggested_fix="Add `return -1;` after the free in the error handler, "
                                  "or set working_copy = NULL after freeing.",
                ))
            else:
                free_sites[var] = i
    return findings


def detect_untrusted_length(lines: list[str], filename: str) -> list[Finding]:
    """Pass 1: detect use of attacker-controlled length in memcpy."""
    findings = []
    for i, line in enumerate(lines, 1):
        if 'payload_len' in line and 'memcpy' in line:
            findings.append(Finding(
                vuln_class=VulnClass.OOB_READ.value,
                severity=Severity.CRITICAL.value,
                file=filename, line=i,
                function="handle_message",
                description="memcpy uses msg->payload_len from untrusted input without "
                            "validating it against actual received data length (raw_len).",
                root_cause="payload_len is read from the wire and used directly as "
                           "the copy size. Attacker sets payload_len > raw_len.",
                trigger="Send a message with payload_len=0xFFFF but only 8 bytes of actual data.",
                suggested_fix="Validate: if (sizeof(uint32_t)*2 + msg->payload_len > raw_len) return -1;",
            ))
    return findings


def detect_format_string(lines: list[str], filename: str) -> list[Finding]:
    """Pass 1: detect format string vulnerabilities."""
    findings = []
    for i, line in enumerate(lines, 1):
        # snprintf with user data as format
        if re.search(r'snprintf\s*\(\s*\w+\s*,\s*[^,]+,\s*\w*user\w*', line, re.IGNORECASE):
            findings.append(Finding(
                vuln_class=VulnClass.FORMAT_STRING.value,
                severity=Severity.HIGH.value,
                file=filename, line=i,
                function="log_message",
                description="User-controlled string passed directly as format argument "
                            "to snprintf(). Attacker can read stack or cause crashes.",
                root_cause="user_data is used as the format string instead of being "
                           "passed as an argument: snprintf(buf, sz, user_data) vs "
                           'snprintf(buf, sz, "%s", user_data).',
                trigger='Call log_message("%x%x%x%x") to leak stack contents.',
                suggested_fix='Change to: snprintf(log_buf, sizeof(log_buf), "%s", user_data);',
            ))
    return findings


def detect_null_deref(lines: list[str], filename: str) -> list[Finding]:
    """Pass 1: detect missing NULL checks after malloc."""
    findings = []
    for i, line in enumerate(lines, 1):
        malloc_match = re.search(r'(\w+)\s*=.*malloc\s*\(', line)
        if malloc_match:
            var = malloc_match.group(1)
            # Check next 2 lines for NULL check
            has_check = False
            for j in range(i, min(i + 3, len(lines))):
                if f'!{var}' in lines[j - 1] or f'{var} == NULL' in lines[j - 1] or f'{var} ==' in lines[j - 1]:
                    has_check = True
                    break
            if not has_check:
                # Check if var is dereferenced immediately
                for j in range(i + 1, min(i + 3, len(lines) + 1)):
                    if j <= len(lines) and re.search(rf'{var}\s*->', lines[j - 1]):
                        findings.append(Finding(
                            vuln_class=VulnClass.NULL_DEREF.value,
                            severity=Severity.MEDIUM.value,
                            file=filename, line=j,
                            function="create_channel",
                            description=f"'{var}' from malloc() dereferenced without NULL check. "
                                        f"If allocation fails, this is a NULL pointer dereference.",
                            root_cause="malloc() can return NULL under memory pressure. "
                                       "The code immediately dereferences without checking.",
                            trigger="Trigger under low-memory conditions or with ulimit -v.",
                            suggested_fix=f"Add: if (!{var}) return NULL; after the malloc call.",
                            mitigations=["Most modern allocators overcommit, making this hard to trigger"],
                        ))
                        break
    return findings


def detect_toctou(lines: list[str], filename: str) -> list[Finding]:
    """Pass 1: detect TOCTOU race conditions."""
    findings = []
    for i, line in enumerate(lines, 1):
        if 'global_auth_flag' in line and 'if' in line:
            # Check if there's a second check on a different variable
            for j in range(i + 1, min(i + 5, len(lines) + 1)):
                if j <= len(lines) and 'authenticated' in lines[j - 1] and 'if' in lines[j - 1]:
                    findings.append(Finding(
                        vuln_class=VulnClass.TOCTOU.value,
                        severity=Severity.MEDIUM.value,
                        file=filename, line=i,
                        function="privileged_action",
                        description="Two-step auth check: global_auth_flag then chan->authenticated. "
                                    "Window between checks allows race condition.",
                        root_cause="global_auth_flag is shared mutable state. Another thread "
                                   "can modify it between the two if-checks.",
                        trigger="Thread A: call authenticate() then privileged_action(). "
                                "Thread B: reset global_auth_flag between the two checks.",
                        suggested_fix="Use a mutex to protect the check-then-act sequence, "
                                      "or use atomic operations with a single auth variable.",
                    ))
                    break
    return findings


# ---------------------------------------------------------------------------
# SCALE: chunk the codebase and run all detectors
# ---------------------------------------------------------------------------

ALL_DETECTORS = [
    detect_buffer_overflow,
    detect_use_after_free,
    detect_integer_overflow,
    detect_double_free,
    detect_untrusted_length,
    detect_format_string,
    detect_null_deref,
    detect_toctou,
]


def scan_file(filepath: Path) -> list[Finding]:
    """Run all detectors on a single file (one 'chunk')."""
    content = filepath.read_text()
    lines = content.splitlines()
    findings = []
    for detector in ALL_DETECTORS:
        findings.extend(detector(lines, str(filepath)))
    return findings


def scan_directory(target_dir: Path) -> list[Finding]:
    """SCALE: iterate over all C/C++ files in the target."""
    all_findings = []
    patterns = ["*.c", "*.cc", "*.cpp", "*.h", "*.hpp"]
    for pattern in patterns:
        for filepath in sorted(target_dir.rglob(pattern)):
            file_findings = scan_file(filepath)
            all_findings.extend(file_findings)
    return all_findings


# ---------------------------------------------------------------------------
# STACK: multi-pass validation
# ---------------------------------------------------------------------------

def validate_findings(findings: list[Finding]) -> list[Finding]:
    """
    Pass 2: validate and filter findings.
    In production, this would be a second LLM call asking Claude to
    verify reachability and exploitability of each candidate.
    Here we simulate by marking high-confidence patterns as validated.
    """
    for f in findings:
        # Simulate validation — in production, Claude traces code paths
        if f.severity in ("Critical", "High"):
            f.validated = True
            f.pass_number = 2
        elif f.severity == "Medium":
            f.validated = True
            f.pass_number = 2
            f.mitigations.append("Requires specific conditions to trigger")
    return [f for f in findings if f.validated]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def run_harness(target_dir: str, output_format: str = "text") -> list[Finding]:
    """
    Full steer/scale/stack pipeline.
    Returns validated findings list.
    """
    target = Path(target_dir)
    if not target.is_dir():
        print(f"Error: {target_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Pass 1: broad scan
    raw_findings = scan_directory(target)

    # Pass 2: validate
    validated = validate_findings(raw_findings)

    return validated


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sample_targets"
    fmt = sys.argv[2] if len(sys.argv) > 2 else "text"
    findings = run_harness(target, fmt)

    if fmt == "json":
        print(json.dumps([asdict(f) for f in findings], indent=2))
    else:
        # text output handled by report_generator
        from report_generator import print_report
        print_report(findings)
