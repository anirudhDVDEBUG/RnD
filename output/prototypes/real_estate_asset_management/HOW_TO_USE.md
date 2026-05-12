# How to Use

## Installation

This is a **Claude Code skill** — no pip install or npm required. You just drop the skill file into your Claude Code skills directory.

### Step 1: Install the skill

```bash
mkdir -p ~/.claude/skills/real_estate_asset_management
cp SKILL.md ~/.claude/skills/real_estate_asset_management/SKILL.md
```

Or clone from source:

```bash
git clone https://github.com/rubyh218/real-estate-asset-management.git
cp real-estate-asset-management/SKILL.md ~/.claude/skills/real_estate_asset_management/SKILL.md
```

### Step 2: Verify

Claude Code automatically loads skills from `~/.claude/skills/`. No restart needed — the skill activates on the next message matching a trigger phrase.

## Trigger Phrases

The skill activates when you mention any of:

- "Prepare a quarterly asset review"
- "Generate an LP report"
- "Run a T-12 analysis"
- "Analyze this rent roll"
- "Property valuation"
- "Debt maturity monitoring"
- "Hold vs. sell vs. refinance"
- "Commercial real estate portfolio management"

## First 60 Seconds

1. Drop the skill file (above).
2. Open Claude Code and type:

```
Prepare a quarterly asset review for my portfolio. Here's the data:

Property: 123 Main St Office Tower
- 150,000 SF, 88% occupied (budget 92%)
- In-place NOI: $3.2M (budget $3.5M)
- Top tenant: Acme Corp, 45,000 SF, lease expires Dec 2025
- Debt: $25M @ 5.5%, matures June 2026
- T-12 revenue: $4.8M, OpEx: $1.6M
```

3. Claude responds with a structured scorecard including:
   - Occupancy variance analysis
   - WALT and rollover exposure
   - Debt metrics (DSCR, LTV) with flags
   - Valuation sensitivity (cap rate +/- 50bps)
   - Hold/Sell/Refi recommendation with scoring

## Running the Demo Locally

To see the analysis engine in action with mock data:

```bash
bash run.sh
```

This produces a full Quarterly Asset Review report for a 3-property portfolio (Office, Multifamily, Industrial) — no API keys or external services needed.

## What the Skill Does NOT Do

- It does not call external APIs or property databases
- It does not store or persist data between sessions
- It does not replace audited financial reporting
- It relies on you providing accurate source data (rent rolls, T-12s, debt terms)
