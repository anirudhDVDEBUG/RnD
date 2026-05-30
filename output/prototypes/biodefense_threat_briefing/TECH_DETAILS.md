# Technical Details

## What it does

This prototype generates structured biodefense threat briefings modeled on the intelligence-briefing format used by public health agencies and biosecurity organizations. It ships with curated mock threat data (H5N1, Mpox Clade Ib, C. auris, dual-use research risks, AI-enabled bio risks) and produces a complete Markdown briefing covering the threat landscape, surveillance posture, preparedness scorecard, and prioritized action recommendations.

The concept is inspired by [Rosalind Biodefense](https://openai.com/index/strengthening-societal-resilience-with-rosalind-biodefense), which applies AI to strengthen pandemic preparedness. This skill brings a similar structured-output approach into the Claude Code workflow — letting analysts generate, customize, and iterate on briefings conversationally.

## Architecture

```
generate_briefing.py    — Single-file generator (stdlib only)
  |
  +-- MOCK_THREATS      — Embedded threat intel data (dict)
  |     +-- natural[]        Pathogen entries with confidence/trend/source
  |     +-- engineered[]     Dual-use and emerging tech threats
  |     +-- surveillance{}   Strengths and gaps
  |     +-- preparedness[]   Domain-by-domain scorecard
  |
  +-- generate_briefing()  — Assembles Markdown from data
  +-- main()               — CLI with argparse (scope/audience/format/output)

SKILL.md                — Claude Code skill definition (drop into ~/.claude/skills/)
run.sh                  — Demo runner
```

### Data flow

1. CLI args or Claude skill context set scope, audience, and focus
2. `generate_briefing()` pulls from the embedded `MOCK_THREATS` dictionary
3. Briefing sections are templated into Markdown with confidence tags and source attribution
4. Output goes to stdout, a file, or JSON (for pipeline consumption)

### Dependencies

- **Python 3.8+** (stdlib only — `json`, `argparse`, `datetime`, `pathlib`)
- No external packages, no API keys, no network calls

### Where an LLM fits in

In a production version, Claude would:
- Ingest real-time feeds (WHO DON, CDC MMWR, ProMED, GISAID) via MCP or tool use
- Synthesize free-text intelligence into the structured template
- Adjust tone and detail level for the specified audience
- Generate follow-up analysis on request ("drill into H5N1 dairy cattle timeline")

The current prototype uses static mock data so it runs without API keys.

## Limitations

- **Static data only** — Threat intelligence is hardcoded mock data, not live feeds
- **No LLM synthesis** — The briefing is template-assembled, not AI-generated prose
- **US-centric defaults** — Mock data focuses on US threats; easily extensible
- **No classification handling** — Marked UNCLASSIFIED; no real classification infrastructure
- **No PDF/PPTX export** — Outputs Markdown; use `pandoc` for conversion

## Why it matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | Skill demonstrates a structured-output pattern: take context params, produce a formatted deliverable. Same pattern works for any domain briefing (market intel, competitive analysis, regulatory updates). |
| **Lead-gen / marketing** | Public health orgs, defense contractors, and biotech firms need automated briefing tools. This is a vertical-specific skill template. |
| **Voice AI** | Briefing structure (executive summary + details + actions) maps well to voice-delivered intelligence summaries. |
| **MCP integration** | Natural extension: connect to WHO/CDC RSS feeds via an MCP server, replace mock data with live intel, and generate real-time briefings. |
