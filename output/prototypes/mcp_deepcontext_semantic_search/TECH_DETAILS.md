# Technical Details: mcp-deepcontext

## What It Does

mcp-deepcontext is a Model Context Protocol (MCP) server written in TypeScript
that adds symbol-aware semantic search to Claude Code. It parses source files
using tree-sitter to extract structured symbols (functions, classes, interfaces,
types, constants), generates vector embeddings for each symbol's name and
surrounding context, and serves ranked search results over the MCP stdio
transport. When configured, Claude Code automatically routes code-search
queries through deepcontext instead of falling back to grep.

The key insight is **symbol-level granularity**: instead of embedding entire
files or arbitrary chunks, it anchors embeddings on language-aware symbol
boundaries, producing more precise results and richer context (definition +
references + call sites).

## Architecture

```
┌────────────┐     stdio/MCP      ┌──────────────────────┐
│ Claude Code │ ◄──────────────► │  mcp-deepcontext      │
└────────────┘                    │                        │
                                  │  1. tree-sitter parse  │
                                  │  2. symbol extraction  │
                                  │  3. embedding gen      │
                                  │  4. HNSW vector index  │
                                  │  5. ranked retrieval   │
                                  └──────────┬─────────────┘
                                             │
                                       ┌─────▼─────┐
                                       │ Source     │
                                       │ files on   │
                                       │ disk       │
                                       └───────────┘
```

### Key Components

| Component | Description |
|-----------|-------------|
| **Symbol extractor** | Uses tree-sitter grammars to parse TS/JS/Python and extract named symbols with line ranges |
| **Embedding engine** | Generates vector embeddings for symbol name + context; may use local models or API |
| **Vector index** | In-memory HNSW (Hierarchical Navigable Small World) for fast approximate nearest-neighbor search |
| **MCP transport** | Serves tools via stdio following the Model Context Protocol spec |

### Data Flow

1. **Index**: User triggers indexing (or it auto-indexes on first query)
2. **Parse**: tree-sitter walks each source file, extracts symbols
3. **Embed**: Each symbol's name + surrounding code lines → vector
4. **Store**: Vectors go into an HNSW index keyed by symbol metadata
5. **Query**: Incoming search text → embed → nearest-neighbor lookup → ranked results with file/line/context

### Dependencies

- `@anthropic-ai/sdk` or similar — MCP server framework
- `tree-sitter` + language grammars (tree-sitter-typescript, tree-sitter-javascript)
- Vector similarity library (HNSW implementation)
- Node.js >= 18

## Supported Languages

Confirmed: **TypeScript, JavaScript** (via tree-sitter grammars).
Potentially extensible to any language with a tree-sitter grammar (Python, Go, Rust, etc.).

## Limitations

- **Embedding model dependency**: The quality of semantic search depends entirely
  on the embedding model used. If it uses a local/small model, results may be
  less accurate than a full API-based embedding service.
- **Index freshness**: The index is built at query time or on-demand. There is no
  file-watcher that auto-re-indexes on save; stale results are possible after
  edits.
- **Language coverage**: Only languages with tree-sitter grammars are supported.
  Non-code files (Markdown, YAML, config) are typically skipped.
- **Memory usage**: The entire vector index lives in-process memory. Very large
  codebases (100k+ files) may consume significant RAM.
- **No cross-repo search**: Indexes a single project directory at a time.
- **MCP ecosystem maturity**: MCP is still evolving; server compatibility may
  shift between Claude Code versions.

## Why This Matters for Claude-Driven Products

If you are building **agent factories, lead-gen tools, marketing automation,
or AI-native dev workflows** on top of Claude:

1. **Better agent grounding**: Agents that can semantically search a codebase
   produce more accurate code modifications and fewer hallucinations, because
   they find the *right* context instead of relying on filename guessing.

2. **Reduced token cost**: Symbol-level retrieval returns only the relevant
   function/class + immediate context (10-30 lines) instead of entire files,
   cutting context-window usage by 5-10x.

3. **Composable MCP stack**: deepcontext slots into a multi-MCP setup alongside
   other servers (filesystem, git, browser) — each server adds a capability
   that agents can orchestrate without custom glue code.

4. **Prototype → production path**: The MCP interface means you can swap the
   local mock (this demo) for the real server with zero code changes — just
   update the config JSON.
