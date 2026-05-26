#!/usr/bin/env python3
"""
AWS Well-Architected Review — static analyzer for IaC and application code.

Scans Terraform (.tf), CloudFormation/IAM JSON, and Python source files
for anti-patterns mapped to the six Well-Architected Framework pillars.
No AWS credentials or API keys required — pure offline analysis.
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class Pillar(Enum):
    OPERATIONAL_EXCELLENCE = "Operational Excellence"
    SECURITY = "Security"
    RELIABILITY = "Reliability"
    PERFORMANCE_EFFICIENCY = "Performance Efficiency"
    COST_OPTIMIZATION = "Cost Optimization"
    SUSTAINABILITY = "Sustainability"


class Risk(Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class Finding:
    pillar: Pillar
    risk: Risk
    title: str
    description: str
    recommendation: str
    file: str
    line: Optional[int] = None


# ---------------------------------------------------------------------------
# Terraform checks
# ---------------------------------------------------------------------------

def check_terraform(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text()
    lines = text.splitlines()

    # --- Security ---
    # Wide-open security group ingress (0.0.0.0/0 on all ports)
    for i, line in enumerate(lines, 1):
        if "0.0.0.0/0" in line:
            # Check context: is this inside an ingress block with wide port range?
            context = "\n".join(lines[max(0, i - 6):i + 2])
            if "ingress" in context or "cidr_blocks" in context:
                port_match = re.search(r'to_port\s*=\s*(\d+)', context)
                if port_match and int(port_match.group(1)) > 443:
                    findings.append(Finding(
                        Pillar.SECURITY, Risk.HIGH,
                        "Security group allows unrestricted ingress on high ports",
                        f"cidr_blocks includes 0.0.0.0/0 with ports open above 443.",
                        "Restrict ingress to specific IPs/CIDRs and only required ports. "
                        "Use VPN or bastion hosts for SSH access.",
                        str(path), i,
                    ))
                elif "22" in context:
                    findings.append(Finding(
                        Pillar.SECURITY, Risk.HIGH,
                        "SSH (port 22) open to the internet",
                        "Port 22 is accessible from 0.0.0.0/0.",
                        "Restrict SSH access to known IPs or use AWS Systems Manager "
                        "Session Manager instead of direct SSH.",
                        str(path), i,
                    ))

    # Public ACL on S3
    if re.search(r'acl\s*=\s*"public-read"', text):
        findings.append(Finding(
            Pillar.SECURITY, Risk.HIGH,
            "S3 bucket has public-read ACL",
            "The bucket is publicly readable, which may expose sensitive data.",
            "Remove the public ACL. Use S3 Block Public Access and bucket policies "
            "to control access. Serve public content via CloudFront with OAI.",
            str(path),
        ))

    # Missing encryption on S3
    if "aws_s3_bucket" in text and "server_side_encryption" not in text:
        findings.append(Finding(
            Pillar.SECURITY, Risk.MEDIUM,
            "S3 bucket missing server-side encryption configuration",
            "No encryption at rest is configured for the S3 bucket.",
            "Add an aws_s3_bucket_server_side_encryption_configuration resource "
            "with AES256 or aws:kms.",
            str(path),
        ))

    # Missing versioning on S3
    if "aws_s3_bucket" in text and "versioning" not in text:
        findings.append(Finding(
            Pillar.RELIABILITY, Risk.MEDIUM,
            "S3 bucket missing versioning",
            "Versioning is not enabled, making accidental data loss unrecoverable.",
            "Enable versioning via aws_s3_bucket_versioning resource.",
            str(path),
        ))

    # Missing lifecycle rules on S3
    if "aws_s3_bucket" in text and "lifecycle" not in text:
        findings.append(Finding(
            Pillar.COST_OPTIMIZATION, Risk.LOW,
            "S3 bucket missing lifecycle rules",
            "No lifecycle policies to transition or expire objects.",
            "Add lifecycle rules to move infrequently accessed data to S3-IA or "
            "Glacier and expire old objects.",
            str(path),
        ))

    # RDS: publicly accessible
    if re.search(r'publicly_accessible\s*=\s*true', text):
        findings.append(Finding(
            Pillar.SECURITY, Risk.HIGH,
            "RDS instance is publicly accessible",
            "The database is reachable from the public internet.",
            "Set publicly_accessible = false and access via private subnets only.",
            str(path),
        ))

    # RDS: no encryption
    if "aws_db_instance" in text and re.search(r'storage_encrypted\s*=\s*false', text):
        findings.append(Finding(
            Pillar.SECURITY, Risk.HIGH,
            "RDS storage encryption disabled",
            "Database storage is not encrypted at rest.",
            "Set storage_encrypted = true and specify a KMS key.",
            str(path),
        ))

    # RDS: hard-coded password
    if "aws_db_instance" in text and re.search(r'password\s*=\s*"[^"]+"', text):
        findings.append(Finding(
            Pillar.SECURITY, Risk.HIGH,
            "Hard-coded database password in Terraform",
            "The RDS password is stored in plain text in the .tf file.",
            "Use aws_secretsmanager_secret or pass the password via a variable "
            "marked as sensitive. Never commit secrets to source control.",
            str(path),
        ))

    # RDS: no backups
    if re.search(r'backup_retention_period\s*=\s*0', text):
        findings.append(Finding(
            Pillar.RELIABILITY, Risk.HIGH,
            "RDS automated backups disabled",
            "backup_retention_period is 0 — no point-in-time recovery available.",
            "Set backup_retention_period to at least 7 days for production.",
            str(path),
        ))

    # RDS: single-AZ
    if "aws_db_instance" in text and re.search(r'multi_az\s*=\s*false', text):
        findings.append(Finding(
            Pillar.RELIABILITY, Risk.HIGH,
            "RDS deployed in single Availability Zone",
            "No multi-AZ failover — an AZ outage will cause downtime.",
            "Set multi_az = true for production databases.",
            str(path),
        ))

    # EC2: no auto-scaling
    if "aws_instance" in text and "aws_autoscaling" not in text:
        findings.append(Finding(
            Pillar.RELIABILITY, Risk.MEDIUM,
            "EC2 instance without auto-scaling",
            "A standalone EC2 instance has no auto-scaling or self-healing.",
            "Use an Auto Scaling Group with min/max/desired capacity and health checks.",
            str(path),
        ))

    # EC2: possibly over-provisioned
    large_types = ["4xlarge", "8xlarge", "12xlarge", "16xlarge", "24xlarge", "metal"]
    for lt in large_types:
        if lt in text:
            findings.append(Finding(
                Pillar.COST_OPTIMIZATION, Risk.MEDIUM,
                f"Potentially over-provisioned instance ({lt})",
                f"Instance type includes '{lt}' — verify this matches actual load.",
                "Right-size instances using AWS Compute Optimizer recommendations. "
                "Consider Graviton (arm64) instances for better price/performance.",
                str(path),
            ))
            break

    # Missing CloudWatch / monitoring
    if ("aws_instance" in text or "aws_db_instance" in text) and "cloudwatch" not in text.lower():
        findings.append(Finding(
            Pillar.OPERATIONAL_EXCELLENCE, Risk.MEDIUM,
            "No CloudWatch monitoring configured",
            "No alarms or dashboards defined alongside the resource.",
            "Add CloudWatch alarms for CPU, memory, disk, and custom application metrics.",
            str(path),
        ))

    # skip_final_snapshot
    if re.search(r'skip_final_snapshot\s*=\s*true', text):
        findings.append(Finding(
            Pillar.RELIABILITY, Risk.MEDIUM,
            "RDS skip_final_snapshot is true",
            "Destroying the RDS instance will not create a final snapshot.",
            "Set skip_final_snapshot = false and provide final_snapshot_identifier.",
            str(path),
        ))

    return findings


# ---------------------------------------------------------------------------
# IAM policy JSON checks
# ---------------------------------------------------------------------------

def check_iam_json(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        doc = json.loads(path.read_text())
    except json.JSONDecodeError:
        return findings

    statements = doc.get("Statement", [])
    for stmt in statements:
        actions = stmt.get("Action", [])
        resources = stmt.get("Resource", [])
        effect = stmt.get("Effect", "")

        if isinstance(actions, str):
            actions = [actions]
        if isinstance(resources, str):
            resources = [resources]

        if effect == "Allow" and "*" in actions and "*" in resources:
            findings.append(Finding(
                Pillar.SECURITY, Risk.HIGH,
                "IAM policy grants full admin access (Action: *, Resource: *)",
                "This policy is equivalent to AdministratorAccess and violates "
                "the principle of least privilege.",
                "Scope actions and resources to only what the role/user needs. "
                "Use AWS Access Analyzer to identify required permissions.",
                str(path),
            ))

        for action in actions:
            if action.endswith(":*") and "*" in resources:
                svc = action.split(":")[0]
                findings.append(Finding(
                    Pillar.SECURITY, Risk.HIGH,
                    f"IAM policy grants all {svc} actions on all resources",
                    f"Action '{action}' with Resource '*' is overly permissive.",
                    f"Restrict to specific {svc} actions and resource ARNs.",
                    str(path),
                ))

    return findings


# ---------------------------------------------------------------------------
# Python application code checks
# ---------------------------------------------------------------------------

def check_python(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = path.read_text()
    lines = text.splitlines()

    # Hard-coded AWS keys
    for i, line in enumerate(lines, 1):
        if re.search(r'AKIA[0-9A-Z]{16}', line):
            findings.append(Finding(
                Pillar.SECURITY, Risk.HIGH,
                "Hard-coded AWS access key in source code",
                "An AWS access key ID is embedded in the code.",
                "Use IAM roles, environment variables via Secrets Manager, "
                "or AWS SDK credential provider chain instead.",
                str(path), i,
            ))
        if re.search(r'(secret|password|key)\s*=\s*"[^"]{8,}"', line, re.IGNORECASE):
            if "AKIA" not in line:  # avoid double-reporting
                findings.append(Finding(
                    Pillar.SECURITY, Risk.HIGH,
                    "Potential secret or password hard-coded in source",
                    f"Line {i} appears to contain a hard-coded credential.",
                    "Store secrets in AWS Secrets Manager or SSM Parameter Store "
                    "and retrieve them at runtime.",
                    str(path), i,
                ))

    # SQL injection patterns
    if re.search(r"f['\"].*\{.*\}.*['\"]", text) and ("INSERT" in text or "SELECT" in text or "UPDATE" in text):
        findings.append(Finding(
            Pillar.SECURITY, Risk.HIGH,
            "Potential SQL injection via string interpolation",
            "User input appears to be interpolated directly into SQL queries.",
            "Use parameterized queries or an ORM to prevent SQL injection.",
            str(path),
        ))

    return findings


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------

RISK_ORDER = {Risk.HIGH: 0, Risk.MEDIUM: 1, Risk.LOW: 2}
PILLAR_EMOJI = {
    Pillar.OPERATIONAL_EXCELLENCE: "OPS",
    Pillar.SECURITY: "SEC",
    Pillar.RELIABILITY: "REL",
    Pillar.PERFORMANCE_EFFICIENCY: "PER",
    Pillar.COST_OPTIMIZATION: "CST",
    Pillar.SUSTAINABILITY: "SUS",
}
RISK_LABEL = {Risk.HIGH: "HIGH  ", Risk.MEDIUM: "MEDIUM", Risk.LOW: "LOW   "}


def print_report(findings: list[Finding]) -> None:
    findings.sort(key=lambda f: (RISK_ORDER[f.risk], f.pillar.value))

    print("=" * 72)
    print("  AWS WELL-ARCHITECTED REVIEW REPORT")
    print("=" * 72)
    print()

    # Summary
    by_risk = {r: 0 for r in Risk}
    by_pillar: dict[Pillar, int] = {}
    for f in findings:
        by_risk[f.risk] += 1
        by_pillar[f.pillar] = by_pillar.get(f.pillar, 0) + 1

    print(f"  Total findings: {len(findings)}")
    print(f"    HIGH:   {by_risk[Risk.HIGH]}")
    print(f"    MEDIUM: {by_risk[Risk.MEDIUM]}")
    print(f"    LOW:    {by_risk[Risk.LOW]}")
    print()
    print("  Findings by pillar:")
    for pillar in Pillar:
        count = by_pillar.get(pillar, 0)
        bar = "#" * count
        print(f"    [{PILLAR_EMOJI[pillar]}] {pillar.value:<25s} {count:>2d}  {bar}")
    print()
    print("-" * 72)

    # Detail
    for idx, f in enumerate(findings, 1):
        loc = f.file
        if f.line:
            loc += f":{f.line}"
        print(f"\n  [{RISK_LABEL[f.risk]}] #{idx}  {f.title}")
        print(f"  Pillar : {f.pillar.value}")
        print(f"  File   : {loc}")
        print(f"  Detail : {f.description}")
        print(f"  Fix    : {f.recommendation}")
        print("  " + "-" * 68)

    print()
    print("=" * 72)
    if by_risk[Risk.HIGH] > 0:
        print(f"  VERDICT: {by_risk[Risk.HIGH]} HIGH-risk findings require immediate attention.")
    elif by_risk[Risk.MEDIUM] > 0:
        print(f"  VERDICT: No critical issues, but {by_risk[Risk.MEDIUM]} MEDIUM-risk items to address.")
    else:
        print("  VERDICT: Architecture looks solid. Only minor improvements suggested.")
    print("=" * 72)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def scan_directory(target: str) -> list[Finding]:
    target_path = Path(target)
    findings: list[Finding] = []

    if target_path.is_file():
        files = [target_path]
    else:
        files = sorted(target_path.rglob("*"))

    for fp in files:
        if fp.suffix == ".tf":
            findings.extend(check_terraform(fp))
        elif fp.suffix == ".json":
            findings.extend(check_iam_json(fp))
        elif fp.suffix == ".py" and fp.name != "wa_reviewer.py":
            findings.extend(check_python(fp))

    return findings


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "samples"
    if not Path(target).exists():
        print(f"Error: path '{target}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"\nScanning: {target}\n")
    findings = scan_directory(target)

    if not findings:
        print("No findings. The scanned files look clean.")
    else:
        print_report(findings)


if __name__ == "__main__":
    main()
