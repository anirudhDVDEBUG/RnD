# Technical Details

## What It Does

MarkPDF is an MCP (Model Context Protocol) server that converts Markdown into professionally styled PDFs, HTML slide decks, and HTML documents. When installed as an MCP server in Claude Code, it exposes conversion tools that Claude calls directly — the user just says "convert this to PDF" and gets a polished output file. The skill layer (`SKILL.md`) provides trigger-phrase matching so Claude knows when to invoke these tools without explicit instructions.

The standalone demo in this repo reproduces the core conversion pipeline: Markdown is parsed via `marked` with GFM extensions, code blocks are syntax-highlighted via `highlight.js`, and the result is wrapped in a self-contained HTML document with embedded CSS. For slides, the markdown is split on `---` horizontal rules, and each segment becomes a styled slide card. The HTML output is print-ready — browser print-to-PDF produces results indistinguishable from native PDF generation.

## Architecture

```
User prompt ("convert notes.md to PDF")
        │
        ▼
┌──────────────┐     ┌───────────────────┐
│  Claude Code │────▶│  MarkPDF MCP      │
│  (Skill.md   │     │  Server           │
│   triggers)  │     │  (npx markpdf-    │
│              │◀────│   mcp-server)     │
└──────────────┘     └───────────────────┘
                              │
                     ┌────────┼────────┐
                     ▼        ▼        ▼
                   PDF     Slides    HTML
```

### Key Files (this demo)

| File | Purpose |
|------|---------|
| `convert.js` | Core conversion engine — MD → HTML document or slide deck |
| `sample.md` | Example: report with tables, code, blockquotes, checklists |
| `sample_slides.md` | Example: presentation split by `---` separators |
| `run.sh` | One-command demo runner |
| `package.json` | Dependencies: `marked`, `highlight.js` |

### Data Flow

1. Read `.md` file from disk
2. Parse Markdown via `marked` (GFM mode: tables, task lists, strikethrough)
3. Syntax-highlight code blocks via `highlight.js` (auto-detect or explicit lang)
4. Wrap in HTML template with embedded CSS (document or slides layout)
5. Write self-contained `.html` file (no external assets)
6. For PDF: print-to-PDF via browser or headless renderer

### Dependencies

- **`marked`** (v15) — Fast Markdown parser, GFM-compliant
- **`highlight.js`** (v11) — Syntax highlighting for 190+ languages
- **Node.js >= 18** — Runtime
- **MCP server** (`markpdf-mcp-server` via npx) — The production converter (handles PDF generation natively)

## Limitations

- **This demo produces HTML, not native PDF.** The MCP server handles native PDF generation; this standalone demo relies on browser print-to-PDF. The visual result is identical.
- **No custom themes.** The embedded CSS uses a fixed blue-accent design. The MCP server may support theme options.
- **No image embedding.** Images referenced via URLs work in HTML output but won't survive a copy-paste. Local image paths work if the HTML is opened from the same directory.
- **Slide layout is basic.** No transitions, animations, or speaker notes. For full presentation features, use the MCP server's slide export.
- **Single-file input only.** No multi-file concatenation or directory scanning.

## Why It Matters

For teams building Claude-driven products:

- **Lead-gen / Marketing:** Auto-generate polished PDF reports, one-pagers, or pitch decks from markdown templates. Feed CRM data into markdown → call MarkPDF → email PDF to prospect. Zero design tool needed.
- **Agent factories:** Any agent that produces markdown output (research summaries, code reviews, analysis reports) can pipe results through MarkPDF for client-ready deliverables.
- **Ad creatives:** Convert markdown briefs into styled HTML pages for review, or PDF handoffs to design teams.
- **Documentation pipelines:** Automatically convert README files, changelogs, or API docs into distributable PDFs as part of CI/CD.

The MCP server pattern means the conversion happens inside Claude's tool loop — no separate API call, no webhook, no file upload. Ask → get PDF. This makes it a natural building block for any workflow that ends with "and send them a document."
