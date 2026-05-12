# SFDC MCP Security Toolkit

**Adversarial testing toolkit that seeds ~70 attack payloads across 14 categories (prompt injection, honeytoken leakage, encoding bypasses, cross-tenant probes) into mock Salesforce records and scans for MCP server vulnerabilities.** Zero dependencies, runs locally in seconds.

## Headline Result

```
  VERDICT: 27 VULNERABILITIES DETECTED (14 critical)
  Your MCP integration needs hardening before production use.
```

The scanner simulates how an unsanitized MCP server would leak honeytokens, follow injected instructions, and echo SOQL payloads — then gives you a prioritized fix list.

## Quick Start

```bash
bash run.sh
```

No API keys, no Salesforce access needed. Produces a terminal report + `report.json`.

## Next Steps

- [HOW_TO_USE.md](HOW_TO_USE.md) — Installation, skill setup, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, payload categories, limitations

## Source

[ccmalcom/SFDC-MCP-Security-Toolkit](https://github.com/ccmalcom/SFDC-MCP-Security-Toolkit) — the full toolkit deploys Apex classes to a Salesforce sandbox and seeds ~270 real records.
