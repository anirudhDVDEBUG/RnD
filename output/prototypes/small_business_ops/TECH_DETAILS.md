# Tech Details — Small Business Ops Skill

## What It Does

This is a **Claude Code skill** (a structured prompt in `SKILL.md`) that teaches Claude how to run 10 weekly operational workflows for small businesses. When a user says "run my Monday brief," Claude reads the skill, identifies which workflow to execute, then queries the user's connected business tools (QuickBooks, Stripe, HubSpot, Gmail) through MCP connectors to pull live data, generate reports, draft emails, and update records.

The skill itself contains no code — it's a prompt template that Claude interprets at runtime. The Python demo in this repo (`small_business_ops.py`) simulates what Claude would produce by running the same workflows against mock data.

## Architecture

```
User prompt ("Run my Monday brief")
       │
       ▼
Claude Code reads SKILL.md
       │
       ▼
Claude identifies workflow → Monday Brief
       │
       ├──► MCP: QuickBooks → open invoices, revenue
       ├──► MCP: Stripe/PayPal → recent payments
       ├──► MCP: HubSpot → pipeline, top deals
       └──► MCP: Gmail → calendar, pending emails
       │
       ▼
Claude assembles prioritized brief
       │
       ▼
User reviews → approves actions (send emails, update CRM)
```

### Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The actual skill — drop into `~/.claude/skills/small_business_ops/` |
| `small_business_ops.py` | Demo: 10 workflows with mock data, CLI interface |
| `run.sh` | One-command demo runner |

### Data Flow

1. **Input:** Natural language trigger (e.g., "chase overdue invoices")
2. **Skill match:** Claude matches trigger phrases in SKILL.md description
3. **MCP queries:** Claude calls connected tool APIs via MCP protocol
4. **Processing:** Claude aggregates, calculates, and formats data
5. **Output:** Structured report + draft actions (emails, CRM updates)
6. **Human-in-the-loop:** User approves before Claude executes write operations

### Dependencies

- **Runtime:** Claude Code with MCP connectors configured
- **Demo:** Python 3.8+ (standard library only — no pip packages)
- **MCP servers:** QuickBooks, Stripe, PayPal, Square, HubSpot, Gmail (any subset works)

## Limitations

- **No standalone execution.** The skill is a prompt, not a program. It requires Claude Code + MCP connectors to work with real data.
- **MCP connector availability.** Not all business tools have official MCP servers yet. The skill adapts to whatever connectors are present, but some workflows need specific tools (e.g., Invoice Chase needs accounting + email).
- **No persistent state.** The skill doesn't maintain its own database. Each run queries live data from connected tools. There's no week-over-week trending unless the user's tools provide historical views.
- **Approval required for writes.** The skill drafts emails and CRM updates but doesn't auto-send. This is by design (human-in-the-loop), but it means it's not fully autonomous.
- **Mock data only in demo.** The Python script shows the *format* of outputs, not real business data. The numbers are illustrative.

## Why This Matters

**For Claude-driven product builders:**

- **Agent factories:** This is a template for vertical-specific agent skills. The same pattern (SKILL.md + MCP connectors + structured workflows) applies to legal ops, healthcare admin, real estate management, or any domain with SaaS tools that expose APIs.
- **Lead-gen / marketing:** The campaign planner and CRM maintenance workflows show how Claude can segment audiences, draft outreach, and maintain pipeline hygiene — all from natural language.
- **Small business SaaS play:** There's a market for "Claude as your ops assistant" — a wrapper that pre-configures MCP connectors for common SMB stacks (QBO + Stripe + HubSpot) and ships with this skill pre-loaded.
- **Recurring automation:** Combined with `/schedule`, these workflows become a lightweight alternative to Zapier/Make for businesses that want AI-generated summaries, not just data piping.
