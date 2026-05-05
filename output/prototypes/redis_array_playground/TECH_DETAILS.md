# Technical Details

## What It Does

This playground emulates all 18 commands from the Redis Array data type proposal (PR #15162) entirely in the browser using JavaScript. It provides a command-builder UI with a sidebar listing every array command, dynamic parameter fields, optional flag checkboxes, a live command-preview string, and a formatted output display. No server, no Redis instance, no WASM compilation — the array semantics are faithfully reimplemented in ~300 lines of JS.

The original concept (by Simon Willison) compiles Redis itself to WASM for full fidelity. This prototype takes a lighter approach: pure JS emulation of the array command semantics, which is sufficient for exploring the API surface and understanding the data model.

## Architecture

```
index.html          — Single-page UI: sidebar, builder panel, preview, output
playground.js       — Command registry, in-memory array store, UI wiring
run.sh              — Launches Python HTTP server on port 8765
```

**Data flow:**
1. User selects a command → UI renders parameter fields from `COMMANDS[name].params`
2. User fills fields → `updatePreview()` builds the Redis command string live
3. User clicks Run → `collectArgs()` gathers values → `cmd.run(args)` executes against `store`
4. Result appended to output panel as formatted text

**Key implementation details:**
- `store` is a plain JS object mapping keys to arrays of strings
- `ARGREP` supports four predicates (MATCH, PREFIX, SUFFIX, CONTAINS) with NOCASE and LIMIT
- `ARSCAN` converts glob patterns to regex via `globToRegex()`
- `ARRING` implements ring-buffer semantics with `arr.push()` + `arr.shift()`
- `AROP` supports INCR, DECR, ADD, SUB, MUL on numeric string values

**Dependencies:** None. Pure vanilla JS + HTML + CSS. Python 3 is used only to serve the static files.

## Limitations

- **Not actual Redis** — this is a behavioral emulator, not a WASM-compiled Redis. Edge cases around memory management, persistence, and multi-key atomicity are not replicated.
- **No networking** — commands run locally in JS; there's no Redis protocol or RESP parsing.
- **Single-predicate ARGREP** — the real Redis ARGREP supports chaining multiple predicates with AND/OR. This emulator handles one predicate per invocation.
- **No TRE regex** — ARGREP approximate/fuzzy matching via the TRE library is not implemented; only exact predicate matching.
- **No persistence** — refreshing the page clears all data.

## Why It Matters

For teams building Claude-driven products:

- **Agent tool design** — Redis Arrays introduce a structured, index-addressable data type that maps well to agent memory and state management. Understanding the command surface helps when designing MCP tools that wrap Redis.
- **Lead-gen / marketing pipelines** — ARGREP's server-side filtering (prefix, suffix, contains, with case-insensitive matching and limits) is directly useful for searching through arrays of leads, tags, or campaign metadata without pulling data client-side.
- **Ad creative catalogs** — Arrays with ARSCAN glob matching enable fast server-side filtering of creative asset metadata stored in Redis.
- **Voice AI session state** — Ring buffers (ARRING) are a natural fit for conversation history windows in voice agents, keeping the last N turns without unbounded growth.
- **Prototyping** — This playground lets you explore the API before Redis merges the PR, so you can plan integrations early.
