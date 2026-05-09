---
name: safe_coding_agent_sandbox
description: |
  Design and implement secure sandboxing, approval workflows, network policies, and telemetry for coding agents.
  TRIGGER: sandboxing coding agents, secure agent execution, agent security architecture, coding agent isolation, safe AI code generation, agent network policies, approval workflows for code agents
---

# Safe Coding Agent Sandbox

Design secure execution environments for coding agents with sandboxing, network controls, approval gates, and observability — based on production patterns from OpenAI's Codex platform.

## When to use

- "Set up a sandbox for a coding agent"
- "How do I run a coding agent safely in production?"
- "Design network policies and isolation for an AI code assistant"
- "Add approval workflows before an agent can execute code"
- "Implement telemetry and audit logging for agent actions"

## How to use

### 1. Sandbox Isolation

Run coding agents in isolated, ephemeral containers with minimal privileges:

- **Use microVMs or containers**: Each agent task should run in a fresh, short-lived environment (e.g., Firecracker microVMs, gVisor-sandboxed containers, or Docker with seccomp/AppArmor profiles).
- **Read-only filesystem by default**: Mount the codebase read-only. Only allow writes to a designated scratch/output directory.
- **No persistent state**: Destroy the sandbox after each task. Do not reuse environments across tasks.
- **Resource limits**: Set CPU, memory, disk, and process count limits to prevent resource abuse.

```yaml
# Example: Docker container with security constraints
services:
  agent-sandbox:
    image: agent-runner:latest
    read_only: true
    tmpfs:
      - /tmp:size=512M
    security_opt:
      - no-new-privileges:true
      - seccomp=seccomp-profile.json
    deploy:
      resources:
        limits:
          cpus: "2.0"
          memory: 4G
    network_mode: "agent-network"
```

### 2. Network Policies

Restrict what the agent can reach over the network:

- **Default deny egress**: Block all outbound traffic by default.
- **Allowlist specific endpoints**: Only permit access to approved registries (npm, PyPI), internal APIs, or version control hosts.
- **No internet access for code execution**: The agent should not be able to exfiltrate data or download arbitrary payloads.
- **DNS filtering**: Restrict DNS resolution to approved domains.

```yaml
# Kubernetes NetworkPolicy example
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: agent-sandbox-egress
spec:
  podSelector:
    matchLabels:
      role: coding-agent
  policyTypes:
    - Egress
  egress:
    - to:
        - ipBlock:
            cidr: 10.0.0.0/8  # internal services only
      ports:
        - port: 443
          protocol: TCP
```

### 3. Approval Workflows

Require human review before agents take high-impact actions:

- **Classify actions by risk**: Read-only operations (search, lint) are low-risk. File writes, dependency installs, and git operations are higher-risk.
- **Gate destructive actions**: Require explicit human approval before the agent can push commits, modify CI/CD configs, delete files, or install packages.
- **Diff review**: Present proposed code changes as diffs for human review before applying.
- **Timeout and auto-deny**: If no approval is received within a time window, deny the action by default.

```python
# Approval gate pattern
class ApprovalGate:
    RISK_LEVELS = {
        "read_file": "low",
        "search_code": "low",
        "write_file": "medium",
        "install_package": "high",
        "git_push": "high",
        "modify_ci": "critical",
    }

    async def check(self, action: str, details: dict) -> bool:
        risk = self.RISK_LEVELS.get(action, "high")
        if risk == "low":
            return True
        if risk in ("high", "critical"):
            return await self.request_human_approval(
                action, details, timeout_seconds=300
            )
        # Medium: auto-approve with logging
        self.audit_log(action, details, auto_approved=True)
        return True
```

### 4. Agent-Native Telemetry

Build observability designed for agent behavior, not just traditional APM:

- **Log every tool call**: Record the agent's reasoning, tool invocations, parameters, and results.
- **Structured audit trail**: Emit structured events for each action (file read, write, command execution) with timestamps, session IDs, and user context.
- **Anomaly detection**: Flag unusual patterns — excessive file writes, unexpected network calls, attempts to access sensitive paths.
- **Token and cost tracking**: Monitor token usage and compute costs per agent session.

```python
# Telemetry event structure
import json
import time

def emit_agent_event(event_type: str, details: dict, session_id: str):
    event = {
        "timestamp": time.time(),
        "session_id": session_id,
        "event_type": event_type,  # tool_call, file_write, approval, error
        "details": details,
    }
    # Send to your logging pipeline (e.g., stdout for container log collection)
    print(json.dumps(event))
```

### 5. Secrets and Credential Management

- **Never inject secrets into the sandbox**: Use short-lived, scoped tokens if API access is needed.
- **Scan outputs for secrets**: Run secret detection (e.g., truffleHog, gitleaks) on any agent-generated code before it leaves the sandbox.
- **Rotate credentials**: If an agent environment is compromised, rotate any credentials it may have accessed.

### 6. Compliance and Policy Enforcement

- **Code scanning**: Run SAST/DAST tools on agent-generated code before merging.
- **License compliance**: Verify that any dependencies the agent suggests are license-compatible.
- **Policy-as-code**: Define organizational policies (e.g., "no eval()", "no hardcoded IPs") and enforce them automatically on agent output.

## Architecture Overview

```
User Request
    │
    ▼
┌─────────────┐     ┌──────────────┐
│  API Gateway │────▶│ Approval Gate │
└─────────────┘     └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Sandbox    │
                    │  (microVM /  │
                    │  container)  │
                    │              │
                    │ • Read-only  │
                    │   codebase   │
                    │ • No egress  │
                    │ • Resource   │
                    │   limits     │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  Telemetry   │
                    │  & Audit Log │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Code Review  │
                    │ (diff + scan)│
                    └──────────────┘
```

## References

- [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely) — Source post describing OpenAI's production approach to secure coding agent execution with sandboxing, approvals, network policies, and agent-native telemetry.
