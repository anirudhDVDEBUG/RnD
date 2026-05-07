# How to Use MarkPDF

## Option A: MCP Server (recommended)

The MarkPDF MCP server lets Claude Code convert markdown to PDF/slides/HTML natively. No manual steps — just ask Claude.

### 1. Add MCP server to Claude Code

Paste this into your `~/.claude.json` under the `mcpServers` block:

```json
{
  "mcpServers": {
    "markpdf": {
      "command": "npx",
      "args": ["-y", "markpdf-mcp-server"]
    }
  }
}
```

Or add it to a project-local `.mcp.json` in your repo root with the same structure.

### 2. Restart Claude Code

The MCP server starts automatically. No API keys needed.

### 3. Ask Claude

Trigger phrases that activate the MarkPDF tools:

- "Convert this markdown to PDF"
- "Generate a slide deck from notes.md"
- "Export this README as styled HTML"
- "Create a printable PDF from this document"
- "Turn my markdown into a presentation"

Claude will read the markdown, call the MCP server, and deliver the output file.

## Option B: Claude Skill (for auto-triggering)

### 1. Install the skill

```bash
mkdir -p ~/.claude/skills/markpdf_convert_md_to_pdf
# Copy the SKILL.md file into this directory
cp SKILL.md ~/.claude/skills/markpdf_convert_md_to_pdf/SKILL.md
```

The skill file tells Claude *when* and *how* to use the MCP server. It triggers automatically on the phrases listed above.

### 2. Ensure the MCP server is configured

The skill requires the MCP server (Option A above) to be set up. The skill provides the intelligence; the MCP server provides the conversion engine.

## Option C: Standalone demo (this repo)

No MCP server needed — runs locally with Node.js.

```bash
# Requires Node.js >= 18
bash run.sh
```

## First 60 Seconds

**Input:** `sample.md` — a quarterly product report with tables, code blocks, checklists, and blockquotes.

```bash
$ bash run.sh

=== MarkPDF Demo: Markdown → Styled HTML ===

[1/3] Installing dependencies...
[2/3] Converting sample.md → styled document...

┌─────────────────────────────────────────────┐
│  MarkPDF Demo — Markdown → Styled Output    │
└─────────────────────────────────────────────┘

  Input:       sample.md
  Format:      document
  Words:       148
  Output:      output/sample.html
  Size:        4.2 KB

  ✓ Conversion complete!

[3/3] Converting sample_slides.md → slide deck...

┌─────────────────────────────────────────────┐
│  MarkPDF Demo — Markdown → Styled Output    │
└─────────────────────────────────────────────┘

  Input:       sample_slides.md
  Format:      slides
  Slides:      5
  Output:      output/sample_slides.html
  Size:        3.1 KB

  ✓ Conversion complete!
```

**Output:** Open `output/sample.html` in any browser. You get a professionally styled document with:
- Blue accent headings with border separators
- Striped tables with colored headers
- Syntax-highlighted code blocks (dark theme)
- Styled blockquotes and checkbox lists

Print to PDF via `Ctrl+P` / `Cmd+P` for a polished PDF. The slides version (`output/sample_slides.html`) renders as individual slide cards on a dark background.

## CLI Options

```bash
# Convert a specific file
node convert.js my-report.md

# Generate slides (splits on --- horizontal rules)
node convert.js my-presentation.md --slides

# Custom output path
node convert.js my-report.md --output build/report.html
```
