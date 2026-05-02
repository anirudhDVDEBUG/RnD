# mcp-deepcontext: Symbol-Aware Semantic Search for Claude Code

Search your codebase by **meaning**, not just text. mcp-deepcontext is an MCP
server that parses your source files into symbols (functions, classes, types),
builds an embedding index, and lets Claude Code find code by semantic query
instead of grep.

## Headline Result

```
Query: "user session management"

grep results:  0 matches
semantic search:  loginUser, registerUser, deactivateUser (all relevant)
```

Plain grep requires the exact string. Semantic search understands that
`loginUser` relates to "session management" even though those words never
appear together.

## Quick Start

```bash
bash run.sh          # runs the self-contained demo (no API keys needed)
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the real MCP server into Claude Code in 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, limitations, and why this matters
