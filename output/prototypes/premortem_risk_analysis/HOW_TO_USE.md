# How to Use — Premortem Risk Analysis

## What this is

A **Claude Code skill** (not an MCP server). It gives Claude structured instructions for running a premortem analysis whenever you ask. No Python dependencies are needed for the skill itself — the demo script uses only stdlib.

## Install the skill

```bash
# Clone the source repo
git clone https://github.com/AndyShaman/premortem.git

# Copy the skill file into Claude Code's skills directory
mkdir -p ~/.claude/skills/premortem_risk_analysis
cp premortem/SKILL.md ~/.claude/skills/premortem_risk_analysis/SKILL.md
```

Or copy the `SKILL.md` from this prototype directory directly:

```bash
mkdir -p ~/.claude/skills/premortem_risk_analysis
cp SKILL.md ~/.claude/skills/premortem_risk_analysis/SKILL.md
```

That's it. No `pip install`, no `npm install`, no API keys.

## Trigger phrases

Once the skill is installed, say any of these in Claude Code:

| Phrase | What happens |
|---|---|
| `premortem` or `pre-mortem` | Full 6-step premortem analysis |
| `what could go wrong` | Same — triggers prospective hindsight |
| `find the failure modes` | Scans for risks across 5 dimensions |
| `stress-test this architecture` | Multi-agent silent scan |
| `find the risks` / `find the blind spots` | Mitigation triplets + reverse-premortem |

## First 60 seconds

1. Install the skill (above).
2. Open Claude Code in a project with a plan, architecture doc, or just describe your plan in chat.
3. Type:

```
Run a premortem on our plan to migrate the billing service to Kafka.
```

4. Claude will:
   - Frame the plan from your codebase/conversation context
   - Imagine the plan failed spectacularly 6 months from now
   - Scan 5 dimensions (Technical, Integration, Operational, Human/Process, External/Market)
   - Apply 5 reviewer personas (Devil's Advocate, Pessimist, Security Auditor, Ops Engineer, End User)
   - Output ranked mitigation triplets (Risk / Likelihood / Mitigation)
   - Run a reverse-premortem ("what if it succeeded wildly?")
   - Offer to save a snapshot to `docs/premortem-YYYY-MM-DD.md`

**Example output** (abbreviated):

```
## Premortem Summary — Billing Migration — 2026-05-10

### Top Risks (ranked)
1. **Message ordering breaks invoice sequencing** — Likelihood: High, Impact: High
   - Mitigation: Enforce deterministic partition keys, add idempotency tokens...

2. **Payment gateway webhook replay floods consumer** — Likelihood: High, Impact: High
   - Mitigation: Deduplication layer using event ID + idempotency key in Redis...

### Assumptions That Must Hold
- Kafka throughput handles 10x peak without horizontal scaling
- Stripe webhook contract remains stable for 12+ months

### Recommended Actions Before Committing
- [ ] Write and drill Kafka incident runbook before go-live
- [ ] Implement idempotency + deduplication layer in week 1
```

## Running the demo (no Claude needed)

```bash
bash run.sh
```

This runs `premortem_demo.py` which simulates the full pipeline on a sample plan using mock data. Outputs:
- Console report with color-coded risk rankings
- `premortem_snapshot.md` — markdown report
- `premortem_snapshot.json` — structured JSON for programmatic use
