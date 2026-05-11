# Second Brain on Cloudflare Workers — MCP Server

**Give Claude persistent memory with semantic search.** This MCP server stores and retrieves "memories" using Cloudflare D1 (SQLite) for storage and Vectorize for similarity search, all running on Workers at the edge. Claude can `remember`, `recall`, `forget`, and `list_memories` across sessions.

**Headline result:** Ask Claude "what did I tell you about the project architecture last week?" and get a ranked list of relevant memories — even across separate conversations.

- [HOW_TO_USE.md](HOW_TO_USE.md) — Setup, install, and connect to Claude in 5 minutes
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, data flow, limitations
- `bash run.sh` — Run the local demo (no API keys needed)
