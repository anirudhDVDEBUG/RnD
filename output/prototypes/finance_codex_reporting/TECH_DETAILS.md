# Technical Details — Finance Codex Reporting

## What It Does

This skill codifies the finance reporting workflows described in OpenAI's "How finance teams use Codex" into a structured Claude Code skill. Rather than ad-hoc prompting, it provides a repeatable pipeline: ingest chart of accounts + budget/actuals, classify line items into standard categories (Revenue, COGS, OpEx, CapEx), compute variances with materiality flags, and produce four distinct deliverables — MBRs, variance bridges, model integrity checks, and planning scenarios.

The key insight from the source material is that finance teams get the most value from AI when the workflow is structured (parse → classify → compute → narrate) rather than open-ended. This skill encodes that structure so Claude follows a consistent process every time.

## Architecture

### Key Files

| File | Purpose |
|---|---|
| `finance_codex.py` | Core implementation — all deliverable generators, mock data, CSV export |
| `SKILL.md` | Claude Code skill definition with triggers and workflow instructions |
| `run.sh` | Entry point — runs the demo end-to-end |

### Data Flow

```
Input (CSV/manual) → Parse & validate accounts
                   → Map to standard categories (Revenue, COGS, OpEx, etc.)
                   → Compute variances (absolute + %)
                   → Apply materiality filter (5% or $50K threshold)
                   → Generate deliverable (MBR / bridge / check / scenarios)
                   → Output (terminal tables + CSV)
```

### Dependencies

- **Python 3.6+** (stdlib only: `csv`, `io`, `json`, `collections`, `pathlib`)
- No external packages, no API keys, no database

### Model Calls

The demo itself makes **zero LLM API calls** — it's pure computation on structured data. When used as a Claude Code skill, Claude provides:
- Natural language commentary for material variances
- Interactive refinement of driver explanations
- Flexible response to follow-up questions ("drill into marketing spend")

## Limitations

- **Mock data only in demo** — real use requires the user to provide CSV/Excel with actual financials
- **No Excel output** — produces Markdown tables and CSV, not .xlsx workbooks
- **No chart generation** — variance bridges are text-based waterfalls, not visual charts
- **Single-currency** — no multi-currency consolidation or FX translation
- **No balance sheet** — focuses on P&L; BS cross-checks mentioned but not implemented
- **Commentary is templated in demo** — in live skill use, Claude generates contextual narratives
- **No GAAP/IFRS validation** — classifies by chart of accounts, doesn't enforce accounting standards

## Why It Matters for Claude-Driven Products

**Agent factories:** This skill demonstrates a pattern for building domain-specific finance agents. The structured workflow (parse → classify → compute → narrate) is reusable — swap finance data for marketing spend data or ad performance data and the same pipeline applies.

**Lead-gen / marketing:** Finance teams are high-value buyers of AI tools. A working demo of automated MBR generation or variance analysis is a compelling proof point for selling AI services to CFO offices.

**Voice AI:** The structured output (KPI tables, variance commentary) is well-suited for voice-driven dashboards — "What were the material variances this quarter?" can be answered directly from the MBR output.

**Ad creatives:** The planning scenarios (bear/base/bull) demonstrate multi-scenario analysis — the same pattern applies to ad spend optimization across budget scenarios.
