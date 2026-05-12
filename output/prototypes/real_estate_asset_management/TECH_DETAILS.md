# Technical Details

## What It Does

This Claude Code skill provides structured analytical workflows for commercial real estate (CRE) and private equity (PE) asset management. When triggered, Claude follows a systematic framework to process property-level financial data and produce institutional-quality reporting: quarterly asset reviews (QARs), LP investor reports, rent roll analytics, T-12 operating statement analysis, direct-cap and DCF valuations, debt covenant monitoring, and hold/sell/refi disposition scoring.

The skill transforms raw property data (occupancy, rents, expenses, debt terms) into actionable output — scorecards with KPIs, risk flags, and strategy recommendations — following the same analytical steps an asset manager at a PE real estate fund would perform.

## Architecture

### Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The Claude Code skill definition (drop into `~/.claude/skills/`) |
| `asset_analyzer.py` | Core analysis engine — T-12, WALT, valuation, debt, hold/sell/refi |
| `portfolio_data.py` | Mock 3-property portfolio (Office, Multifamily, Industrial) |
| `run.sh` | End-to-end demo runner |

### Data Flow

```
User provides property data (rent roll, T-12, debt terms)
        │
        ▼
┌─────────────────────────────┐
│  Claude + Skill Framework   │
│  (structured prompts)       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  Analysis Steps:            │
│  1. Parse & normalize data  │
│  2. T-12 trending           │
│  3. Rent roll metrics       │
│  4. Valuation (cap rate)    │
│  5. Debt analysis           │
│  6. Hold/Sell/Refi scoring  │
└──────────────┬──────────────┘
               │
               ▼
    Formatted QAR / LP Report
```

### Dependencies

- **Runtime:** Python 3.10+ (stdlib only — no external packages)
- **Skill usage:** Claude Code with skills support (`~/.claude/skills/`)
- **No model calls in demo:** The Python demo uses pure computation; the skill itself guides Claude's reasoning at inference time

### Key Computations

- **WALT:** Weighted average lease term = Σ(SF × remaining years) / Σ(SF)
- **Concentration risk:** Tenant revenue share > 20% threshold
- **OpEx ratio:** Total operating expenses / effective gross income
- **DSCR:** NOI / annual debt service
- **LTV:** Loan balance / direct capitalization value
- **Hold/Sell/Refi scoring:** Multi-factor point system (occupancy gap, mark-to-market rent, capex deployment, WALT risk, appreciation, maturity proximity)

## Limitations

- **No live data feeds:** Does not connect to CoStar, Yardi, MRI, or any property management system. You must provide the data.
- **No DCF engine:** The demo uses direct capitalization only. Full DCF with year-by-year projections would require explicit assumption inputs.
- **No tax modeling:** Does not calculate depreciation recapture, 1031 eligibility, or promote waterfalls.
- **Skill is prompt-based:** The quality of output depends on Claude's reasoning — it's a structured guide, not deterministic software.
- **Single-point-in-time:** No historical trend database; each session starts fresh.

## Why It Matters for Claude-Driven Products

- **Agent factories:** This pattern — structured domain skill + data parsing + multi-step analysis — is directly transferable to building vertical AI agents for other asset classes (infrastructure, credit, venture).
- **Lead generation:** Real estate PE firms managing 10-50 assets spend 20+ hours per quarter on QAR preparation. An agent that drafts the first pass from raw data is immediately valuable.
- **Marketing/reporting:** LP-ready reports with consistent formatting, KPI dashboards, and executive summaries are a natural output for skill-guided Claude.
- **Voice AI:** The structured output format (scorecards, flags, recommendations) maps well to voice-driven portfolio review sessions where a fund manager asks "what are the risk flags this quarter?"
