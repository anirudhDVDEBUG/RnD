---
name: annas_archive_skill_generator
description: |
  Search Anna's Archive for books, download them, extract methodologies using Gemini, and generate audited Claude Code SKILL.md files. End-to-end knowledge extraction pipeline from books to actionable skills.
  Triggers: book search, knowledge extraction, methodology extraction, SKILL.md from book, Anna's Archive search
---

# Anna's Archive Skill Generator

Search Anna's Archive for books (PDF/EPUB), download them, extract structured methodologies via Google Gemini, and produce audited Claude Code SKILL.md files — all in one pipeline.

## When to use

- "Extract a methodology from this book and create a skill"
- "Search Anna's Archive for books on [topic] and build a skill"
- "Generate a SKILL.md from a PDF/EPUB book"
- "Download a book and extract its key frameworks into a Claude skill"
- "Turn this book's methodology into an actionable Claude Code skill"

## How to use

### Prerequisites

1. **Install the MCP server** from the repository:
   ```bash
   git clone https://github.com/VKirill/mcp-annas-archive-create-skill.git
   cd mcp-annas-archive-create-skill
   npm install && npm run build
   ```

2. **Configure environment variables:**
   - `GEMINI_API_KEY` — Google AI Studio API key for Gemini (used for methodology extraction from book content)
   - Ensure network access to Anna's Archive for search and download

3. **Register the MCP server** in your Claude Code configuration (`~/.claude/settings.json` or project-level):
   ```json
   {
     "mcpServers": {
       "annas-archive-create-skill": {
         "command": "node",
         "args": ["path/to/mcp-annas-archive-create-skill/dist/index.js"],
         "env": {
           "GEMINI_API_KEY": "your-gemini-api-key"
         }
       }
     }
   }
   ```

### Workflow

1. **Search**: Query Anna's Archive with a book title, author, or topic. The tool searches and returns matching results with metadata.

2. **Download**: Select a result and the tool downloads the book (PDF or EPUB format).

3. **Extract**: The book content is sent to Google Gemini for methodology extraction — identifying key frameworks, step-by-step processes, decision trees, and actionable patterns.

4. **Generate**: A structured, audited SKILL.md file is produced following Claude Code skill conventions, containing the extracted methodology ready for use as a Claude Code skill.

5. **Audit**: The generated SKILL.md is evaluated for quality, completeness, and adherence to skill format standards.

All steps run in a single MCP tool call for an end-to-end experience.

### Example

```
Use the annas-archive-create-skill tool to find "Getting Things Done by David Allen",
download it, extract the GTD methodology, and generate a SKILL.md I can use
for task management workflows.
```

The output will be a complete SKILL.md with:
- YAML frontmatter (name, description, triggers)
- When to use section with trigger phrases
- Step-by-step methodology extracted from the book
- Concrete, actionable instructions for Claude Code

## References

- Source: [VKirill/mcp-annas-archive-create-skill](https://github.com/VKirill/mcp-annas-archive-create-skill)
- Stack: TypeScript, Node.js, MCP stdio server
- Integrations: Anna's Archive (search/download), Google Gemini (extraction), Claude Code (skill output)
