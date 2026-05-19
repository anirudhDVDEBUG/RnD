#!/usr/bin/env python3
"""Dell Codex On-Prem Enterprise Deployment Planner.

Generates deployment plans, validates configurations, and produces
infrastructure sizing recommendations for OpenAI Codex in hybrid
and on-premise enterprise environments using Dell infrastructure.
"""

import json
import math
import sys
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


class Topology(Enum):
    FULLY_ON_PREMISE = "fully_on_premise"
    HYBRID = "hybrid"
    EDGE_CLOUD = "edge_cloud"


class ComplianceFramework(Enum):
    SOC2 = "SOC 2"
    HIPAA = "HIPAA"
    FEDRAMP = "FedRAMP"
    PCI_DSS = "PCI-DSS"
    GDPR = "GDPR"
    ITAR = "ITAR"


DELL_SERVER_CATALOG = {
    "R760xa": {
        "name": "Dell PowerEdge R760xa",
        "gpus": 4,
        "gpu_type": "NVIDIA H100",
        "ram_gb": 512,
        "concurrent_sessions": 50,
        "use_case": "Mid-scale inference",
        "price_range": "$45,000-$75,000",
    },
    "XE9680": {
        "name": "Dell PowerEdge XE9680",
        "gpus": 8,
        "gpu_type": "NVIDIA H100 SXM",
        "ram_gb": 2048,
        "concurrent_sessions": 120,
        "use_case": "Large-scale inference / fine-tuning",
        "price_range": "$150,000-$300,000",
    },
    "R760": {
        "name": "Dell PowerEdge R760",
        "gpus": 0,
        "gpu_type": "N/A (CPU-only management node)",
        "ram_gb": 256,
        "concurrent_sessions": 0,
        "use_case": "Control plane / API gateway",
        "price_range": "$8,000-$15,000",
    },
}

STORAGE_OPTIONS = {
    "PowerScale": {
        "name": "Dell PowerScale",
        "type": "NAS (scale-out)",
        "best_for": "Large code repositories, shared model cache",
        "min_capacity_tb": 10,
    },
    "ECS": {
        "name": "Dell ECS (Object Storage)",
        "type": "Object storage",
        "best_for": "Model weights, artifacts, audit logs",
        "min_capacity_tb": 50,
    },
}


@dataclass
class EnterpriseRequirements:
    developer_count: int = 50
    concurrent_sessions_pct: float = 0.3  # % of devs active at once
    topology: Topology = Topology.HYBRID
    compliance_frameworks: list = field(default_factory=lambda: [ComplianceFramework.SOC2])
    air_gapped: bool = False
    repo_size_gb: float = 100.0
    auth_provider: str = "saml"
    region: str = "us-east"


@dataclass
class InfraRecommendation:
    gpu_servers: list = field(default_factory=list)
    management_servers: int = 0
    storage: dict = field(default_factory=dict)
    total_gpus: int = 0
    max_concurrent_sessions: int = 0
    estimated_cost_range: str = ""
    notes: list = field(default_factory=list)


def compute_sizing(reqs: EnterpriseRequirements) -> InfraRecommendation:
    """Calculate infrastructure sizing based on enterprise requirements."""
    concurrent = math.ceil(reqs.developer_count * reqs.concurrent_sessions_pct)
    gpus_needed = math.ceil(concurrent / 12)  # ~12 sessions per GPU

    rec = InfraRecommendation()
    rec.max_concurrent_sessions = concurrent

    # Choose server type based on scale
    if concurrent <= 60:
        server_model = "R760xa"
        servers_needed = math.ceil(gpus_needed / DELL_SERVER_CATALOG["R760xa"]["gpus"])
    else:
        server_model = "XE9680"
        servers_needed = math.ceil(gpus_needed / DELL_SERVER_CATALOG["XE9680"]["gpus"])

    spec = DELL_SERVER_CATALOG[server_model]
    rec.gpu_servers = [
        {
            "model": spec["name"],
            "count": servers_needed,
            "gpus_per_server": spec["gpus"],
            "gpu_type": spec["gpu_type"],
        }
    ]
    rec.total_gpus = servers_needed * spec["gpus"]
    rec.management_servers = max(2, math.ceil(servers_needed * 0.5))  # HA pair minimum

    # Storage
    model_cache_tb = 2  # base model weights
    repo_storage_tb = math.ceil(reqs.repo_size_gb / 100) * 10
    rec.storage = {
        "code_repos": {
            "system": "Dell PowerScale",
            "capacity_tb": max(10, repo_storage_tb),
            "purpose": "Git repositories + working copies",
        },
        "model_cache": {
            "system": "Dell ECS",
            "capacity_tb": max(50, model_cache_tb * 25),
            "purpose": "Model weights, checkpoints, audit logs",
        },
    }

    # Cost estimate
    low = servers_needed * 45000 + rec.management_servers * 8000
    high = servers_needed * 300000 + rec.management_servers * 15000
    rec.estimated_cost_range = f"${low:,} - ${high:,}"

    # Notes
    if reqs.air_gapped:
        rec.notes.append("Air-gapped: model updates require manual sideloading from verified media")
    if reqs.topology == Topology.HYBRID:
        rec.notes.append("Hybrid mode: configure cloud fallback for inference overflow")
    if concurrent > 200:
        rec.notes.append("High concurrency: consider multi-rack deployment with NVIDIA networking")

    return rec


SECURITY_CHECKLIST = [
    ("TLS everywhere", "Enable TLS for all inter-service communication"),
    ("SSO integration", "Configure {auth_provider} SSO with enterprise identity provider"),
    ("Code egress policy", "Set code egress policies to DENY - source code must not leave on-prem boundary"),
    ("Audit logging", "Enable audit logging for all Codex agent actions (reads, writes, suggestions)"),
    ("Signed updates", "Restrict model update channels to verified Dell/OpenAI signed packages"),
    ("Network segmentation", "Segment Codex inference nodes from general corporate network"),
    ("Vulnerability scanning", "Schedule weekly vulnerability scanning on Codex host infrastructure"),
    ("Secrets management", "Integrate with enterprise vault (HashiCorp Vault / CyberArk) for API keys"),
    ("Backup & DR", "Configure automated backups of model cache and configuration"),
]


def generate_security_checklist(reqs: EnterpriseRequirements) -> list:
    """Generate a security hardening checklist tailored to requirements."""
    items = []
    for name, desc in SECURITY_CHECKLIST:
        desc = desc.format(auth_provider=reqs.auth_provider.upper())
        severity = "CRITICAL" if name in ("TLS everywhere", "Code egress policy", "SSO integration") else "HIGH"
        items.append({"check": name, "description": desc, "severity": severity, "status": "PENDING"})

    if reqs.air_gapped:
        items.append({
            "check": "Air-gap verification",
            "description": "Verify no outbound network connectivity from inference nodes",
            "severity": "CRITICAL",
            "status": "PENDING",
        })

    for fw in reqs.compliance_frameworks:
        items.append({
            "check": f"{fw.value} compliance",
            "description": f"Validate deployment meets {fw.value} control requirements",
            "severity": "CRITICAL",
            "status": "PENDING",
        })

    return items


def generate_config_yaml(reqs: EnterpriseRequirements) -> str:
    """Generate a codex-enterprise-config.yaml content."""
    mode = "on-premise" if reqs.topology == Topology.FULLY_ON_PREMISE else "hybrid"
    fallback = "none" if reqs.air_gapped else "cloud"
    concurrent = math.ceil(reqs.developer_count * reqs.concurrent_sessions_pct)

    return f"""# Dell Codex Enterprise Configuration
# Generated by Dell Codex On-Prem Deploy Planner
# Topology: {reqs.topology.value} | Developers: {reqs.developer_count}

deployment:
  mode: {mode}
  region: {reqs.region}
  inference:
    primary: on-prem
    fallback: {fallback}

security:
  network_isolation: true
  tls_everywhere: true
  auth_provider: {reqs.auth_provider}
  code_egress_policy: deny
  audit_logging: true
  compliance:
{chr(10).join(f'    - {fw.value}' for fw in reqs.compliance_frameworks)}

storage:
  repository_backend: local
  model_cache: /opt/codex/models/
  repo_storage: /data/codex/repos/

scaling:
  max_concurrent_sessions: {concurrent}
  gpu_allocation: auto
  autoscale: {'false' if reqs.air_gapped else 'true'}

monitoring:
  cloudiq_enabled: {'false' if reqs.air_gapped else 'true'}
  metrics_endpoint: http://localhost:9090/metrics
  alerting:
    slack_webhook: ""  # configure per environment
    pagerduty_key: ""  # configure per environment

updates:
  channel: {'manual' if reqs.air_gapped else 'controlled'}
  auto_update: {'false' if reqs.air_gapped else 'true'}
  verification: signature_required
"""


def generate_rollout_plan(reqs: EnterpriseRequirements) -> list:
    """Generate a phased rollout plan."""
    phases = [
        {
            "phase": 1,
            "name": "Pilot",
            "duration": "2-3 weeks",
            "scope": "5-10 developers on non-critical repos",
            "goals": [
                "Validate infrastructure stability",
                "Measure baseline latency and acceptance rates",
                "Verify security controls and audit logging",
            ],
        },
        {
            "phase": 2,
            "name": "Department Rollout",
            "duration": "4-6 weeks",
            "scope": f"~{min(reqs.developer_count, 50)} developers across 2-3 teams",
            "goals": [
                "Test cross-team resource sharing and quotas",
                "Validate SSO integration at scale",
                "Collect developer satisfaction metrics",
            ],
        },
        {
            "phase": 3,
            "name": "Enterprise-Wide",
            "duration": "Ongoing",
            "scope": f"All {reqs.developer_count} developers",
            "goals": [
                "Full production deployment",
                "Activate monitoring dashboards (Dell CloudIQ + Codex)",
                "Establish operational runbooks and on-call procedures",
            ],
        },
    ]
    return phases


def print_report(reqs: EnterpriseRequirements):
    """Print a full deployment readiness report."""
    print("=" * 72)
    print("  DELL CODEX ON-PREM ENTERPRISE DEPLOYMENT PLAN")
    print("=" * 72)
    print()

    # Requirements summary
    print(">> ENTERPRISE REQUIREMENTS")
    print(f"   Developers:           {reqs.developer_count}")
    print(f"   Topology:             {reqs.topology.value}")
    print(f"   Air-gapped:           {'Yes' if reqs.air_gapped else 'No'}")
    print(f"   Compliance:           {', '.join(fw.value for fw in reqs.compliance_frameworks)}")
    print(f"   Auth provider:        {reqs.auth_provider.upper()}")
    print(f"   Repository size:      {reqs.repo_size_gb} GB")
    print(f"   Region:               {reqs.region}")
    print()

    # Infrastructure sizing
    rec = compute_sizing(reqs)
    print(">> INFRASTRUCTURE SIZING")
    print(f"   Concurrent sessions:  {rec.max_concurrent_sessions}")
    print(f"   Total GPUs needed:    {rec.total_gpus}")
    for srv in rec.gpu_servers:
        print(f"   GPU servers:          {srv['count']}x {srv['model']} ({srv['gpus_per_server']}x {srv['gpu_type']} each)")
    print(f"   Management nodes:     {rec.management_servers}x Dell PowerEdge R760")
    print(f"   Code storage:         {rec.storage['code_repos']['capacity_tb']} TB ({rec.storage['code_repos']['system']})")
    print(f"   Model/artifact store: {rec.storage['model_cache']['capacity_tb']} TB ({rec.storage['model_cache']['system']})")
    print(f"   Est. cost range:      {rec.estimated_cost_range}")
    if rec.notes:
        print(f"   Notes:")
        for note in rec.notes:
            print(f"     - {note}")
    print()

    # Security checklist
    checklist = generate_security_checklist(reqs)
    print(">> SECURITY HARDENING CHECKLIST")
    for item in checklist:
        marker = "[ ]"
        print(f"   {marker} [{item['severity']:>8}] {item['check']}: {item['description']}")
    print()

    # Config preview
    print(">> GENERATED CONFIG (codex-enterprise-config.yaml)")
    print("-" * 72)
    config = generate_config_yaml(reqs)
    for line in config.strip().split("\n"):
        print(f"   {line}")
    print("-" * 72)
    print()

    # Rollout plan
    phases = generate_rollout_plan(reqs)
    print(">> PHASED ROLLOUT PLAN")
    for phase in phases:
        print(f"   Phase {phase['phase']}: {phase['name']} ({phase['duration']})")
        print(f"     Scope: {phase['scope']}")
        for goal in phase["goals"]:
            print(f"     - {goal}")
        print()

    print("=" * 72)
    print("  Report generated. Save config with: python codex_deploy_planner.py --save")
    print("=" * 72)

    return rec, checklist, config


def run_scenarios():
    """Run multiple deployment scenarios for comparison."""
    scenarios = [
        ("Mid-size hybrid (50 devs, SOC 2)", EnterpriseRequirements(
            developer_count=50,
            topology=Topology.HYBRID,
            compliance_frameworks=[ComplianceFramework.SOC2],
        )),
        ("Large air-gapped (200 devs, FedRAMP + ITAR)", EnterpriseRequirements(
            developer_count=200,
            topology=Topology.FULLY_ON_PREMISE,
            compliance_frameworks=[ComplianceFramework.FEDRAMP, ComplianceFramework.ITAR],
            air_gapped=True,
            repo_size_gb=500,
            auth_provider="oidc",
        )),
        ("Small edge+cloud (15 devs, GDPR)", EnterpriseRequirements(
            developer_count=15,
            topology=Topology.EDGE_CLOUD,
            compliance_frameworks=[ComplianceFramework.GDPR],
            region="eu-west",
        )),
    ]

    print()
    print("=" * 72)
    print("  SCENARIO COMPARISON")
    print("=" * 72)
    print()
    print(f"  {'Scenario':<45} {'Devs':>5} {'GPUs':>5} {'Sessions':>9}  Cost Range")
    print(f"  {'-'*45} {'-'*5} {'-'*5} {'-'*9}  {'-'*25}")

    for label, reqs in scenarios:
        rec = compute_sizing(reqs)
        print(f"  {label:<45} {reqs.developer_count:>5} {rec.total_gpus:>5} {rec.max_concurrent_sessions:>9}  {rec.estimated_cost_range}")

    print()


def main():
    save_mode = "--save" in sys.argv
    scenario_mode = "--scenarios" in sys.argv

    # Default: generate a full report for a mid-size hybrid deployment
    reqs = EnterpriseRequirements(
        developer_count=75,
        concurrent_sessions_pct=0.35,
        topology=Topology.HYBRID,
        compliance_frameworks=[ComplianceFramework.SOC2, ComplianceFramework.HIPAA],
        air_gapped=False,
        repo_size_gb=250,
        auth_provider="saml",
        region="us-east",
    )

    rec, checklist, config = print_report(reqs)

    if save_mode:
        with open("codex-enterprise-config.yaml", "w") as f:
            f.write(config)
        report = {
            "requirements": asdict(reqs),
            "infrastructure": asdict(rec),
            "security_checklist": checklist,
        }
        # Fix enum serialization
        report["requirements"]["topology"] = reqs.topology.value
        report["requirements"]["compliance_frameworks"] = [fw.value for fw in reqs.compliance_frameworks]
        with open("deployment-report.json", "w") as f:
            json.dump(report, f, indent=2)
        print("\n  Saved: codex-enterprise-config.yaml, deployment-report.json")

    if scenario_mode or not save_mode:
        run_scenarios()


if __name__ == "__main__":
    main()
