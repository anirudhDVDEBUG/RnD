# ZeroClaw MCP Router & SDK Toolkit

**Route Claude Code requests across multiple MCP servers through a single entry point.**

ZeroClaw Plugin Hub acts as a dispatch layer: register multiple MCP backends, define routing rules, and let Claude Code call tools from any of them without switching configs. One CLI manages the whole fleet.

**Headline result:** `bash run.sh` spins up a mock multi-MCP router that dispatches tool calls to three simulated backends (filesystem, database, web-search) and returns unified results in < 2 seconds.

---

- [HOW_TO_USE.md](./HOW_TO_USE.md) — install, configure, first 60 seconds
- [TECH_DETAILS.md](./TECH_DETAILS.md) — architecture, limitations, relevance
