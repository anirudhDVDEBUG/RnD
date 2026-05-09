"""
Safe Coding Agent Sandbox - Core Module

Provides sandbox configuration generation, network policy enforcement,
approval workflows, telemetry, secret scanning, and policy checks
for running coding agents securely.
"""

import json
import time
import re
import uuid
import hashlib
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


# ── Risk Classification ──────────────────────────────────────────────

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


ACTION_RISK_MAP = {
    "read_file": RiskLevel.LOW,
    "search_code": RiskLevel.LOW,
    "list_files": RiskLevel.LOW,
    "lint_code": RiskLevel.LOW,
    "write_file": RiskLevel.MEDIUM,
    "create_file": RiskLevel.MEDIUM,
    "run_test": RiskLevel.MEDIUM,
    "install_package": RiskLevel.HIGH,
    "delete_file": RiskLevel.HIGH,
    "git_commit": RiskLevel.HIGH,
    "git_push": RiskLevel.HIGH,
    "modify_ci": RiskLevel.CRITICAL,
    "modify_dockerfile": RiskLevel.CRITICAL,
    "run_arbitrary_command": RiskLevel.CRITICAL,
    "access_secrets": RiskLevel.CRITICAL,
}


# ── Telemetry ─────────────────────────────────────────────────────────

class AgentTelemetry:
    """Structured audit trail for every agent action."""

    def __init__(self, session_id: Optional[str] = None):
        self.session_id = session_id or str(uuid.uuid4())[:12]
        self.events: list[dict] = []
        self.token_usage = 0
        self.action_counts: dict[str, int] = {}

    def emit(self, event_type: str, details: dict, risk: Optional[RiskLevel] = None):
        event = {
            "timestamp": time.time(),
            "iso_time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "session_id": self.session_id,
            "event_type": event_type,
            "risk_level": risk.value if risk else "info",
            "details": details,
        }
        self.events.append(event)
        self.action_counts[event_type] = self.action_counts.get(event_type, 0) + 1
        return event

    def get_anomalies(self) -> list[dict]:
        """Detect suspicious patterns in the session."""
        anomalies = []
        write_count = self.action_counts.get("write_file", 0) + self.action_counts.get("create_file", 0)
        if write_count > 20:
            anomalies.append({"type": "excessive_writes", "count": write_count, "threshold": 20})

        critical_count = sum(
            1 for e in self.events if e["risk_level"] == "critical"
        )
        if critical_count > 3:
            anomalies.append({"type": "excessive_critical_actions", "count": critical_count, "threshold": 3})

        # Check for attempts to access sensitive paths
        sensitive_paths = ["/etc/shadow", "/etc/passwd", "~/.ssh", "~/.aws", ".env"]
        for e in self.events:
            path = e["details"].get("path", "")
            if any(s in path for s in sensitive_paths):
                anomalies.append({"type": "sensitive_path_access", "path": path})

        return anomalies

    def summary(self) -> dict:
        return {
            "session_id": self.session_id,
            "total_events": len(self.events),
            "action_counts": self.action_counts,
            "anomalies": self.get_anomalies(),
        }


# ── Approval Gate ─────────────────────────────────────────────────────

class ApprovalDecision(Enum):
    APPROVED = "approved"
    DENIED = "denied"
    AUTO_APPROVED = "auto_approved"
    TIMED_OUT = "timed_out"


@dataclass
class ApprovalRequest:
    action: str
    details: dict
    risk_level: RiskLevel
    decision: Optional[ApprovalDecision] = None
    reason: str = ""
    requested_at: float = field(default_factory=time.time)


class ApprovalGate:
    """Classifies actions by risk and gates high-risk ones for human review."""

    def __init__(self, telemetry: AgentTelemetry, auto_approve_medium: bool = True,
                 timeout_seconds: int = 300):
        self.telemetry = telemetry
        self.auto_approve_medium = auto_approve_medium
        self.timeout_seconds = timeout_seconds
        self.history: list[ApprovalRequest] = []

    def classify(self, action: str) -> RiskLevel:
        return ACTION_RISK_MAP.get(action, RiskLevel.HIGH)

    def check(self, action: str, details: dict, simulate_approval: Optional[bool] = None) -> ApprovalRequest:
        risk = self.classify(action)
        req = ApprovalRequest(action=action, details=details, risk_level=risk)

        if risk == RiskLevel.LOW:
            req.decision = ApprovalDecision.AUTO_APPROVED
            req.reason = "Low-risk action, auto-approved"
        elif risk == RiskLevel.MEDIUM:
            if self.auto_approve_medium:
                req.decision = ApprovalDecision.AUTO_APPROVED
                req.reason = "Medium-risk action, auto-approved with logging"
            else:
                req.decision = self._simulate_human(simulate_approval)
                req.reason = "Medium-risk action, required human approval"
        else:  # HIGH or CRITICAL
            req.decision = self._simulate_human(simulate_approval)
            req.reason = f"{risk.value.title()}-risk action, required human approval"

        self.history.append(req)
        self.telemetry.emit("approval_check", {
            "action": action,
            "risk_level": risk.value,
            "decision": req.decision.value,
            "reason": req.reason,
        }, risk)

        return req

    def _simulate_human(self, override: Optional[bool]) -> ApprovalDecision:
        if override is True:
            return ApprovalDecision.APPROVED
        elif override is False:
            return ApprovalDecision.DENIED
        return ApprovalDecision.TIMED_OUT

    @property
    def approved(self):
        return [r for r in self.history if r.decision in (ApprovalDecision.APPROVED, ApprovalDecision.AUTO_APPROVED)]

    @property
    def denied(self):
        return [r for r in self.history if r.decision in (ApprovalDecision.DENIED, ApprovalDecision.TIMED_OUT)]


# ── Secret Scanner ────────────────────────────────────────────────────

SECRET_PATTERNS = [
    (r'(?i)(aws[_\-]?secret[_\-]?access[_\-]?key)\s*[=:]\s*["\']?([A-Za-z0-9/+=]{40})', "AWS Secret Key"),
    (r'(?i)(api[_\-]?key|apikey)\s*[=:]\s*["\']?([A-Za-z0-9\-_]{20,})', "API Key"),
    (r'(?i)(password|passwd|pwd)\s*[=:]\s*["\']?([^\s"\']{8,})', "Password"),
    (r'(ghp_[A-Za-z0-9]{36})', "GitHub Personal Access Token"),
    (r'(sk-[A-Za-z0-9]{48})', "OpenAI/Anthropic API Key"),
    (r'(?i)(secret|token|credential)\s*[=:]\s*["\']?([A-Za-z0-9\-_/+=]{16,})', "Generic Secret"),
    (r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----', "Private Key"),
    (r'(eyJ[A-Za-z0-9\-_]+\.eyJ[A-Za-z0-9\-_]+\.[A-Za-z0-9\-_]+)', "JWT Token"),
]


def scan_for_secrets(code: str) -> list[dict]:
    """Scan code for leaked secrets/credentials."""
    findings = []
    for pattern, label in SECRET_PATTERNS:
        for match in re.finditer(pattern, code):
            findings.append({
                "type": label,
                "match": match.group(0)[:30] + "...",  # truncate for safety
                "line": code[:match.start()].count("\n") + 1,
            })
    return findings


# ── Policy Enforcement ────────────────────────────────────────────────

BUILTIN_POLICIES = {
    "no_eval": {
        "description": "Disallow use of eval() or exec()",
        "pattern": r'\b(eval|exec)\s*\(',
        "severity": "high",
    },
    "no_hardcoded_ip": {
        "description": "Disallow hardcoded IP addresses",
        "pattern": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        "severity": "medium",
        "exceptions": ["127.0.0.1", "0.0.0.0"],
    },
    "no_subprocess_shell": {
        "description": "Disallow subprocess with shell=True",
        "pattern": r'subprocess\.\w+\([^)]*shell\s*=\s*True',
        "severity": "high",
    },
    "no_pickle": {
        "description": "Disallow pickle.loads (deserialization attack vector)",
        "pattern": r'pickle\.(loads?|Unpickler)',
        "severity": "high",
    },
    "no_wildcard_import": {
        "description": "Disallow wildcard imports",
        "pattern": r'from\s+\S+\s+import\s+\*',
        "severity": "low",
    },
}


def enforce_policies(code: str, policies: Optional[dict] = None) -> list[dict]:
    """Check code against security policies."""
    policies = policies or BUILTIN_POLICIES
    violations = []
    for name, policy in policies.items():
        for match in re.finditer(policy["pattern"], code):
            text = match.group(0)
            # Check exceptions
            exceptions = policy.get("exceptions", [])
            if any(exc in text for exc in exceptions):
                continue
            violations.append({
                "policy": name,
                "description": policy["description"],
                "severity": policy["severity"],
                "match": text,
                "line": code[:match.start()].count("\n") + 1,
            })
    return violations


# ── Sandbox Config Generator ─────────────────────────────────────────

def generate_docker_compose(
    image: str = "agent-runner:latest",
    cpus: str = "2.0",
    memory: str = "4G",
    network: str = "agent-network",
    tmpfs_size: str = "512M",
) -> dict:
    """Generate a secure Docker Compose config for agent sandboxing."""
    return {
        "version": "3.8",
        "services": {
            "agent-sandbox": {
                "image": image,
                "read_only": True,
                "tmpfs": [f"/tmp:size={tmpfs_size}"],
                "security_opt": [
                    "no-new-privileges:true",
                    "seccomp=seccomp-profile.json",
                ],
                "cap_drop": ["ALL"],
                "cap_add": ["NET_BIND_SERVICE"],
                "deploy": {
                    "resources": {
                        "limits": {"cpus": cpus, "memory": memory},
                        "reservations": {"cpus": "0.5", "memory": "512M"},
                    }
                },
                "network_mode": network,
                "environment": {
                    "SANDBOX_MODE": "true",
                    "NO_INTERNET": "true",
                },
            }
        },
        "networks": {
            network: {
                "driver": "bridge",
                "internal": True,
            }
        },
    }


def generate_k8s_network_policy(
    name: str = "agent-sandbox-egress",
    allowed_cidrs: Optional[list[str]] = None,
    allowed_ports: Optional[list[int]] = None,
) -> dict:
    """Generate a Kubernetes NetworkPolicy for agent isolation."""
    allowed_cidrs = allowed_cidrs or ["10.0.0.0/8"]
    allowed_ports = allowed_ports or [443]

    return {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {"name": name},
        "spec": {
            "podSelector": {"matchLabels": {"role": "coding-agent"}},
            "policyTypes": ["Ingress", "Egress"],
            "ingress": [],  # deny all ingress
            "egress": [
                {
                    "to": [{"ipBlock": {"cidr": cidr}} for cidr in allowed_cidrs],
                    "ports": [{"port": p, "protocol": "TCP"} for p in allowed_ports],
                }
            ],
        },
    }


def generate_seccomp_profile() -> dict:
    """Generate a restrictive seccomp profile for the sandbox."""
    return {
        "defaultAction": "SCMP_ACT_ERRNO",
        "architectures": ["SCMP_ARCH_X86_64"],
        "syscalls": [
            {
                "names": [
                    "read", "write", "open", "close", "stat", "fstat", "lstat",
                    "poll", "lseek", "mmap", "mprotect", "munmap", "brk",
                    "rt_sigaction", "rt_sigprocmask", "ioctl", "access",
                    "pipe", "select", "sched_yield", "mremap", "msync",
                    "mincore", "madvise", "dup", "dup2", "nanosleep",
                    "getpid", "socket", "connect", "sendto", "recvfrom",
                    "bind", "listen", "accept", "clone", "execve",
                    "exit", "wait4", "kill", "uname", "fcntl",
                    "flock", "fsync", "fdatasync", "truncate", "ftruncate",
                    "getdents", "getcwd", "chdir", "mkdir", "rmdir",
                    "creat", "unlink", "readlink", "chmod", "chown",
                    "arch_prctl", "gettid", "futex", "set_tid_address",
                    "clock_gettime", "epoll_create", "epoll_wait", "epoll_ctl",
                    "openat", "newfstatat", "set_robust_list", "eventfd2",
                    "epoll_create1", "pipe2", "getrandom", "prlimit64",
                ],
                "action": "SCMP_ACT_ALLOW",
            },
            {
                "names": ["ptrace", "personality", "mount", "umount2",
                          "pivot_root", "swapon", "swapoff", "reboot",
                          "sethostname", "setdomainname", "init_module",
                          "delete_module", "kexec_load"],
                "action": "SCMP_ACT_ERRNO",
                "comment": "Dangerous syscalls - always blocked",
            },
        ],
    }
