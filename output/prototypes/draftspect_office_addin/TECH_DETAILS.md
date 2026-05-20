# Technical Details

## What it does

Draftspect is an Electron-based Office add-in that embeds a Claude Code chat interface into Microsoft Word and Excel as a taskpane sidebar. It reads document content via Office.js, sends it as context to a locally-running Claude Code CLI process, and writes AI-generated edits back to the document. Users can also point the add-in at local folders (notes, drafts, repos, data files) to include as additional context, making Claude aware of surrounding project material.

The key insight is that Claude Code already has file read/write capabilities and MCP server access — Draftspect simply bridges Office documents into that existing local agent environment, so your configured skills, CLAUDE.md instructions, and MCP tools all work inside Office.

## Architecture

```
┌─────────────────────────────────────────────┐
│  Microsoft Word / Excel                      │
│  ┌──────────────────────────────────┐        │
│  │  Taskpane (iframe)               │        │
│  │  taskpane.html + chat UI         │        │
│  │         │                        │        │
│  │    Office.js API                 │        │
│  │    (read/write document)         │        │
│  └──────────┬───────────────────────┘        │
└─────────────┼────────────────────────────────┘
              │ HTTP / WebSocket
┌─────────────▼────────────────────────────────┐
│  Local Node/Electron Server (server.js)      │
│  ├── office-bridge.js   (Office.js wrapper)  │
│  ├── claude-runner.js   (CLI process mgmt)   │
│  └── context loader     (local file ingest)  │
│              │                                │
│       child_process.spawn("claude")          │
│              │                                │
│  ┌───────────▼──────────────────────┐        │
│  │  Claude Code CLI                 │        │
│  │  • Uses your ~/.claude config    │        │
│  │  • MCP servers available         │        │
│  │  • Skills & CLAUDE.md active     │        │
│  └──────────────────────────────────┘        │
└──────────────────────────────────────────────┘
```

### Key files

| File | Purpose |
|------|---------|
| `manifest.xml` | Office add-in manifest — declares host apps, permissions, source URL |
| `server.js` | Express server handling API routes for doc read/write and chat |
| `office-bridge.js` | Abstraction over Office.js Word/Excel APIs (mock in demo) |
| `claude-runner.js` | Spawns and manages Claude Code CLI process, pipes context |
| `public/taskpane.html` | Sidebar chat UI rendered inside the Office taskpane |

### Data flow

1. User types a message in the taskpane chat
2. Server reads current document content via Office.js bridge
3. Document text + user message sent to Claude Code CLI as prompt context
4. Claude responds with text and optional edit actions
5. Edit actions (insert, replace, write range) applied back through Office.js
6. Response displayed in chat; document updates in real time

### Dependencies

- **Express** — local HTTP server for the taskpane
- **ws** — WebSocket support for streaming responses (production)
- **Electron** — desktop shell (production; not needed for demo)
- **office-addin-dev-certs** — HTTPS certificates for Office.js requirement (production)
- **Claude Code CLI** — the AI backend, runs locally

### Model calls

In production, all AI interaction goes through the locally-installed Claude Code CLI (`claude --print`). The CLI handles its own API authentication and model selection. No direct Anthropic API calls are made by the add-in code itself.

## Limitations

- **Requires Office desktop apps** — does not work with Office Online/web versions (Office.js taskpane sideloading is desktop-only for custom add-ins)
- **Windows/Mac only** — Office desktop add-ins aren't supported on Linux
- **Claude Code CLI required** — the user must have `claude` installed and authenticated
- **No streaming in basic mode** — the demo uses request/response; production should use WebSocket streaming for better UX
- **Document size limits** — very large documents may exceed Claude's context window; chunking strategy needed
- **No multi-user** — runs entirely locally, single-user only
- **Manifest distribution** — for team use, the manifest needs to be deployed via SharePoint catalog or Microsoft 365 admin center

## Why it matters

For teams building Claude-driven products:

- **Agent factories**: Demonstrates how to embed Claude Code as a backend agent inside existing productivity tools — the same pattern works for CRMs, project management tools, or any app with a sidebar/plugin model
- **Lead-gen / marketing**: Sales teams can use Claude inside their actual workflow (Word proposals, Excel deal models) instead of switching to a separate AI tool
- **Document automation**: The Office.js bridge pattern enables programmatic document generation and editing, useful for report builders, template engines, and content pipelines
- **Local-first AI**: All data stays on the user's machine — no cloud relay, no data residency concerns — which is a selling point for enterprise and regulated industries
