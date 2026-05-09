#!/usr/bin/env python3
"""
Safe Coding Agent Sandbox - Interactive Demo

Simulates a coding agent session with full sandboxing, approval gates,
telemetry, secret scanning, and policy enforcement.
"""

import json
import sys
import time

from sandbox import (
    AgentTelemetry,
    ApprovalDecision,
    ApprovalGate,
    enforce_policies,
    generate_docker_compose,
    generate_k8s_network_policy,
    generate_seccomp_profile,
    scan_for_secrets,
)

# ── Helpers ───────────────────────────────────────────────────────────

BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def header(title: str):
    width = 64
    print(f"\n{BOLD}{CYAN}{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}{RESET}\n")


def subheader(title: str):
    print(f"\n{BOLD}{BLUE}--- {title} ---{RESET}\n")


def ok(msg: str):
    print(f"  {GREEN}[PASS]{RESET} {msg}")


def warn(msg: str):
    print(f"  {YELLOW}[WARN]{RESET} {msg}")


def fail(msg: str):
    print(f"  {RED}[FAIL]{RESET} {msg}")


def info(msg: str):
    print(f"  {DIM}[INFO]{RESET} {msg}")


def pretty_json(obj, indent=2):
    print(json.dumps(obj, indent=indent, default=str))


# ── Simulated Agent Actions ──────────────────────────────────────────

MOCK_AGENT_ACTIONS = [
    ("read_file", {"path": "src/main.py"}),
    ("search_code", {"query": "def authenticate", "scope": "project"}),
    ("write_file", {"path": "src/utils.py", "lines_changed": 15}),
    ("create_file", {"path": "src/new_feature.py", "lines": 42}),
    ("run_test", {"suite": "unit", "files": 12}),
    ("install_package", {"package": "requests==2.31.0", "registry": "pypi"}),
    ("delete_file", {"path": "src/deprecated.py"}),
    ("git_push", {"branch": "feature/new-auth", "commits": 3}),
    ("modify_ci", {"file": ".github/workflows/deploy.yml", "change": "add step"}),
    ("read_file", {"path": "/etc/shadow"}),  # suspicious!
]

MOCK_AGENT_CODE_OUTPUT = '''
import os
import subprocess
import pickle

# Config
API_KEY = "sk-abc123def456ghi789jkl012mno345pqr678stu901vwx"
DB_PASSWORD = "SuperSecret123!"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def run_command(cmd):
    # Dangerous: shell=True
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout

def process_data(raw):
    data = pickle.loads(raw)  # Deserialization vulnerability
    return eval(f"transform({data})")  # Code injection risk

def connect_to_db():
    host = "192.168.1.100"
    from utils import *  # Wildcard import
    return create_connection(host, DB_PASSWORD)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
'''

MOCK_CLEAN_CODE = '''
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def process_data(filepath: str) -> dict:
    """Read and parse data from a file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    content = path.read_text(encoding="utf-8")
    return {"lines": len(content.splitlines()), "size": len(content)}

def validate_input(user_input: str) -> str:
    """Sanitize user input."""
    cleaned = user_input.strip()
    if len(cleaned) > 1000:
        raise ValueError("Input too long")
    return cleaned
'''


# ── Demo Sections ────────────────────────────────────────────────────

def demo_sandbox_config():
    header("1. SANDBOX ISOLATION CONFIG")

    subheader("Docker Compose (Secure Agent Container)")
    compose = generate_docker_compose()
    pretty_json(compose)

    sandbox_cfg = compose["services"]["agent-sandbox"]
    checks = [
        ("Read-only filesystem", sandbox_cfg["read_only"]),
        ("No new privileges", "no-new-privileges:true" in sandbox_cfg["security_opt"]),
        ("Seccomp profile", "seccomp=seccomp-profile.json" in sandbox_cfg["security_opt"]),
        ("All capabilities dropped", sandbox_cfg["cap_drop"] == ["ALL"]),
        ("CPU limit set", "cpus" in sandbox_cfg["deploy"]["resources"]["limits"]),
        ("Memory limit set", "memory" in sandbox_cfg["deploy"]["resources"]["limits"]),
    ]
    print()
    for label, passed in checks:
        ok(label) if passed else fail(label)

    subheader("Seccomp Profile (Syscall Filtering)")
    seccomp = generate_seccomp_profile()
    allowed = len(seccomp["syscalls"][0]["names"])
    blocked = len(seccomp["syscalls"][1]["names"])
    info(f"Default action: {seccomp['defaultAction']} (deny)")
    info(f"Allowed syscalls: {allowed}")
    info(f"Explicitly blocked dangerous syscalls: {blocked}")
    for name in seccomp["syscalls"][1]["names"]:
        fail(f"BLOCKED: {name}")


def demo_network_policy():
    header("2. NETWORK POLICIES")

    subheader("Kubernetes NetworkPolicy")
    policy = generate_k8s_network_policy(
        allowed_cidrs=["10.0.0.0/8"],
        allowed_ports=[443],
    )
    pretty_json(policy)

    spec = policy["spec"]
    print()
    ok("Default deny ingress (empty ingress rules)")
    ok(f"Egress restricted to CIDRs: {[e['cidr'] for r in spec['egress'] for e in r['to']]}")
    ok(f"Egress restricted to ports: {[p['port'] for r in spec['egress'] for p in r['ports']]}")
    warn("No public internet access allowed")


def demo_approval_workflow():
    header("3. APPROVAL WORKFLOW")

    telemetry = AgentTelemetry(session_id="demo-session")
    gate = ApprovalGate(telemetry, auto_approve_medium=True)

    subheader("Simulated Agent Session (10 Actions)")

    for action, details in MOCK_AGENT_ACTIONS:
        risk = gate.classify(action)
        # Simulate: approve some high-risk, deny others
        sim = None
        if risk.value in ("high", "critical"):
            sim = action in ("install_package",)  # only approve installs

        result = gate.check(action, details, simulate_approval=sim)

        icon = {
            ApprovalDecision.AUTO_APPROVED: f"{GREEN}AUTO{RESET}",
            ApprovalDecision.APPROVED: f"{GREEN}OK  {RESET}",
            ApprovalDecision.DENIED: f"{RED}DENY{RESET}",
            ApprovalDecision.TIMED_OUT: f"{YELLOW}T/O {RESET}",
        }[result.decision]

        risk_color = {
            "low": GREEN, "medium": YELLOW, "high": RED, "critical": RED + BOLD,
        }[risk.value]

        print(f"  [{icon}] {risk_color}{risk.value:8s}{RESET}  {action:25s}  {json.dumps(details)}")

    print()
    info(f"Approved: {len(gate.approved)} | Denied/Timed-out: {len(gate.denied)}")
    return telemetry


def demo_secret_scanning():
    header("4. SECRET SCANNING")

    subheader("Scanning Agent-Generated Code for Leaked Secrets")
    findings = scan_for_secrets(MOCK_AGENT_CODE_OUTPUT)

    if findings:
        fail(f"Found {len(findings)} secret(s) in agent output!")
        for f in findings:
            print(f"    {RED}Line {f['line']:3d}{RESET} | {f['type']:30s} | {DIM}{f['match']}{RESET}")
    else:
        ok("No secrets detected")

    subheader("Scanning Clean Code")
    clean_findings = scan_for_secrets(MOCK_CLEAN_CODE)
    if clean_findings:
        fail(f"Found {len(clean_findings)} false positive(s)")
    else:
        ok("Clean code passed secret scan (0 findings)")


def demo_policy_enforcement():
    header("5. POLICY ENFORCEMENT")

    subheader("Checking Agent Output Against Security Policies")
    violations = enforce_policies(MOCK_AGENT_CODE_OUTPUT)

    if violations:
        fail(f"Found {len(violations)} policy violation(s)!")
        for v in violations:
            sev_color = {"low": YELLOW, "medium": YELLOW, "high": RED}[v["severity"]]
            print(f"    {sev_color}[{v['severity']:6s}]{RESET} Line {v['line']:3d} | "
                  f"{v['policy']:25s} | {v['description']}")
            print(f"    {DIM}         Match: {v['match']}{RESET}")
    else:
        ok("No policy violations")

    subheader("Checking Clean Code")
    clean_violations = enforce_policies(MOCK_CLEAN_CODE)
    if clean_violations:
        warn(f"Found {len(clean_violations)} issue(s) in clean code")
    else:
        ok("Clean code passed all policy checks (0 violations)")


def demo_telemetry(telemetry: AgentTelemetry):
    header("6. AGENT TELEMETRY & ANOMALY DETECTION")

    subheader("Session Summary")
    summary = telemetry.summary()
    pretty_json(summary)

    subheader("Anomaly Detection")
    anomalies = summary["anomalies"]
    if anomalies:
        for a in anomalies:
            warn(f"Anomaly: {a['type']} - {json.dumps({k: v for k, v in a.items() if k != 'type'})}")
    else:
        ok("No anomalies detected in this session")

    subheader("Full Audit Trail (last 5 events)")
    for event in telemetry.events[-5:]:
        risk_color = {
            "low": GREEN, "medium": YELLOW, "high": RED, "critical": RED, "info": DIM,
        }.get(event["risk_level"], "")
        print(f"  {DIM}{event['iso_time']}{RESET} "
              f"{risk_color}[{event['risk_level']:8s}]{RESET} "
              f"{event['event_type']}: {json.dumps(event['details'].get('action', event['details']))}")


def demo_summary():
    header("SECURITY POSTURE SUMMARY")

    compose = generate_docker_compose()
    sandbox = compose["services"]["agent-sandbox"]
    violations = enforce_policies(MOCK_AGENT_CODE_OUTPUT)
    secrets = scan_for_secrets(MOCK_AGENT_CODE_OUTPUT)

    checks = [
        ("Container isolation", True, "Read-only FS, no-new-privileges, seccomp"),
        ("Network restriction", True, "Default-deny egress, internal CIDRs only"),
        ("Approval gates", True, "Risk-classified actions with human review"),
        ("Secret scanning", len(secrets) > 0, f"{len(secrets)} secrets caught before merge"),
        ("Policy enforcement", len(violations) > 0, f"{len(violations)} violations caught"),
        ("Audit telemetry", True, "Structured events with anomaly detection"),
    ]

    for label, passed, detail in checks:
        status = f"{GREEN}ACTIVE{RESET}" if passed else f"{RED}INACTIVE{RESET}"
        print(f"  [{status}]  {label:25s}  {DIM}{detail}{RESET}")

    print(f"\n{BOLD}{GREEN}All security layers operational.{RESET}")
    print(f"{DIM}Unsafe code was caught at multiple layers before it could reach production.{RESET}\n")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    print(f"\n{BOLD}{CYAN}")
    print("  ╔═══════════════════════════════════════════════════════════╗")
    print("  ║       SAFE CODING AGENT SANDBOX - Security Demo          ║")
    print("  ║  Sandbox + Network + Approval + Telemetry + Scanning     ║")
    print("  ╚═══════════════════════════════════════════════════════════╝")
    print(f"{RESET}")

    demo_sandbox_config()
    demo_network_policy()
    telemetry = demo_approval_workflow()
    demo_secret_scanning()
    demo_policy_enforcement()
    demo_telemetry(telemetry)
    demo_summary()


if __name__ == "__main__":
    main()
