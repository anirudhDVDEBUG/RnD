# Technical Details

## What This Does

This prototype implements the six security layers described in OpenAI's "Running Codex safely" post as a reusable Python library and demo. It generates production-ready sandbox configurations, enforces network isolation policies, gates high-risk agent actions behind approval workflows, scans agent output for leaked secrets and policy violations, and produces structured telemetry with anomaly detection. Everything runs as pure Python stdlib -- no external dependencies.

The demo simulates a coding agent session where the agent attempts 10 actions (file reads, writes, package installs, git pushes, CI modifications) against the full security stack, showing how each layer catches different classes of risk.

## Architecture

### Key Files

| File | Purpose |
|---|---|
| `sandbox.py` | Core library: all security primitives (350 LOC) |
| `demo.py` | End-to-end demo simulating an agent session |
| `run.sh` | Entry point |

### Data Flow

```
Agent Action Request
    |
    v
[Risk Classifier] --> low / medium / high / critical
    |
    v
[Approval Gate] --> auto-approve low/medium, gate high/critical
    |
    v
[Action Executes] --> (simulated in demo)
    |
    v
[Agent Output Code]
    |
    +---> [Secret Scanner] --> regex-based, 8 pattern types
    |
    +---> [Policy Enforcer] --> 5 built-in rules (eval, shell, pickle, IPs, wildcards)
    |
    v
[Telemetry Pipeline] --> structured events, anomaly detection
```

### Components

- **Risk Classifier**: Maps 14 action types to 4 risk levels. Unknown actions default to HIGH.
- **Approval Gate**: Auto-approves LOW, optionally auto-approves MEDIUM (with logging). HIGH and CRITICAL require human approval with configurable timeout (default 300s, auto-deny on timeout).
- **Secret Scanner**: 8 regex patterns covering AWS keys, API keys, passwords, GitHub PATs, OpenAI/Anthropic keys, JWTs, private keys, and generic secrets.
- **Policy Enforcer**: 5 built-in rules (`no_eval`, `no_hardcoded_ip`, `no_subprocess_shell`, `no_pickle`, `no_wildcard_import`). Supports exception lists (e.g., `127.0.0.1` allowed for IP rule). Custom policies can be added as dicts.
- **Telemetry**: Per-session structured events with timestamps, risk levels, and action details. Anomaly detector flags excessive writes (>20), excessive critical actions (>3), and sensitive path access.
- **Config Generators**: Produce Docker Compose, Kubernetes NetworkPolicy, and seccomp profile JSON ready for deployment.

### Dependencies

None. Pure Python 3.10+ stdlib (`json`, `re`, `time`, `uuid`, `dataclasses`, `enum`).

## Limitations

- **Regex-based scanning**: Secret and policy scanning uses regex, not AST analysis. May produce false positives/negatives on complex code.
- **No real sandbox execution**: The demo simulates agent actions -- it does not actually spin up Docker containers or enforce network policies at runtime.
- **Approval gate is synchronous**: In production you'd need async approval with webhooks or a queue. The demo uses simulated decisions.
- **No SAST/DAST integration**: Policy enforcement covers basic patterns only. For production, integrate with Semgrep, Bandit, or similar tools.
- **Secret patterns are non-exhaustive**: Real secret scanning tools (truffleHog, gitleaks) use entropy analysis and provider-specific validators.

## Relevance to Claude-Driven Products

**Agent factories**: Any system that spawns coding agents (Claude Code, custom agent frameworks) needs these exact security layers. This library provides the building blocks.

**Lead-gen / marketing / ad creatives**: If you use agents to generate code for landing pages, ad integrations, or analytics pipelines, sandboxing prevents agents from accidentally leaking API keys or introducing vulnerabilities into customer-facing code.

**Voice AI**: Voice-driven coding assistants that execute code need the same isolation guarantees -- approval gates prevent voice-triggered destructive actions.

The core pattern -- classify risk, gate actions, scan outputs, log everything -- applies to any autonomous agent system, not just coding agents.
