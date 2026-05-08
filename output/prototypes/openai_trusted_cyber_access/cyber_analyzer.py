"""
OpenAI Trusted Access for Cyber — GPT-5.5-Cyber Demo

Demonstrates how verified defenders use GPT-5.5-Cyber for:
- Vulnerability discovery in source code
- CVE exploit analysis
- Patch generation
- Infrastructure hardening audits

Uses mock responses when OPENAI_API_KEY is not set.
"""

import json
import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Mock responses — realistic examples of what GPT-5.5-Cyber returns
# ---------------------------------------------------------------------------

MOCK_VULN_ANALYSIS = {
    "model": "gpt-5.5-cyber",
    "analysis": {
        "file": "auth_handler.c",
        "vulnerabilities": [
            {
                "id": "VULN-001",
                "severity": "CRITICAL",
                "type": "Buffer Overflow (CWE-120)",
                "line": 42,
                "code": 'strncpy(session_token, user_input, sizeof(session_token));',
                "issue": "strncpy does not null-terminate if source length >= dest size. "
                         "An attacker can supply a 256-byte token to overflow session_token[256], "
                         "overwriting the adjacent is_admin flag on the stack.",
                "exploitability": "High — no ASLR on this embedded target; return address is predictable.",
                "patch": 'strncpy(session_token, user_input, sizeof(session_token) - 1);\nsession_token[sizeof(session_token) - 1] = \'\\0\';',
            },
            {
                "id": "VULN-002",
                "severity": "HIGH",
                "type": "SQL Injection (CWE-89)",
                "line": 87,
                "code": 'snprintf(query, sizeof(query), "SELECT * FROM users WHERE name=\'%s\'", username);',
                "issue": "User-controlled 'username' is interpolated directly into SQL. "
                         "Attacker can inject: ' OR 1=1 -- to bypass authentication.",
                "exploitability": "High — authentication bypass, full database read.",
                "patch": "Use parameterized queries:\n"
                         'sqlite3_prepare_v2(db, "SELECT * FROM users WHERE name=?", -1, &stmt, NULL);\n'
                         "sqlite3_bind_text(stmt, 1, username, -1, SQLITE_STATIC);",
            },
            {
                "id": "VULN-003",
                "severity": "MEDIUM",
                "type": "Time-of-Check Time-of-Use Race (CWE-367)",
                "line": 134,
                "code": "if (access(filepath, R_OK) == 0) { fd = open(filepath, O_RDONLY); }",
                "issue": "Gap between access() check and open() allows symlink race. "
                         "Attacker can swap filepath to /etc/shadow between check and use.",
                "exploitability": "Medium — requires local access and precise timing.",
                "patch": "fd = open(filepath, O_RDONLY | O_NOFOLLOW);\nif (fd < 0) { handle_error(); }",
            },
        ],
        "summary": "3 vulnerabilities found: 1 critical, 1 high, 1 medium. "
                   "The buffer overflow and SQL injection are immediately exploitable "
                   "and should be patched before any deployment.",
    },
}

MOCK_CVE_ANALYSIS = {
    "model": "gpt-5.5-cyber",
    "cve": "CVE-2024-3094",
    "analysis": {
        "name": "XZ Utils Backdoor",
        "cvss": 10.0,
        "affected": "xz-utils 5.6.0, 5.6.1",
        "attack_vector": "Supply chain — malicious code injected into build process via compromised maintainer account.",
        "mechanism": (
            "The backdoor modifies liblzma to intercept RSA_public_decrypt() in OpenSSH's sshd. "
            "When a specially crafted SSH certificate is presented, the backdoor extracts an "
            "attacker-controlled command from the certificate's CA signing key N value, "
            "decrypts it with a hardcoded ChaCha20 key, and executes it as root before authentication."
        ),
        "detection_signatures": [
            "Check xz --version for 5.6.0 or 5.6.1",
            "Inspect build-to-host.m4 for obfuscated test files",
            "Monitor sshd for unusual latency (>500ms) on pre-auth",
            "YARA rule: match on bytes {f4 8d 83 c6 8d 83} in liblzma.so",
        ],
        "remediation": [
            "Downgrade to xz-utils 5.4.x immediately",
            "Rotate all SSH host keys on affected systems",
            "Audit git history of upstream xz repository",
            "Block hashes of compromised .so files at EDR level",
        ],
    },
}

MOCK_HARDENING_AUDIT = {
    "model": "gpt-5.5-cyber",
    "target": "kubernetes-deployment.yaml",
    "findings": [
        {
            "severity": "CRITICAL",
            "issue": "Container runs as root (no securityContext.runAsNonRoot)",
            "fix": "Add securityContext:\n  runAsNonRoot: true\n  runAsUser: 1000",
        },
        {
            "severity": "HIGH",
            "issue": "No resource limits — vulnerable to DoS via resource exhaustion",
            "fix": "Add resources:\n  limits:\n    cpu: '500m'\n    memory: '256Mi'",
        },
        {
            "severity": "HIGH",
            "issue": "hostNetwork: true exposes all host ports to container",
            "fix": "Remove hostNetwork: true; use ClusterIP services instead",
        },
        {
            "severity": "MEDIUM",
            "issue": "No NetworkPolicy — pod can reach any cluster endpoint",
            "fix": "Apply a default-deny NetworkPolicy and whitelist required egress",
        },
    ],
    "score": "2/10 — Significant hardening required before production deployment.",
}

VULNERABLE_CODE_SAMPLE = """\
// auth_handler.c — simplified authentication module
#include <stdio.h>
#include <string.h>
#include <sqlite3.h>
#include <unistd.h>
#include <fcntl.h>

#define TOKEN_SIZE 256

int authenticate(const char *username, const char *user_input) {
    char session_token[TOKEN_SIZE];
    char query[512];
    int is_admin = 0;

    // Line 42: Copy session token from user input
    strncpy(session_token, user_input, sizeof(session_token));

    // Line 87: Build SQL query
    snprintf(query, sizeof(query),
             "SELECT * FROM users WHERE name='%s'", username);

    // ... execute query ...

    // Line 134: Check file access
    const char *filepath = "/var/app/config.dat";
    if (access(filepath, R_OK) == 0) {
        int fd = open(filepath, O_RDONLY);
        // ... read config ...
    }

    return is_admin;
}
"""


def print_banner():
    print("=" * 70)
    print("  OpenAI Trusted Access for Cyber -- GPT-5.5-Cyber Demo")
    print("=" * 70)
    print()


def print_section(title):
    print()
    print("-" * 70)
    print(f"  {title}")
    print("-" * 70)
    print()


def run_live_analysis(task, messages):
    """Call the real OpenAI API with GPT-5.5-Cyber."""
    try:
        from openai import OpenAI
    except ImportError:
        print("  [!] openai package not installed. Run: pip install openai")
        return None

    client = OpenAI()
    print(f"  [*] Sending {task} request to gpt-5.5-cyber ...")
    try:
        response = client.chat.completions.create(
            model="gpt-5.5-cyber",
            messages=messages,
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  [!] API error: {e}")
        print("  [!] Falling back to mock data.")
        return None


def demo_vulnerability_scan(use_api=False):
    """Demo 1: Scan source code for vulnerabilities."""
    print_section("DEMO 1: Vulnerability Discovery in Source Code")

    print("  Target: auth_handler.c")
    print()
    print("  --- Source Code Under Analysis ---")
    for i, line in enumerate(VULNERABLE_CODE_SAMPLE.strip().split("\n"), 1):
        print(f"  {i:3d} | {line}")
    print("  --- End Source Code ---")
    print()

    if use_api:
        result = run_live_analysis(
            "vulnerability scan",
            [
                {"role": "system", "content": "You are a defensive security analyst. Analyze code for vulnerabilities. Return structured JSON."},
                {"role": "user", "content": f"Analyze this C code for security vulnerabilities:\n\n{VULNERABLE_CODE_SAMPLE}"},
            ],
        )
        if result:
            print(result)
            return

    # Mock output
    analysis = MOCK_VULN_ANALYSIS["analysis"]
    print(f"  Model: {MOCK_VULN_ANALYSIS['model']}")
    print(f"  File:  {analysis['file']}")
    print(f"  Result: {analysis['summary']}")
    print()

    for v in analysis["vulnerabilities"]:
        sev_color = {"CRITICAL": "***", "HIGH": "**", "MEDIUM": "*"}.get(v["severity"], "")
        print(f"  {sev_color}[{v['severity']}] {v['id']}: {v['type']}{sev_color}")
        print(f"    Line {v['line']}: {v['code']}")
        print(f"    Issue: {v['issue']}")
        print(f"    Exploitability: {v['exploitability']}")
        print(f"    Suggested patch:")
        for patch_line in v["patch"].split("\n"):
            print(f"      + {patch_line}")
        print()


def demo_cve_analysis(use_api=False):
    """Demo 2: Analyze a known CVE."""
    print_section("DEMO 2: CVE Exploit Analysis (CVE-2024-3094 — XZ Backdoor)")

    if use_api:
        result = run_live_analysis(
            "CVE analysis",
            [
                {"role": "system", "content": "You are a threat intelligence analyst. Provide detailed CVE analysis."},
                {"role": "user", "content": "Analyze CVE-2024-3094 (XZ Utils backdoor). Cover mechanism, detection, and remediation."},
            ],
        )
        if result:
            print(result)
            return

    cve = MOCK_CVE_ANALYSIS
    a = cve["analysis"]
    print(f"  CVE:      {cve['cve']}")
    print(f"  Name:     {a['name']}")
    print(f"  CVSS:     {a['cvss']}")
    print(f"  Affected: {a['affected']}")
    print()
    print(f"  Attack Vector: {a['attack_vector']}")
    print()
    print(f"  Mechanism:")
    for line in _wrap(a["mechanism"], 64):
        print(f"    {line}")
    print()
    print("  Detection Signatures:")
    for sig in a["detection_signatures"]:
        print(f"    - {sig}")
    print()
    print("  Remediation Steps:")
    for step in a["remediation"]:
        print(f"    1. {step}")
    print()


def demo_hardening_audit(use_api=False):
    """Demo 3: Infrastructure hardening audit."""
    print_section("DEMO 3: Kubernetes Deployment Hardening Audit")

    if use_api:
        result = run_live_analysis(
            "hardening audit",
            [
                {"role": "system", "content": "You are an infrastructure security auditor. Audit Kubernetes manifests."},
                {"role": "user", "content": "Audit this K8s deployment for security issues:\napiVersion: apps/v1\nkind: Deployment\nspec:\n  template:\n    spec:\n      hostNetwork: true\n      containers:\n      - name: app\n        image: myapp:latest"},
            ],
        )
        if result:
            print(result)
            return

    audit = MOCK_HARDENING_AUDIT
    print(f"  Target: {audit['target']}")
    print(f"  Security Score: {audit['score']}")
    print()

    for f in audit["findings"]:
        print(f"  [{f['severity']}] {f['issue']}")
        print(f"    Fix:")
        for fix_line in f["fix"].split("\n"):
            print(f"      {fix_line}")
        print()


def demo_program_info():
    """Demo 4: Program overview and eligibility."""
    print_section("PROGRAM INFO: Trusted Access for Cyber")

    info = {
        "program": "OpenAI Trusted Access for Cyber",
        "models": ["gpt-5.5 (general frontier)", "gpt-5.5-cyber (security-specialized)"],
        "eligible_orgs": [
            "Government cyber agencies (CISA, NSA, NCSC, etc.)",
            "Authorized penetration testing firms",
            "Enterprise security teams at critical infrastructure orgs",
            "Academic security researchers with institutional backing",
            "Bug bounty hunters with established track records",
        ],
        "key_capabilities": [
            "Reduced safety refusals for legitimate defensive research",
            "Deep vulnerability analysis with exploit chain reasoning",
            "CVE analysis with detection signature generation",
            "Automated patch suggestion and validation",
            "Infrastructure configuration auditing",
        ],
        "apply": "https://openai.com/index/gpt-5-5-with-trusted-access-for-cyber",
    }

    print(f"  Program: {info['program']}")
    print()
    print("  Available Models:")
    for m in info["models"]:
        print(f"    - {m}")
    print()
    print("  Eligible Organizations:")
    for org in info["eligible_orgs"]:
        print(f"    - {org}")
    print()
    print("  Key Capabilities vs Standard GPT-5.5:")
    for cap in info["key_capabilities"]:
        print(f"    + {cap}")
    print()
    print(f"  Apply: {info['apply']}")
    print()


def _wrap(text, width):
    """Simple word wrap."""
    words = text.split()
    lines, current = [], []
    length = 0
    for w in words:
        if length + len(w) + 1 > width and current:
            lines.append(" ".join(current))
            current, length = [], 0
        current.append(w)
        length += len(w) + 1
    if current:
        lines.append(" ".join(current))
    return lines


def main():
    use_api = bool(os.environ.get("OPENAI_API_KEY"))
    mode = "LIVE (API)" if use_api else "MOCK (no API key)"

    print_banner()
    print(f"  Mode: {mode}")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if not use_api:
        print("  Set OPENAI_API_KEY to use real GPT-5.5-Cyber responses.")

    demo_program_info()
    demo_vulnerability_scan(use_api)
    demo_cve_analysis(use_api)
    demo_hardening_audit(use_api)

    print_section("SUMMARY")
    print("  Trusted Access for Cyber gives verified defenders access to")
    print("  GPT-5.5-Cyber — a model fine-tuned for security workflows with")
    print("  reduced refusals for legitimate defensive research.")
    print()
    print("  This demo showed three core capabilities:")
    print("    1. Source code vulnerability discovery with patch suggestions")
    print("    2. CVE exploit analysis with detection signatures")
    print("    3. Infrastructure hardening audits with fix recommendations")
    print()
    print("  To use with real API access:")
    print("    export OPENAI_API_KEY=sk-...")
    print("    python cyber_analyzer.py")
    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
