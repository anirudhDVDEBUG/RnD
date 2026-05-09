# Safe Coding Agent Sandbox

**Security framework for running AI coding agents in production** -- generates sandbox configs, network policies, approval gates, secret scanning, and audit telemetry. Zero dependencies, pure Python.

## Headline Result

```
  [ACTIVE]  Container isolation      Read-only FS, no-new-privileges, seccomp
  [ACTIVE]  Network restriction      Default-deny egress, internal CIDRs only
  [ACTIVE]  Approval gates           Risk-classified actions with human review
  [ACTIVE]  Secret scanning          6 secrets caught before merge
  [ACTIVE]  Policy enforcement       7 violations caught
  [ACTIVE]  Audit telemetry          Structured events with anomaly detection
```

One `bash run.sh` demos all six layers catching unsafe agent output before it reaches production.

## Quick Start

```bash
bash run.sh
```

## Docs

- [HOW_TO_USE.md](HOW_TO_USE.md) -- install, integrate, trigger phrases
- [TECH_DETAILS.md](TECH_DETAILS.md) -- architecture, data flow, limitations

## Source

Based on [Running Codex safely](https://openai.com/index/running-codex-safely) by OpenAI.
