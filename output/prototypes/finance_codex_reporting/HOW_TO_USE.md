# How to Use — Finance Codex Reporting

## Installation

No pip install needed. The implementation uses only Python 3 stdlib (`csv`, `io`, `json`, `collections`, `pathlib`).

```bash
git clone <this-repo>
cd finance_codex_reporting
bash run.sh
```

## Setting Up as a Claude Code Skill

This is a **Claude Code Skill**. To install it:

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/finance_codex_reporting
   ```

2. Copy the skill file:
   ```bash
   cp SKILL.md ~/.claude/skills/finance_codex_reporting/SKILL.md
   ```

3. Claude Code will now detect and activate this skill when you use trigger phrases.

### Trigger Phrases

Say any of these to Claude Code and the skill activates:

- "Build a monthly business review from this data"
- "Create a variance bridge between budget and actuals"
- "Generate a reporting pack for the board"
- "Audit this financial model for errors"
- "Run planning scenarios on these assumptions"
- "Show me budget vs actual analysis"
- "Prepare a variance analysis"

## First 60 Seconds

**Input:** Run the demo with mock FY26 Q1 data:

```bash
bash run.sh
```

**Output:** Four deliverables printed to terminal:

1. **MBR** — P&L summary by category (Revenue, COGS, OpEx), KPI table (gross margin, revenue growth, OpEx ratio), material variance commentary
2. **Variance Bridge** — Ordered waterfall from budget net income to actual net income, with drivers for each line item, reconciliation check
3. **Model Check** — Account mapping validation, sign convention audit, P&L reconciliation, circular reference scan, assumption audit (implied tax rate, COGS %)
4. **Planning Scenarios** — Bear/Base/Bull projections with annualized Q1 actuals, sensitivity analysis (+/- 1% revenue impact)

Plus a CSV export in `output/finance_data.csv` with all account-level data.

## Using with Real Data

When using the skill in Claude Code with your own data:

1. Provide a CSV or Excel file with columns: Account, Name, Budget, Actual
2. Tell Claude which deliverable you need (MBR, variance bridge, model check, or scenarios)
3. Optionally specify materiality thresholds (default: 5% or $50K)
4. Claude will parse, classify, compute variances, flag material items, and generate commentary
5. Review and edit the commentary — Claude drafts it, you confirm

## Output Formats

- Terminal: formatted tables and commentary
- CSV: `output/finance_data.csv` with all account-level detail
- The skill can also produce Markdown tables for embedding in reports
