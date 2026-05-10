# Technical Details: Overseas Sales Research Skill

## What it does

This is a prompt-engineering skill (SKILL.md) that instructs Claude Code to follow a structured 5-step research workflow — the 五看六定 (Five Perspectives, Six Decisions) framework used in Chinese B2B cross-border sales. When triggered, Claude uses web search MCP tools to gather real market data, then compiles findings into a standardized Markdown report covering industry analysis, market segmentation, competitive benchmarking, customer profiling, SWOT positioning, and a phased go-to-market plan with concrete KPIs.

The standalone demo (`generate_report.py`) replicates the report structure using curated mock data, showing the exact output format without requiring web access or API keys.

## Architecture

```
┌─────────────────────────────────────────────┐
│  SKILL.md  (prompt template)                │
│  - 5-step workflow instructions             │
│  - Output format specification              │
│  - Trigger phrase definitions               │
└──────────────┬──────────────────────────────┘
               │ loaded by Claude Code
               ▼
┌─────────────────────────────────────────────┐
│  Claude Code Agent                          │
│  Step 1: Gather inputs (company, market)    │
│  Step 2: Web search → Five Perspectives     │
│  Step 3: Synthesize → Six Decisions         │
│  Step 4: Compile Markdown report            │
│  Step 5: Review & refine with user          │
└──────────────┬──────────────────────────────┘
               │ writes
               ▼
   overseas_sales_research_<company>_<date>.md
```

### Key files

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill definition — prompt template with workflow steps, output format, and trigger phrases |
| `generate_report.py` | Standalone demo that renders the report structure from mock data (Python 3.10+, no deps) |
| `run.sh` | One-command demo runner |

### Data flow (live skill)

1. User provides company name, industry, market, and purpose
2. Claude performs 10-15 web searches across the five perspectives
3. Results are structured into the 五看六定 sections
4. Report is written as a Markdown file in the working directory
5. User reviews; Claude refines on request

### Data flow (demo)

1. `generate_report.py` loads hardcoded mock data for Siemens AG
2. Data is formatted into Markdown tables, bullet lists, and structured sections
3. Report is written to disk and previewed in the terminal

### Dependencies

- **Live skill:** Claude Code with web search capability (no additional packages)
- **Demo:** Python 3.10+ standard library only (argparse, datetime, json, re)

## Limitations

- **No real-time data in demo mode.** The standalone script uses mock data; only the Claude Skill with web search produces live research.
- **Single company per report.** The framework is designed for one target company at a time. Multi-company comparison requires running the skill multiple times.
- **English and Chinese only.** The report template supports bilingual (zh) or English (en) output. Other languages are not templated.
- **No financial modeling.** Revenue projections and KPIs in the "Six Decisions" section are qualitative estimates, not financial models.
- **Web search depth varies.** Report quality depends on what Claude can find via web search. Private companies or niche markets may have sparse public data.
- **No CRM integration.** Reports are standalone Markdown files — there's no automatic sync to Salesforce, HubSpot, or other CRM systems.

## Why it matters

For teams building Claude-driven products in these areas:

- **Lead-gen & sales enablement:** The 五看六定 framework is a proven B2B research methodology. This skill turns Claude into a sales analyst that produces stakeholder-ready reports — useful for building automated prospect research pipelines.
- **Agent factories:** Demonstrates how a single SKILL.md file can encode a complex multi-step workflow (research → analysis → synthesis → structured output) without any code. Good pattern for creating domain-specific research agents.
- **Marketing & competitive intelligence:** The competitor benchmarking tables and market segmentation analysis can feed into marketing strategy tools or competitive dashboards.
- **Cross-border commerce:** Purpose-built for international B2B scenarios — handles multi-market analysis, regulatory considerations, and localized go-to-market planning that general-purpose research tools miss.
