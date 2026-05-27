# Agentic Exfiltration Defense Audit

**Scan your AI agent code and configs for data exfiltration vulnerabilities** — the "lethal trifecta" where prompt injection + sensitive data access + an output channel = leaked files.

Inspired by the [Microsoft Copilot Cowork exfiltration disclosure](https://simonwillison.net/2026/May/26/copilot-cowork-exfiltrates-files/) where agents auto-sent emails containing rendered external images that leaked OneDrive files via pre-authenticated URLs.

## Headline Result

```
!! LETHAL TRIFECTA DETECTED !!
  [X] Untrusted Input:      Email processing, Document ingestion
  [X] Sensitive Data:       Cloud storage access, Pre-authenticated URL generation
  [X] Exfiltration Channel: Email sending, HTML/Markdown rendering
  -> 8 CRITICAL, 12 HIGH severity findings
```

## Quick Start

```bash
bash run.sh                          # Demo with sample vulnerable/hardened agents
python3 audit.py <your-project-dir>  # Scan your own code
python3 audit.py agent.json --json   # JSON output for CI pipelines
```

Zero dependencies (Python 3.7+ stdlib only).

See [HOW_TO_USE.md](HOW_TO_USE.md) for Claude Code skill installation and [TECH_DETAILS.md](TECH_DETAILS.md) for architecture details.
