---
name: markpdf_convert_md_to_pdf
description: |
  Convert Markdown files to premium PDFs, slides, and HTML using the MarkPDF MCP server.
  TRIGGER when: user wants to convert markdown to PDF, generate slides from markdown,
  export markdown as HTML, create printable documents from .md files, or mentions MarkPDF.
---

# MarkPDF — Markdown to PDF / Slides / HTML

Convert Markdown content into professionally styled PDFs, slide decks, and HTML pages using the MarkPDF MCP server.

## When to use

- "Convert this markdown file to PDF"
- "Generate a slide deck from my notes.md"
- "Export this document as a styled HTML page"
- "Create a printable PDF from this README"
- "Turn my markdown into a presentation"

## How to use

### Prerequisites

Ensure the MarkPDF MCP server is configured in your Claude Code MCP settings. Add the following to your `.mcp.json` or MCP configuration:

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

### Steps

1. **Identify the Markdown source**: Read the Markdown file or content the user wants to convert.
2. **Choose the output format**: Determine whether the user wants a PDF, slide deck, or HTML output.
3. **Use the MarkPDF MCP tools**: Call the appropriate MarkPDF MCP server tool to perform the conversion:
   - For PDF output: Use the MCP tool to convert Markdown to a styled PDF document.
   - For slides: Use the MCP tool to generate a presentation/slide deck from Markdown.
   - For HTML: Use the MCP tool to export Markdown as a styled HTML page.
4. **Deliver the result**: Provide the path to the generated output file and confirm the conversion was successful.

### Tips

- The MarkPDF server produces premium-styled documents with professional formatting out of the box.
- Markdown features like headings, lists, code blocks, tables, and images are fully supported.
- For slides, use `---` horizontal rules to separate individual slides in the Markdown source.
- If the MCP server is not available, prompt the user to install it via `npx -y markpdf-mcp-server`.

## References

- Source: [gausoft/markpdf-skill](https://github.com/gausoft/markpdf-skill)
- MCP Server: `markpdf-mcp-server` (available via npx)
