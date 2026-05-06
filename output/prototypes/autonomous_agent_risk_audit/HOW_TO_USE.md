# How to Use

## Install

```bash
git clone <this-repo>
cd autonomous_agent_risk_audit
# No dependencies -- Python 3.8+ stdlib only
```

## Run the demo

```bash
bash run.sh
```

This runs two built-in scenarios (dangerous AI cafe vs. safe inventory assistant) and prints a side-by-side risk comparison.

## Audit your own agent

Create a JSON file describing your agent (see `example_agent.json` for the schema):

```bash
python3 audit_agent.py example_agent.json
```

Add `--json` to write machine-readable results to `audit_results.json`:

```bash
python3 audit_agent.py example_agent.json --json
```

### JSON spec format

```json
{
  "name": "My Agent",
  "description": "What the agent does",
  "capabilities": ["Order supplies", "Send emails to vendors"],
  "external_touchpoints": ["Supplier API", "Email system"],
  "has_human_approval": {"Send emails to vendors": true},
  "quantity_limits": {"Order supplies": "max 2x weekly average"},
  "logging_enabled": true,
  "override_log": false
}
```

## Use as a Claude Code Skill

Drop the skill folder into your Claude Code skills directory:

```bash
cp -r SKILL.md ~/.claude/skills/autonomous_agent_risk_audit/SKILL.md
```

### Trigger phrases

- "Review my autonomous agent for real-world risks"
- "What guardrails should I add to my AI that places orders?"
- "Audit my agentic system for ethical issues with third parties"
- "How do I prevent my agent from spamming external contacts?"
- "Design safety limits for an AI that manages inventory"

When triggered, Claude will walk through the 6-step audit process from the skill definition: identify external touchpoints, apply the consent boundary test, set quantity guardrails, implement an override log, run the checklist, and verify ethical red lines.

## First 60 seconds

```
$ bash run.sh

======================================================================
  AUTONOMOUS AGENT RISK AUDIT TOOL
  Inspired by: 'Our AI started a cafe in Stockholm'
======================================================================

>>> SCENARIO 1: AI Cafe Manager (no guardrails)

======================================================================
  AUTONOMOUS AGENT RISK AUDIT REPORT
  Agent: AI Cafe Manager (Stockholm)
======================================================================

  Risk Score: 100/100 | Grade: F - DO NOT DEPLOY
  Findings: 14 | Checklist: 0/7 passed

  Risk: [########################################] 100/100

----------------------------------------------------------------------
  AUDIT CHECKLIST
----------------------------------------------------------------------
  [FAIL] No EMERGENCY emails without human approval
  [FAIL] No autonomous government/legal submissions
  [FAIL] Quantity limits on all ordering capabilities
  [FAIL] All external comms have human-in-the-loop
  [FAIL] Irreversible actions require confirmation
  [FAIL] Action logging enabled
  [FAIL] Override/escalation log ('Hall of Shame') active

  ... (14 detailed findings with recommendations) ...

>>> SCENARIO 2: Inventory Assistant (with guardrails)

  Risk Score: 0/100 | Grade: A - Low risk
  Findings: 0 | Checklist: 7/7 passed
```
