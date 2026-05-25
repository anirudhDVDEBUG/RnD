# Technical Details

## What datasette-agent does

datasette-agent is a Datasette plugin that injects an agentic chat interface into Datasette's Jump menu (the `/` shortcut). When a user types a natural-language question, the agent translates it into SQL, executes the query against the connected database, and returns formatted results -- all within the Datasette browser UI. The agent can run multi-turn conversations, refining queries iteratively.

The plugin leverages the `makeJumpSections()` JavaScript plugin hook introduced in Datasette 1.0a30. This hook allows plugins to register custom UI sections in the Jump menu without any server-side configuration. datasette-agent registers itself automatically on install.

## Architecture

```
Browser (Jump menu)
  |
  v
makeJumpSections() JS hook  <-- datasette-agent registers here
  |
  v
Agent chat UI (injected panel)
  |
  v
LLM call (NL -> SQL)  <-- translates user question to SQL
  |
  v
Datasette SQL API  <-- executes the generated query
  |
  v
Formatted results displayed in chat panel
```

### Key components

| Component | Role |
|-----------|------|
| `makeJumpSections()` hook | Entry point; injects the chat input into the Jump menu |
| Agent chat panel | Browser-side UI for the conversation thread |
| NL-to-SQL layer | Sends the user's question + schema context to an LLM, receives SQL |
| Datasette SQL API | Executes the generated SQL and returns JSON results |

### Dependencies

- **Datasette >= 1.0a30** -- required for `makeJumpSections()` support
- **datasette-agent >= 0.1a4** -- the plugin itself (alpha)
- An LLM backend (configured via Datasette's LLM plugin ecosystem) for NL-to-SQL translation

## Limitations

- **Alpha software** (0.1a4) -- API and UI may change between releases.
- Requires an LLM backend for real NL-to-SQL; without one, the chat input appears but cannot generate queries.
- Only works with databases Datasette can read (SQLite primarily).
- Complex multi-join or analytical queries may produce incorrect SQL depending on the backing LLM's capabilities.
- The Jump menu UI is keyboard-driven (`/` shortcut); there is no standalone page or REST endpoint for the chat.

## What it does NOT do

- It does not write or modify data -- all generated SQL is read-only (`SELECT`).
- It does not provide its own LLM -- you must configure one via Datasette's plugin ecosystem (e.g., `datasette-llm`).
- It does not support non-SQLite databases (Postgres, MySQL, etc.) unless Datasette itself is configured with those backends.

## Why it matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | Shows a pattern for embedding agentic NL interfaces into existing tools via plugin hooks -- reusable for any app with a command palette or search menu. |
| **Lead-gen / marketing** | Analysts can query campaign databases in plain English without writing SQL, lowering the barrier to data-driven decisions. |
| **Ad creatives** | Creative teams can pull performance metrics ("show me top 5 ads by CTR this week") without leaving the data tool. |
| **Voice AI** | The NL-to-SQL pattern is directly transferable to voice-driven data queries -- swap the text input for speech-to-text. |
| **Internal tools** | Any team with a SQLite dataset can add a chat-based exploration layer in minutes, reducing the need for custom dashboards. |
