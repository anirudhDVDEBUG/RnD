# Technical Details — Equity Research Agent

## What It Does

The Equity Research Agent is a Claude Code skill that transforms Claude into a structured equity-research analyst. When a user asks to analyze a stock, the skill instructs Claude to execute a multi-step pipeline: gather financial data (via MCP server or web search), run 8 analysis modules (income statement, balance sheet, cash flow, ratios, DCF, comps, risk, catalysts), and synthesize results into a formatted research report with a buy/hold/sell rating and price target range.

The skill's key innovation is its **personalization layer** — it adapts output depth and terminology to three investor levels (beginner/intermediate/advanced), making the same underlying analysis accessible to different audiences.

## Architecture

```
User prompt ("analyze NVDA")
        │
        ▼
┌─────────────────────┐
│  SKILL.md trigger    │  ← Claude matches intent to skill
│  (pattern matching)  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Data Collection     │  ← MCP server (live) or web search (fallback)
│  - Financials        │
│  - SEC filings       │
│  - Market data       │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Analysis Pipeline   │  ← 8 modules, executed sequentially
│  1. Income stmt      │
│  2. Balance sheet    │
│  3. Cash flow        │
│  4. Ratio analysis   │
│  5. DCF valuation    │
│  6. Comparable cos   │
│  7. Risk assessment  │
│  8. Catalyst ID      │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Report Synthesis    │  ← Personalized to investor level
│  - Executive summary │
│  - Rating + target   │
│  - Disclaimer        │
└─────────────────────┘
```

### Key Files (Source Repo)

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill definition — triggers, analysis steps, output format |
| `skills/*.md` | 24 individual analysis skill files (modular) |
| `mcp_server/server.py` | Optional MCP server for live financial data |
| `config/personas.yml` | Investor-level personalization templates |

### Key Files (This Demo)

| File | Purpose |
|------|---------|
| `equity_research.py` | Self-contained demo with mock data + all 8 analysis modules |
| `run.sh` | Runs three demo scenarios end-to-end |
| `SKILL.md` | The skill file you'd install into `~/.claude/skills/` |

## Dependencies

- **Demo**: Python 3.8+ (stdlib only — no pip packages needed)
- **Full skill**: Claude Code with skill support, optionally an MCP financial data server
- **Model calls**: The skill itself doesn't make API calls — Claude Code does the LLM reasoning. The skill is a prompt template that guides Claude's analysis structure.

## Data Flow

1. **Skill trigger**: Claude reads `SKILL.md` and recognizes the user's intent matches a trigger pattern
2. **Data gathering**: Claude uses its available tools (MCP server, web search, file read) to collect financial data
3. **Analysis**: Claude follows the step-by-step analysis instructions in the skill, producing each section
4. **Personalization**: Output depth adjusts based on the user's stated or inferred experience level
5. **Disclaimer**: Every report includes an AI-generated-analysis disclaimer

## Limitations

- **No real-time data in demo**: The demo uses hardcoded mock financials. Live data requires the MCP server or Claude's web search.
- **No SEC filing parsing**: The skill instructs Claude to review filings, but doesn't include an EDGAR parser. Claude relies on web search or pre-fetched filing text.
- **DCF is simplified**: The valuation model uses a basic 5-year single-stage DCF. No WACC build-up from CAPM, no explicit working-capital adjustments.
- **No portfolio-level analysis**: Analyzes individual stocks or small comparisons — not portfolio optimization or correlation analysis.
- **Data freshness**: When using web search for data, results may lag real-time by hours or days.
- **Not financial advice**: AI-generated analysis with no fiduciary responsibility.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent factories** | Shows how a single SKILL.md file can turn Claude into a domain expert — same pattern works for legal research, medical literature review, competitive intelligence |
| **Lead-gen / marketing** | Financial content generation at scale: earnings previews, sector reports, stock comparisons for fintech newsletters |
| **MCP ecosystem** | Demonstrates the skill + MCP server pattern: structured prompts paired with a data tool, composable and swappable |
| **Personalization** | The beginner/intermediate/advanced layer is a reusable pattern for adapting any agent output to audience expertise |
| **Structured output** | The report format (tables, ratings, ranges) shows how to get consistent, parseable output from Claude without fine-tuning |
