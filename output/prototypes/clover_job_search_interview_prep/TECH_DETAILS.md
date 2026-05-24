# Technical Details — Clover Job Search & Interview Prep

## What It Does

Clover is an MCP (Model Context Protocol) server packaged as `@fourleafai/clover-mcp` on npm. When registered in Claude's MCP config, it exposes three tools that Claude can call during conversation:

- **`job_search`** — Queries four-leaf.ai's job aggregation API for live listings filtered by role, location, seniority, and keywords. Returns structured job objects with title, company, salary range, and application links.
- **`interview_prep`** — Given a company and role, returns a structured interview intelligence package: the company's typical interview process, role-specific behavioral and technical questions, and preparation tips drawn from candidate reports.
- **`resume_review`** — Accepts resume text and a target role, then returns a scored breakdown by section (summary, experience, skills, education), keyword alignment analysis, and prioritized action items.

The MCP server acts as a bridge: Claude sends structured tool calls, Clover translates them into API requests to four-leaf.ai, and returns structured JSON that Claude renders conversationally.

## Architecture

```
User prompt
    |
    v
Claude (with SKILL.md routing hints)
    |
    v  MCP tool call (JSON-RPC over stdio)
@fourleafai/clover-mcp  (Node.js, runs via npx)
    |
    v  HTTPS
four-leaf.ai API
    |
    v
Structured JSON response -> Claude renders to user
```

### Key Files (in source repo)

| Path | Purpose |
|---|---|
| `SKILL.md` | Claude skill definition — trigger phrases, usage patterns |
| `package.json` / npm package | MCP server entry point, declares `bin` for npx |
| MCP server (JS/TS) | Implements MCP protocol, registers tools, calls four-leaf.ai |

### Dependencies

- **Runtime:** Node.js 18+, npx
- **Protocol:** MCP (stdio transport) — compatible with Claude Code, Claude Desktop
- **Backend:** four-leaf.ai API (no user-side API key required for basic queries)

### Data Flow

1. User types a natural-language prompt (e.g., "find me Python jobs in NYC").
2. Claude matches the SKILL.md trigger and selects the `job_search` MCP tool.
3. Claude sends a JSON-RPC `tools/call` message via stdio to the clover process.
4. The MCP server makes an HTTPS request to four-leaf.ai's search endpoint.
5. The response (job listings as JSON) is returned to Claude.
6. Claude formats the results conversationally and presents them to the user.

## Limitations

- **Voice mock interviews** are only available on the four-leaf.ai web platform, not through the MCP server.
- **Resume review** works on text input — it cannot parse PDF or DOCX files directly; you need to paste or extract the text first.
- **Job data freshness** depends on four-leaf.ai's aggregation pipeline; listings may lag real-time by hours.
- **Geographic coverage** is strongest for US tech roles; international coverage varies.
- **No write-back** — you cannot apply to jobs or submit resumes through the MCP tools; they are read-only intelligence tools.
- The MCP server requires an active internet connection to reach four-leaf.ai's API.

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|---|---|
| **Agent factories** | Shows the pattern of wrapping a vertical API as an MCP server that any Claude agent can consume — replicable for real estate, healthcare, legal, etc. |
| **Lead-gen / recruiting** | Job search + interview prep is a natural lead-gen funnel: free tool attracts candidates, premium features (voice mock, coaching) convert. |
| **Career coaching products** | Demonstrates how to package domain expertise (interview questions, resume scoring) as structured tool output rather than free-form chat. |
| **Skill + MCP combo pattern** | Illustrates the recommended pattern: SKILL.md for routing + MCP server for execution, keeping the skill lightweight and the server reusable across Claude surfaces (Code, Desktop, API). |
