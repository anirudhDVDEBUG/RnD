# capsulemcp — Capsule CRM Integration for Claude

**Give Claude direct read/write access to your Capsule CRM** — contacts, opportunities, cases, and tasks — via a local MCP server you install with a single `npx` command. Supports a read-only mode for safe exploration.

## Headline result

```
  Deal              │ Stage       │ Value    │ Close Date │ Prob
  ──────────────────┼─────────────┼──────────┼────────────┼─────
  Acme Enterprise   │ Proposal    │ $120,000 │ 2026-06-15 │ 60%
  Globex Expansion  │ Negotiation │ $45,000  │ 2026-07-01 │ 40%

  Weighted pipeline: $90,000
```

Claude queries your pipeline, creates contacts, assigns tasks — all through natural conversation.

## Quick links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — install, configure, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — architecture, limitations, why it matters
- **Source:** [soil-dev/capsulemcp](https://github.com/soil-dev/capsulemcp)

## Run the demo

```bash
bash run.sh
```

No API keys needed — uses a local mock Capsule CRM API.
