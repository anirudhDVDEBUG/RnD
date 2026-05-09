# Technical Details: html_rich_output

## What it does

This is a Claude Code **skill** — a SKILL.md file that injects behavior into Claude's system prompt. When a user asks for visual explanations, PR reviews, or reports, Claude generates a single self-contained HTML file instead of plain Markdown. The HTML uses inline CSS, inline SVG diagrams, vanilla JavaScript for interactivity, and semantic HTML5 structure. No external dependencies are loaded.

The core insight (from [Thariq Shihipar's advocacy](https://simonwillison.net/2026/May/8/unreasonable-effectiveness-of-html/#atom-everything), amplified by Simon Willison) is that HTML is a dramatically better output format than Markdown for complex information: it supports diagrams, color-coding, collapsible sections, filtering, and navigation that Markdown simply cannot express.

## Architecture

```
~/.claude/skills/html_rich_output/SKILL.md
    │
    ▼  (loaded into Claude's context on startup)
Claude Code session
    │
    ▼  (user triggers: "make it HTML", "create an HTML artifact", etc.)
Claude generates a .html file via the Write tool
    │
    ▼
Single self-contained .html file in working directory
    (inline <style>, inline <script>, inline SVGs)
```

**Key files in this repo:**

| File | Purpose |
|------|---------|
| `SKILL.md` | The actual skill definition — drop this into `~/.claude/skills/html_rich_output/` |
| `generate_html_report.py` | Standalone demo that builds a sample HTML report from mock data |
| `run.sh` | Runs the demo end-to-end |

**Dependencies:** None. The skill itself is just a markdown file. The demo script uses only Python 3 standard library (`html`, `json`, `pathlib`, `datetime`).

**Model calls:** The skill itself makes zero API calls — it's a prompt-level instruction. When active, Claude's normal response generation produces the HTML file. No additional LLM calls beyond the user's conversation.

## What it does NOT do

- **No live preview server.** It writes a static file; you open it yourself.
- **No external data fetching.** The HTML it generates is fully offline/self-contained.
- **No persistent state.** Each invocation produces an independent file.
- **No charting library.** Visualizations use inline SVG, not D3/Chart.js. This keeps files self-contained but limits chart complexity.
- **No templating engine.** Claude generates the HTML directly each time — there's no Jinja/Mustache layer.
- **Not a web app framework.** The skill explicitly does NOT trigger when you're building a web application.

## Limitations

- **SVG diagrams are hand-drawn by the model.** Complex architectures may produce imperfect layouts.
- **File size scales with content.** A large PR review with many findings can produce a 50-100KB HTML file.
- **No hot-reload.** If you ask Claude to revise, it writes a new file (or overwrites).
- **Browser required.** Terminal-only workflows don't benefit from the visual output.

## Why it matters for Claude-driven products

| Use case | Application |
|----------|------------|
| **Lead-gen / marketing** | Generate polished HTML reports (competitor analysis, SEO audits, market research) that look professional without a frontend team. Drop the skill in and ask Claude to "create an HTML report" of any analysis. |
| **Ad creatives** | Rapid HTML mockups for ad landing pages, email templates, or A/B test variants — all self-contained, no build step. |
| **Agent factories** | Agents that produce human-readable output artifacts. Instead of dumping JSON or Markdown, an agent pipeline can use this skill to produce review-ready HTML dashboards. |
| **Voice AI** | Post-call analysis rendered as interactive HTML: call timeline, sentiment flow, key moments — all browsable rather than scrolling through text. |
| **Code review automation** | The demo's core use case: automated PR reviews with severity filtering, architecture diagrams, and inline code suggestions that reviewers can actually navigate. |

The fundamental insight is that HTML is the highest-fidelity output format Claude can produce natively, and a single skill file unlocks it across every project.
