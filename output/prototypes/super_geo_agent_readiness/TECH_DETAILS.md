# Technical Details

## What It Does

Super GEO & Agent Readiness is a Claude Code skill that teaches Claude how to audit and optimize websites for **Generative Engine Optimization (GEO)** -- the practice of making your content citable by AI systems like ChatGPT, Perplexity, and Google AI Overviews. It also checks **agent readiness**: whether AI agents can discover, authenticate with, and interact with your service via MCP, OAuth, and structured data.

The included Python auditor (`geo_audit.py`) implements the same checklist as a standalone CLI tool, scanning a local directory that mirrors a site's file structure and producing a scored report with actionable recommendations.

## Architecture

```
geo_audit.py          # Main auditor: 8 checks, scoring, report output
sample_site/          # Mock website with all GEO signals in place
  llms.txt            # AI-readable site summary (llmstxt.org spec)
  robots.txt          # AI bot access control
  sitemap.xml         # Content discovery
  index.html          # Page with Schema.org JSON-LD + quality signals
  .well-known/
    mcp.json          # MCP tool manifest for agent discovery
    oauth-authorization-server   # OAuth 2.0 metadata
SKILL.md              # Claude Code skill definition
run.sh                # Demo runner (two-pass: good site vs bare site)
```

**Data flow:** `run.sh` -> `geo_audit.py` reads files from `sample_site/` (or any directory) -> runs 8 independent checks -> aggregates scores -> prints table + recommendations.

**Dependencies:** Python 3.8+ standard library only (`json`, `re`, `pathlib`, `dataclasses`). No network calls, no API keys, no external packages.

**Model calls:** None. The standalone auditor is pure Python. When used as a Claude skill, Claude itself performs the audit logic guided by the SKILL.md instructions -- no additional LLM API calls are made beyond the Claude session.

## The 8 Checks

| # | Check | What It Validates |
|---|-------|-------------------|
| 1 | llms.txt | Presence, heading, description block, doc links |
| 2 | llms-full.txt | Presence and content depth |
| 3 | MCP manifest | Valid JSON at `/.well-known/mcp.json` with tools + name |
| 4 | Schema.org | JSON-LD blocks in HTML; AI-useful types (FAQPage, HowTo, Article, etc.) |
| 5 | robots.txt | AI bots (GPTBot, PerplexityBot, ClaudeBot, etc.) not blocked |
| 6 | OAuth discovery | `/.well-known/oauth-authorization-server` with issuer + endpoints |
| 7 | sitemap.xml | Presence and URL count |
| 8 | Content quality | Q&A headings, lists, tables, citations in HTML |

## Limitations

- **Static file analysis only.** The auditor reads files from a local directory, not from a live URL. It does not make HTTP requests, follow redirects, or render JavaScript.
- **Heuristic scoring.** Checks use regex and simple JSON parsing, not full HTML DOM parsing or semantic analysis. Edge cases (e.g., nested JSON-LD, dynamically injected structured data) may be missed.
- **No crawler simulation.** It does not verify that Googlebot or GPTBot can actually reach your pages -- just that `robots.txt` allows them.
- **No content semantic evaluation.** It checks for structural signals (lists, tables, citations) but does not evaluate whether the content itself is factually useful or authoritative.
- **Skill is guidance, not automation.** The SKILL.md tells Claude *what* to check and *how* to fix it, but Claude still depends on the user providing site context or files.

## Why It Matters for Claude-Driven Products

- **Lead-gen / marketing sites:** GEO is the new SEO. If your landing pages aren't structured for AI extraction, you're invisible to the growing share of traffic that comes through AI-generated answers. This skill automates the audit.
- **Agent factories:** If you're building services that AI agents consume, MCP manifests and OAuth discovery are table-stakes. This checks both.
- **Ad creatives / content teams:** The content quality checks align with what AI systems actually extract -- Q&A format, statistical claims with sources, structured tables -- which also happen to be what converts.
- **Voice AI:** Voice assistants powered by LLMs pull from the same AI-cited sources. GEO optimization feeds directly into voice search visibility.
