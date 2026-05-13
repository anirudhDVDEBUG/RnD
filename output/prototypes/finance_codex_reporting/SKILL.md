---
name: finance_codex_reporting
description: >
  Build finance reporting artifacts — MBRs, reporting packs, variance bridges,
  model checks, and planning scenarios — using structured AI-driven workflows.
  TRIGGER: user mentions monthly business review, variance analysis, reporting pack,
  financial model audit, budget vs actual, or planning scenarios.
---

# Finance Codex Reporting Skill

Automate and accelerate finance team deliverables: monthly business reviews (MBRs),
reporting packs, variance bridge analyses, model integrity checks, and forward-looking
planning scenarios.

## When to use

- "Build a monthly business review from this data"
- "Create a variance bridge between budget and actuals"
- "Generate a reporting pack for the board"
- "Audit this financial model for errors"
- "Run planning scenarios on these assumptions"

## How to use

### 1. Gather Inputs

Collect the raw finance data the user provides. Typical inputs include:
- Trial balance or GL exports (CSV, Excel)
- Budget / forecast files
- Prior period actuals for comparison
- Chart of accounts or mapping tables
- Narrative context (business drivers, one-offs)

Ask the user which deliverable they need:
| Deliverable | Key output |
|---|---|
| MBR | P&L summary, KPI table, commentary |
| Reporting pack | Multi-tab structured report with exec summary |
| Variance bridge | Waterfall of budget → actual with drivers |
| Model check | Error log, circular-ref scan, assumption audit |
| Planning scenarios | Base / bull / bear cases with sensitivity table |

### 2. Structure the Analysis

1. **Parse & validate** — Load data, confirm column mappings, flag missing accounts.
2. **Classify line items** — Map to standard categories (Revenue, COGS, OpEx, CapEx, etc.).
3. **Compute variances** — Calculate period-over-period and budget-vs-actual deltas (absolute and %).
4. **Identify materiality** — Flag variances exceeding a user-defined threshold (default: 5% or $50K).
5. **Generate commentary** — For each material variance, draft a plain-English driver explanation and prompt the user to confirm or edit.

### 3. Produce the Deliverable

- Output tables in Markdown or CSV.
- For variance bridges, produce a waterfall-style ordered list from starting balance to ending balance.
- For model checks, output a structured error/warning log with cell references or line numbers.
- For planning scenarios, present a side-by-side comparison table with clearly labeled assumptions.

### 4. Quality Checks

- Verify totals reconcile (e.g., sum of bridge items equals total variance).
- Cross-check P&L net income to balance sheet retained earnings movement if both are available.
- Flag any unclassified or suspense-account balances.

## Example: Variance Bridge

```
Starting point: FY26 Q1 Budget Revenue = $12.0M

+ Volume uplift:        +$800K   (unit volumes 7% above plan)
- Price erosion:        -$200K   (competitive discounting in EMEA)
+ New product launch:   +$350K   (Product X ahead of schedule)
- FX headwind:          -$150K   (EUR/USD moved from 1.10 to 1.07)
= Actual Revenue:       $12.8M   (variance: +$800K / +6.7%)
```

## References

- Source: [How finance teams use Codex — OpenAI](https://openai.com/academy/how-finance-teams-use-codex)
