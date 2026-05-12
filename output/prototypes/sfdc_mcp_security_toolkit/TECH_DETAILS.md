# Technical Details

## What It Does

The SFDC MCP Security Toolkit is an adversarial testing framework for Salesforce MCP (Model Context Protocol) integrations. It generates records containing 14 categories of attack payloads — from prompt injection and honeytoken canaries to SOQL injection and cross-tenant boundary probes — and seeds them into Salesforce objects (Account, Contact, Case, Outreach Log). When your MCP server queries these records and passes them to an LLM, the toolkit's detection rules flag any case where the server fails to sanitize, filter, or isolate the malicious content.

The local demo (this repo) runs entirely offline: it generates mock Salesforce records, simulates three MCP response modes (raw echo, sanitized, partial leak), and applies 8 detection rules to produce a vulnerability report. The upstream repo deploys real Apex code to a Salesforce sandbox for live testing.

## Architecture

```
payloads.py          — 14 attack categories, 70 payloads, mock record generator
  |
  v
scanner.py           — Detection rules, MCP response simulator, report generator
  |
  +-- Terminal report (stdout)
  +-- report.json (machine-readable)
```

### Key Files

| File | Purpose |
|------|---------|
| `payloads.py` | Defines all 14 payload categories with 5 payloads each. Generates mock SFDC records across 4 objects. |
| `scanner.py` | 8 regex-based detection rules. Simulates MCP responses in 3 modes. Produces terminal + JSON reports. |
| `run.sh` | Entry point — runs scanner with no arguments. |

### Data Flow

1. `payloads.py` generates 70 records, each tagged with object type, target field, category, and severity
2. `scanner.py` simulates what an MCP server would return (deterministic hash selects response mode)
3. Each simulated response is scanned against 8 detection rules (regex patterns)
4. Findings are aggregated by severity, object, and category

### Dependencies

- Python 3.8+ (stdlib only — `re`, `json`, `base64`, `hashlib`, `datetime`)
- No external packages

### Detection Rules

| Rule ID | Name | Catches |
|---------|------|---------|
| LEAK-001 | Honeytoken Leaked | Canary tokens appearing in output |
| EXEC-001 | Instruction Following | LLM obeying injected instructions |
| LEAK-002 | System Prompt Exposed | System prompt content in response |
| XTEN-001 | Cross-Tenant Reference | Other org IDs or cross-tenant data |
| SQLI-001 | SOQL Injection Echo | Unsanitized SOQL fragments |
| REND-001 | Malicious Render Element | Dangerous HTML/Markdown |
| EXFIL-001 | PII Exfiltration | References to sensitive PII fields |
| TOOL-001 | Unauthorized Tool Invocation | Attacker-controlled tool calls |

## Limitations

- **This demo uses simulated MCP responses**, not a real MCP server. To test actual vulnerability, deploy the upstream toolkit to a Salesforce sandbox.
- Detection rules are regex-based — they catch obvious leaks but won't detect semantic instruction-following (e.g., an LLM rephrasing a payload).
- The 70-payload local set is a subset of the upstream's ~270 records.
- No Apex deployment or Salesforce CLI integration in this demo.
- Does not test authentication, session management, or rate limiting.

## Why It Matters for Claude-Driven Products

If you're building Claude-powered tools that read from Salesforce via MCP:

- **Lead-gen / CRM agents**: Your agent reads Account and Contact fields. If a competitor seeds a prompt injection into a company description field, your agent could leak data or follow rogue instructions.
- **Marketing automation**: Outreach Log records flow into LLM-generated email drafts. A poisoned log entry could hijack email content.
- **Agent factories**: Multi-tenant MCP setups need cross-tenant isolation. This toolkit tests whether org boundaries hold under adversarial conditions.
- **Any MCP integration**: The 14 payload categories are OWASP-style attacks adapted for the LLM+MCP threat model. Running them before go-live is basic hygiene.

## Source Repository

[ccmalcom/SFDC-MCP-Security-Toolkit](https://github.com/ccmalcom/SFDC-MCP-Security-Toolkit)
