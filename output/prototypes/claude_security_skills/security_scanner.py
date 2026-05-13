#!/usr/bin/env python3
"""
Claude Security Skills Demo Scanner
Demonstrates 6 of the 25 security audit categories from claude-security-skills:
  1. Slopsquatting detection (hallucinated packages)
  2. Prompt injection pattern detection
  3. Hardcoded secrets scanning
  4. Docker security audit
  5. OWASP LLM Top 10 checklist
  6. GitHub Actions security audit

Uses mock project files to show what each skill surfaces.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


@dataclass
class Finding:
    category: str
    severity: Severity
    title: str
    description: str
    file: Optional[str] = None
    line: Optional[int] = None
    remediation: str = ""


@dataclass
class AuditReport:
    project_name: str
    findings: list = field(default_factory=list)

    def add(self, finding: Finding):
        self.findings.append(finding)

    def summary(self) -> dict:
        counts = {}
        for s in Severity:
            counts[s.value] = sum(1 for f in self.findings if f.severity == s)
        return counts

    def print_report(self):
        sep = "=" * 72
        print(f"\n{sep}")
        print(f"  SECURITY AUDIT REPORT: {self.project_name}")
        print(f"{sep}\n")

        summary = self.summary()
        total = len(self.findings)
        print(f"  Total findings: {total}")
        for sev, count in summary.items():
            if count > 0:
                print(f"    {sev}: {count}")
        print()

        by_category = {}
        for f in self.findings:
            by_category.setdefault(f.category, []).append(f)

        for cat, findings in by_category.items():
            print(f"{'─' * 72}")
            print(f"  [{cat}]")
            print(f"{'─' * 72}")
            for f in findings:
                loc = ""
                if f.file:
                    loc = f"  @ {f.file}"
                    if f.line:
                        loc += f":{f.line}"
                print(f"\n  [{f.severity.value}] {f.title}{loc}")
                print(f"    {f.description}")
                if f.remediation:
                    print(f"    Fix: {f.remediation}")
            print()

        print(sep)
        if summary.get("CRITICAL", 0) > 0:
            print("  !! CRITICAL issues found - immediate action required")
        elif summary.get("HIGH", 0) > 0:
            print("  ! HIGH severity issues found - address before deployment")
        else:
            print("  No critical/high issues. Review medium/low findings.")
        print(sep)


# ---------------------------------------------------------------------------
# Skill 1: Slopsquatting Detection
# ---------------------------------------------------------------------------

# Real packages (a subset for quick lookup)
KNOWN_NPM = {
    "react", "express", "lodash", "axios", "next", "typescript", "webpack",
    "babel", "eslint", "prettier", "jest", "mocha", "chalk", "commander",
    "dotenv", "cors", "body-parser", "mongoose", "sequelize", "prisma",
    "zod", "yup", "uuid", "moment", "dayjs", "date-fns", "sharp",
    "jsonwebtoken", "bcrypt", "helmet", "morgan", "winston", "pino",
    "socket.io", "ws", "node-fetch", "got", "superagent",
}

KNOWN_PYPI = {
    "requests", "flask", "django", "fastapi", "numpy", "pandas", "scipy",
    "matplotlib", "scikit-learn", "tensorflow", "torch", "transformers",
    "pydantic", "sqlalchemy", "celery", "redis", "boto3", "pillow",
    "cryptography", "paramiko", "black", "mypy", "pytest", "httpx",
    "uvicorn", "gunicorn", "starlette", "jinja2", "click", "typer",
    "rich", "beautifulsoup4", "lxml", "scrapy", "anthropic",
}


def check_slopsquatting(report: AuditReport, mock_dir: str):
    """Check package manifests for hallucinated/non-existent packages."""

    # Check package.json
    pkg_json = os.path.join(mock_dir, "package.json")
    if os.path.exists(pkg_json):
        with open(pkg_json) as f:
            data = json.load(f)
        all_deps = {}
        for key in ("dependencies", "devDependencies"):
            all_deps.update(data.get(key, {}))
        for pkg in all_deps:
            if pkg not in KNOWN_NPM:
                report.add(Finding(
                    category="Slopsquatting",
                    severity=Severity.HIGH,
                    title=f"Possibly hallucinated npm package: {pkg}",
                    description=f"'{pkg}' not found in known npm registry subset. "
                                "AI may have invented this package name.",
                    file="package.json",
                    remediation=f"Run: npm view {pkg} to verify it exists. "
                                "Check for typosquatting variants.",
                ))

    # Check requirements.txt
    req_txt = os.path.join(mock_dir, "requirements.txt")
    if os.path.exists(req_txt):
        with open(req_txt) as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                pkg = re.split(r"[><=!~\[]", line)[0].strip().lower()
                if pkg and pkg not in KNOWN_PYPI:
                    report.add(Finding(
                        category="Slopsquatting",
                        severity=Severity.HIGH,
                        title=f"Possibly hallucinated PyPI package: {pkg}",
                        description=f"'{pkg}' not in known PyPI registry subset. "
                                    "Verify it exists before installing.",
                        file="requirements.txt",
                        line=i,
                        remediation=f"Run: pip index versions {pkg} to verify.",
                    ))


# ---------------------------------------------------------------------------
# Skill 2: Prompt Injection Detection
# ---------------------------------------------------------------------------

INJECTION_PATTERNS = [
    (r"ignore\s+(previous|above|all)\s+(instructions|prompts)", "Instruction override attempt"),
    (r"system\s*:\s*you\s+are", "System prompt injection via user input"),
    (r"<\|im_start\|>|<\|im_end\|>", "ChatML delimiter injection"),
    (r"\{\{.*system.*\}\}", "Template injection targeting system prompt"),
    (r"ADMIN_OVERRIDE|SUDO_MODE|GOD_MODE", "Privilege escalation keyword"),
    (r"(?i)ignore.*safety|bypass.*filter|disable.*guard", "Safety bypass attempt"),
    (r"base64\.(b64decode|decode)", "Base64 decode in prompt handling (obfuscation vector)"),
    (r"eval\s*\(.*input", "Eval on user input (code injection)"),
]


def check_prompt_injection(report: AuditReport, mock_dir: str):
    """Scan source files for prompt injection vulnerability patterns."""
    for root, _, files in os.walk(mock_dir):
        for fname in files:
            if not fname.endswith((".py", ".js", ".ts", ".txt", ".md")):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, mock_dir)
            with open(fpath) as f:
                for i, line in enumerate(f, 1):
                    for pattern, desc in INJECTION_PATTERNS:
                        if re.search(pattern, line, re.IGNORECASE):
                            report.add(Finding(
                                category="Prompt Injection",
                                severity=Severity.CRITICAL,
                                title=desc,
                                description=f"Pattern matched: {pattern}",
                                file=rel,
                                line=i,
                                remediation="Sanitize user inputs before passing "
                                            "to LLM. Use allowlists, not blocklists.",
                            ))


# ---------------------------------------------------------------------------
# Skill 3: Hardcoded Secrets
# ---------------------------------------------------------------------------

SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|secret[_-]?key|password|token)\s*=\s*['\"][^'\"]{8,}['\"]",
     "Hardcoded secret/credential"),
    (r"sk-[a-zA-Z0-9]{20,}", "OpenAI-style API key"),
    (r"sk-ant-[a-zA-Z0-9]{20,}", "Anthropic API key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key ID"),
    (r"-----BEGIN (RSA |EC )?PRIVATE KEY-----", "Private key in source"),
]


def check_hardcoded_secrets(report: AuditReport, mock_dir: str):
    """Scan for hardcoded secrets and API keys."""
    for root, _, files in os.walk(mock_dir):
        for fname in files:
            if fname.endswith((".pyc", ".png", ".jpg", ".ico")):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, mock_dir)
            try:
                with open(fpath) as f:
                    for i, line in enumerate(f, 1):
                        for pattern, desc in SECRET_PATTERNS:
                            if re.search(pattern, line):
                                report.add(Finding(
                                    category="Hardcoded Secrets",
                                    severity=Severity.CRITICAL,
                                    title=desc,
                                    description=f"Potential secret found in source code.",
                                    file=rel,
                                    line=i,
                                    remediation="Move secrets to environment variables "
                                                "or a secrets manager (Vault, AWS SSM).",
                                ))
            except (UnicodeDecodeError, PermissionError):
                pass


# ---------------------------------------------------------------------------
# Skill 4: Docker Security Audit
# ---------------------------------------------------------------------------

DOCKER_CHECKS = [
    (r"FROM\s+\S+:latest", "Using :latest tag",
     Severity.MEDIUM, "Pin to a specific image digest or version tag."),
    (r"USER\s+root", "Container runs as root",
     Severity.HIGH, "Add 'USER nonroot' or use rootless containers."),
    (r"--privileged", "Privileged container",
     Severity.CRITICAL, "Remove --privileged flag; use specific capabilities instead."),
    (r"COPY\s+\.\s+", "Copying entire build context",
     Severity.MEDIUM, "Use .dockerignore and copy only needed files."),
    (r"apt-get install(?!.*--no-install-recommends)", "Missing --no-install-recommends",
     Severity.LOW, "Add --no-install-recommends to reduce image attack surface."),
    (r"ENV\s+\w*(PASSWORD|SECRET|TOKEN|KEY)\w*\s*=", "Secret in ENV instruction",
     Severity.HIGH, "Use Docker secrets or build args with --secret flag."),
]


def check_docker_security(report: AuditReport, mock_dir: str):
    """Audit Dockerfiles for security issues."""
    for root, _, files in os.walk(mock_dir):
        for fname in files:
            if fname in ("Dockerfile", "docker-compose.yml") or fname.startswith("Dockerfile."):
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, mock_dir)
                with open(fpath) as f:
                    for i, line in enumerate(f, 1):
                        for pattern, title, sev, fix in DOCKER_CHECKS:
                            if re.search(pattern, line):
                                report.add(Finding(
                                    category="Docker Security",
                                    severity=sev,
                                    title=title,
                                    description=f"Dockerfile issue on line {i}.",
                                    file=rel,
                                    line=i,
                                    remediation=fix,
                                ))
                # Check if no USER instruction at all
                with open(fpath) as f:
                    content = f.read()
                    if "USER" not in content and "FROM" in content:
                        report.add(Finding(
                            category="Docker Security",
                            severity=Severity.HIGH,
                            title="No USER instruction - runs as root by default",
                            description="Container will run as root unless USER is specified.",
                            file=rel,
                            remediation="Add 'RUN useradd -r appuser && USER appuser'.",
                        ))


# ---------------------------------------------------------------------------
# Skill 5: OWASP LLM Top 10 Checklist
# ---------------------------------------------------------------------------

def check_owasp_llm_top10(report: AuditReport, mock_dir: str):
    """Run OWASP LLM Top 10 checklist against project files."""
    checks = {
        "LLM01 - Prompt Injection": [
            (r"user_input.*prompt|prompt.*user_input|f['\"].*\{.*input", "User input directly in prompt"),
        ],
        "LLM02 - Insecure Output Handling": [
            (r"innerHTML\s*=|dangerouslySetInnerHTML|v-html|eval\(", "LLM output rendered without sanitization"),
        ],
        "LLM03 - Training Data Poisoning": [
            (r"fine.?tune|train.*dataset|upload.*training", "Training data pipeline without validation"),
        ],
        "LLM06 - Sensitive Info Disclosure": [
            (r"system_prompt|SYSTEM_PROMPT|systemMessage", "System prompt potentially exposed to users"),
        ],
        "LLM07 - Insecure Plugin Design": [
            (r"tool_call.*exec|execute.*tool|run_tool", "Tool execution without permission checks"),
        ],
        "LLM08 - Excessive Agency": [
            (r"auto_execute|auto_approve|skip.*confirmation", "Auto-execution without human approval"),
        ],
    }

    for root, _, files in os.walk(mock_dir):
        for fname in files:
            if not fname.endswith((".py", ".js", ".ts", ".jsx", ".tsx")):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, mock_dir)
            with open(fpath) as f:
                for i, line in enumerate(f, 1):
                    for owasp_id, patterns in checks.items():
                        for pattern, desc in patterns:
                            if re.search(pattern, line, re.IGNORECASE):
                                report.add(Finding(
                                    category=f"OWASP LLM Top 10",
                                    severity=Severity.HIGH,
                                    title=f"{owasp_id}: {desc}",
                                    description=f"Potential issue found.",
                                    file=rel,
                                    line=i,
                                    remediation=f"Review against {owasp_id} guidance at "
                                                "owasp.org/www-project-top-10-for-large-language-model-applications",
                                ))


# ---------------------------------------------------------------------------
# Skill 6: GitHub Actions Security
# ---------------------------------------------------------------------------

def check_github_actions(report: AuditReport, mock_dir: str):
    """Audit GitHub Actions workflows for security issues."""
    workflows_dir = os.path.join(mock_dir, ".github", "workflows")
    if not os.path.isdir(workflows_dir):
        return

    for fname in os.listdir(workflows_dir):
        if not fname.endswith((".yml", ".yaml")):
            continue
        fpath = os.path.join(workflows_dir, fname)
        rel = os.path.relpath(fpath, mock_dir)
        with open(fpath) as f:
            for i, line in enumerate(f, 1):
                # Unpinned action versions
                if re.search(r"uses:\s+\S+@(main|master|v\d+)\s*$", line):
                    report.add(Finding(
                        category="GitHub Actions",
                        severity=Severity.HIGH,
                        title="Unpinned action version",
                        description="Action uses branch/tag ref instead of SHA pin.",
                        file=rel, line=i,
                        remediation="Pin to full SHA: uses: owner/action@<sha>",
                    ))
                # Script injection via expressions
                if re.search(r"\$\{\{\s*github\.event\.", line):
                    report.add(Finding(
                        category="GitHub Actions",
                        severity=Severity.CRITICAL,
                        title="Potential script injection via github.event context",
                        description="Untrusted event data used in run step.",
                        file=rel, line=i,
                        remediation="Pass event data through env vars, not inline expressions.",
                    ))
                # Overly permissive permissions
                if re.search(r"permissions:\s*write-all", line):
                    report.add(Finding(
                        category="GitHub Actions",
                        severity=Severity.HIGH,
                        title="Overly permissive workflow permissions",
                        description="write-all grants unnecessary access.",
                        file=rel, line=i,
                        remediation="Use least-privilege: specify individual permission scopes.",
                    ))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_audit(mock_dir: str) -> AuditReport:
    report = AuditReport(project_name=os.path.basename(os.path.abspath(mock_dir)))

    print("[*] Running security audit...")
    print(f"[*] Target: {os.path.abspath(mock_dir)}\n")

    scanners = [
        ("Slopsquatting Detection", check_slopsquatting),
        ("Prompt Injection Scan", check_prompt_injection),
        ("Hardcoded Secrets Scan", check_hardcoded_secrets),
        ("Docker Security Audit", check_docker_security),
        ("OWASP LLM Top 10 Review", check_owasp_llm_top10),
        ("GitHub Actions Security", check_github_actions),
    ]

    for name, fn in scanners:
        print(f"  [+] {name}...")
        fn(report, mock_dir)

    report.print_report()
    return report


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "mock_project"
    run_audit(target)
