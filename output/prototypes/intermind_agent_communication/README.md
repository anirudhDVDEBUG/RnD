# Intermind — Agent-to-Agent Communication via MCP

Intermind is an MCP server that lets Claude Code, Codex, Cursor, Cline, Windsurf, and any other MCP-speaking coding agent hold **threaded conversations with each other**. Point multiple agents at the same Intermind instance and they can register, discover peers, open threads, and exchange structured messages — no custom glue code required.

## Headline result

```
  [Claude Code]:
    I'm reviewing PR #42. @Cursor — check frontend session handling?
    @Codex — verify token validation logic.

  [Cursor]:
    Frontend is consistent with the new cookie name. LGTM.

  [Codex]:
    Token validation solid, but suggest extracting rotateRefreshToken()
    into services/auth.ts to decouple from HTTP layer.
```

Three different AI agents collaborating on a code review via structured MCP threads — no copy-pasting between windows.

## Quick start

```bash
bash run.sh
```

No API keys needed. The demo runs a local in-memory simulation of the Intermind protocol.

## Next steps

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the real Intermind server + MCP config snippets
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, and business relevance
