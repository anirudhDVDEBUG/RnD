# How to Use — Small Business Ops Skill

## This is a Claude Code Skill

It is **not** an MCP server or standalone CLI. It's a prompt-based skill that tells Claude *how* to orchestrate your connected business tools.

## Installation

### 1. Drop the skill file

```bash
mkdir -p ~/.claude/skills/small_business_ops
cp SKILL.md ~/.claude/skills/small_business_ops/SKILL.md
```

### 2. Configure MCP connectors

The skill needs at least one business tool connected via MCP. Add connectors to `~/.claude.json`:

```json
{
  "mcpServers": {
    "quickbooks": {
      "command": "npx",
      "args": ["-y", "@anthropic/qbo-mcp-server"],
      "env": { "QBO_CLIENT_ID": "...", "QBO_CLIENT_SECRET": "..." }
    },
    "stripe": {
      "command": "npx",
      "args": ["-y", "@anthropic/stripe-mcp-server"],
      "env": { "STRIPE_SECRET_KEY": "sk_..." }
    },
    "hubspot": {
      "command": "npx",
      "args": ["-y", "@anthropic/hubspot-mcp-server"],
      "env": { "HUBSPOT_API_KEY": "..." }
    },
    "gmail": {
      "command": "npx",
      "args": ["-y", "@anthropic/gmail-mcp-server"],
      "env": { "GMAIL_OAUTH_TOKEN": "..." }
    }
  }
}
```

> **Note:** The exact MCP server packages depend on what's available. The skill works with whatever subset of connectors you have — it adapts to available tools.

### 3. (Optional) Add business context

Create a `CLAUDE.md` in your working directory:

```markdown
# My Business Context
- Business: Acme Consulting, B2B services
- Invoice terms: Net 30
- Key accounts: BigCorp, MediumCo, StartupX
- Payroll: Bi-weekly, Fridays
- Revenue target: $25K/month
```

## Trigger Phrases

Say any of these to Claude Code to activate the skill:

| Phrase | Workflow |
|--------|----------|
| "Run my Monday brief" | Monday Brief |
| "Chase outstanding invoices" | Invoice Chase |
| "Help me close the month" | Close Month |
| "Plan payroll for this period" | Plan Payroll |
| "Generate my call list" | Call List |
| "Handle this customer complaint" | Handle Complaint |
| "Plan a marketing campaign" | Run Campaign |
| "Create my Friday brief" | Friday Brief |
| "Run quarterly review" | Quarterly Review |
| "Clean up my CRM" | CRM Maintenance |

## First 60 Seconds

**Without MCP connectors** (demo mode):

```bash
# Clone this repo and run the demo
bash run.sh
```

Output: all 10 workflows run against mock data — Monday brief, invoice chase emails, P&L snapshot, payroll calc, call list, complaint draft, campaign plan, Friday summary, quarterly board report, CRM dedup.

**With MCP connectors** (real mode):

```
You: Run my Monday brief

Claude: Pulling data from QuickBooks and HubSpot...

  MONDAY BRIEF — May 22, 2026
  Revenue this week: $5,980
  3 overdue invoices totaling $8,900
  Top opportunity: Sarah Chen ($12K, negotiation stage)

  Priorities:
  1. Chase overdue invoices
  2. Follow up with Sarah Chen
  3. Prepare payroll

  Shall I draft chase emails for the overdue invoices?
```

## Individual Workflows

Run a single workflow from the demo:

```bash
python3 small_business_ops.py monday     # Monday Brief only
python3 small_business_ops.py chase      # Invoice Chase only
python3 small_business_ops.py close      # Month-End Close
python3 small_business_ops.py payroll    # Payroll Planning
python3 small_business_ops.py calls      # Call List
python3 small_business_ops.py complaint  # Complaint Handler
python3 small_business_ops.py campaign   # Campaign Planner
python3 small_business_ops.py crm        # CRM Maintenance
python3 small_business_ops.py friday     # Friday Brief
python3 small_business_ops.py quarterly  # Quarterly Review
python3 small_business_ops.py all        # Everything
```
