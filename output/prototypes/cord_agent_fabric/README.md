# Cord Agent Fabric — Prototype

**Distributed agent mesh that lets LLMs, MCP servers, and AI agents discover each other across machines using natural-language semantic search.** Built in Rust, Cord replaces hard-coded service URLs with a decentralized, zero-config discovery layer.

## Headline result

```
Query: "agent that handles database operations and schema changes"
  1. db-agent       [agent]       on ops-node     ██████████████████████████████ 82%
  2. deploy-agent   [agent]       on ops-node     █████████░░░░░░░░░░░░░░░░░░░░ 28%
  3. git-mcp        [mcp-server]  on dev-box      ██████░░░░░░░░░░░░░░░░░░░░░░░ 19%
```

Eight services registered across five peers, discovered instantly with plain-English queries — no exact name matches required.

## Quick links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the real Cord, set up the Claude skill, run the demo.
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, relevance to agent factories.
- **[run.sh](run.sh)** — `bash run.sh` for an end-to-end demo (no API keys needed).
- **Source**: https://github.com/fosenai/cord
