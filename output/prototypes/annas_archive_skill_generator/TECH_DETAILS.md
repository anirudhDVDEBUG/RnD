# Technical Details

## What It Does

This is an MCP (Model Context Protocol) stdio server written in TypeScript that provides a single tool: `annas-archive-create-skill`. When invoked, it searches Anna's Archive (a book metadata/download aggregator) for a given query, downloads the best-matching book in PDF or EPUB format, sends the extracted text to Google Gemini for structured methodology extraction, and produces a complete Claude Code SKILL.md file that follows Anthropic's skill conventions.

The key value is collapsing what would be a multi-step manual workflow (find book, download, read, summarize, format as skill) into a single tool call that Claude Code can execute autonomously.

## Architecture

```
Claude Code ──MCP stdio──> MCP Server (Node.js/TypeScript)
                                │
                                ├─> Anna's Archive API (search + download)
                                │       Returns: book metadata, download URLs
                                │
                                ├─> File system (temporary PDF/EPUB storage)
                                │
                                ├─> Text extraction (pdf-parse / epub-parser)
                                │       Returns: raw book text
                                │
                                ├─> Google Gemini API (methodology extraction)
                                │       Input: book text + extraction prompt
                                │       Returns: structured JSON methodology
                                │
                                └─> SKILL.md template engine
                                        Returns: formatted SKILL.md string
```

### Key Files (in source repo)

- `src/index.ts` — MCP server entry point, tool registration
- `src/search.ts` — Anna's Archive search/scraping logic
- `src/download.ts` — Book download handler (PDF/EPUB)
- `src/extract.ts` — Gemini API call for methodology extraction
- `src/generate.ts` — SKILL.md template generation and audit

### Dependencies

- `@modelcontextprotocol/sdk` — MCP server framework
- `@google/generative-ai` — Gemini API client
- `pdf-parse` — PDF text extraction
- `epub-parser` or similar — EPUB text extraction
- `zod` — Input validation

## Limitations

- **Network-dependent**: Requires live access to Anna's Archive (which may be blocked in some regions or change its interface).
- **Gemini quality varies**: Extraction quality depends on book structure; highly visual or formula-heavy books produce worse results.
- **No local LLM option**: Tied to Gemini; no fallback to local models or other providers.
- **Single book per call**: Cannot batch-process multiple books in one invocation.
- **No caching**: Re-downloads and re-processes on every call, even for the same book.
- **Legal gray area**: Anna's Archive aggregates content from various sources; users should verify copyright compliance in their jurisdiction.

## Why It Matters

For teams building Claude-driven products:

- **Agent factories**: Demonstrates the pattern of "tool that creates tools" — an MCP server that generates SKILL.md files which then augment Claude's capabilities. This is a meta-automation pattern applicable to any domain where expert knowledge lives in documents.
- **Knowledge extraction pipeline**: The search → download → extract → structure pipeline is reusable for lead-gen (extract competitor methodologies), marketing (extract frameworks from industry books), and content creation.
- **Skill marketplace potential**: If you're building a skill registry or marketplace, this tool automates the supply side — converting any book into a distributable skill.
- **Gemini as extraction layer**: Shows how to use a secondary LLM (Gemini) as a structured data extraction service within a Claude-native workflow, useful for cost optimization on large document processing.
