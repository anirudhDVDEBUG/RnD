# Draftspect: Office Add-Ins Powered by Claude Code

Open Word or Excel and chat with Claude Code in a sidebar — it reads and edits your document, pulls in local files/folders as context, and uses your configured MCP servers, skills, and CLAUDE.md. Everything runs locally on your machine.

**Headline result:** Type "Summarize this document" in the sidebar and get a structured summary of your Word doc, or "Analyze the revenue data" to get insights from your Excel sheet — then apply AI-suggested edits directly to the document with one click.

---

- **How to install and use** → [HOW_TO_USE.md](HOW_TO_USE.md)
- **Architecture and technical details** → [TECH_DETAILS.md](TECH_DETAILS.md)
- **Source repo** → [LeonardHope/Draftspect-Add-Ins-for-Word-and-Excel-Powered-by-Claude-Code](https://github.com/LeonardHope/Draftspect-Add-Ins-for-Word-and-Excel-Powered-by-Claude-Code)

## Quick demo

```bash
bash run.sh
```

Runs an automated walkthrough (document read, Excel data, chat interactions) in the terminal, then serves an interactive taskpane UI at `http://localhost:3000/taskpane.html`.
