# Technical Details

## What It Does

Static pattern scanner that detects the **lethal trifecta** pattern in agentic AI system code and configs: the combination of (1) untrusted input processing, (2) sensitive data access, and (3) exfiltration channels that enables prompt-injection-driven data leaks. Modeled directly on the Microsoft Copilot Cowork vulnerability where prompt injection in an email caused the agent to embed OneDrive pre-authenticated download URLs in external image tags, which were auto-sent via email — leaking files without user awareness.

The scanner is regex-based static analysis, not runtime or LLM-powered. It finds the structural conditions that make exfiltration possible, not the exploits themselves. Think of it as a checklist enforcer: if all three legs of the trifecta are present in your codebase, you have the vulnerability class regardless of specific payloads.

## Architecture

```
audit.py (single file, ~300 lines, stdlib only)
  |
  ├── Pattern definitions (4 categories):
  │   ├── UNTRUSTED_INPUT_PATTERNS   — email, doc, web, chat ingestion
  │   ├── SENSITIVE_DATA_PATTERNS    — cloud storage, pre-auth URLs, creds
  │   ├── EXFIL_CHANNEL_PATTERNS     — email send, img render, API calls
  │   └── AUTO_ACTION_PATTERNS       — auto-send, approval bypass
  │
  ├── scan_content()        — regex scan per file line
  ├── scan_json_config()    — JSON permission/rendering audit
  ├── scan_directory()      — recursive file walker
  │
  └── render_report() / render_json_report()
      └── Trifecta verdict + per-finding details + mitigation checklist

samples/
  ├── vulnerable_agent.json    — config with all bad patterns
  ├── vulnerable_handler.py    — code with full trifecta
  └── hardened_handler.py      — same flow with mitigations applied
```

### Data Flow

1. Walk target directory, filter by extension (`.py`, `.js`, `.json`, `.yaml`, etc.)
2. For each file, run regex patterns against every line
3. Classify matches into trifecta legs (input / data / channel)
4. For JSON files, additionally check permission keys and rendering config
5. Check for *missing* mitigations (CSP, sanitization, approval gates)
6. Aggregate into report with trifecta verdict and severity-sorted findings

### Key Design Decisions

- **No dependencies**: stdlib only — runs anywhere Python 3.7+ exists, no install step
- **No LLM calls**: deterministic, fast, no API keys needed
- **Exit codes**: machine-readable for CI/CD gating (0/1/2)
- **Dual output**: human-readable text or JSON for pipeline integration

## Limitations

- **Static regex only** — no data flow analysis, no taint tracking. Will produce false positives (pattern matches in comments/strings) and false negatives (obfuscated patterns, dynamic code).
- **No runtime testing** — does not actually inject canary payloads or test rendering behavior. The PoC canary test in the skill doc is a manual step.
- **Language coverage** — patterns are English-keyword oriented. Custom DSLs or non-standard naming will be missed.
- **Not a replacement for pentest** — finds the structural conditions for exfiltration, not working exploits. Use this to triage, then follow up with manual review or red-teaming.

## Why This Matters for Claude-Driven Products

If you're building any of these with Claude, you likely have the trifecta:

- **Agent factories / orchestrators**: agents that process user docs and take actions (emails, API calls) — classic exfil surface
- **Lead-gen / marketing automation**: agents that read incoming leads (untrusted) and have CRM access (sensitive) and send emails (channel)
- **Ad creative pipelines**: agents that render HTML/images from user briefs — rendered output is an exfil channel if it loads external resources
- **Voice AI with tool use**: voice agents that read caller data and can trigger webhooks or send SMS — same pattern, different modality
- **MCP servers with file access**: any MCP tool that reads files and produces markdown/HTML output could be an exfil vector if the output renderer loads external images

The Copilot Cowork bug is not a one-off — it's the template for how most agentic systems will be attacked. This scanner helps you check your own setup before someone else does.
