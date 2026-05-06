# Technical Details

## What it does

This is a static rule-based audit engine that analyzes an autonomous AI agent's design specification -- its capabilities, external touchpoints, human approval gates, and quantity limits -- and produces a structured risk report. It does not require API keys or LLM calls; the audit logic is deterministic and runs instantly against a JSON agent spec.

The tool codifies lessons from real autonomous agent deployments, particularly the [AI cafe experiment in Stockholm](https://simonwillison.net/2026/May/5/our-ai-started-a-cafe-in-stockholm/) where an AI agent autonomously ordered 120 eggs (no stove), 6,000 napkins, sent multiple "EMERGENCY" emails to suppliers, and applied for government permits with AI-generated floor plans.

## Architecture

```
audit_agent.py          -- Single-file implementation, no external deps
  |
  +-- AgentSpec          -- Dataclass: agent name, capabilities, touchpoints,
  |                         approval gates, quantity limits, logging config
  +-- Finding            -- Dataclass: category, severity, title, description,
  |                         recommendation, affected capability
  +-- AuditReport        -- Dataclass: findings, checklist, risk score, summary
  |
  +-- Rule functions:
  |     check_consent_boundary()     -- External comms without consent
  |     check_urgency_escalation()   -- EMERGENCY/urgent without approval
  |     check_quantity_guardrails()  -- Ordering without limits
  |     check_irreversible_actions() -- Sign/submit/delete without confirmation
  |     check_legal_regulatory()     -- Government/legal without oversight
  |     check_missing_guardrails()   -- Systemic gaps (logging, override log)
  |
  +-- build_checklist()              -- 7-item pass/fail checklist
  +-- calculate_risk_score()         -- Weighted severity -> 0-100 score
  +-- format_report()                -- Human-readable text output

example_agent.json      -- Sample custom agent spec for testing
SKILL.md                -- Claude Code skill definition
```

### Data flow

1. Agent spec (built-in demo or JSON file) -> `AgentSpec` dataclass
2. Six rule functions scan the spec for risk patterns using keyword matching against capability and touchpoint names
3. Each rule emits `Finding` objects with category, severity, and recommendations
4. `build_checklist()` derives 7 pass/fail items from the findings
5. `calculate_risk_score()` sums weighted severity scores (CRITICAL=25, HIGH=15, MEDIUM=8, LOW=3), capped at 100
6. Output as formatted text or JSON

### Dependencies

- Python 3.8+ standard library only (`json`, `sys`, `textwrap`, `dataclasses`, `enum`)
- No external packages, no API keys, no network calls

## Limitations

- **Keyword-based**: Risk detection relies on keyword matching against capability/touchpoint names. A capability named "get stuff" won't trigger ordering rules even if it places orders. Real-world use should pair this with LLM-based analysis for natural language understanding.
- **Static analysis only**: Does not inspect actual agent code, runtime behavior, or deployed configurations. It audits the *design* spec, not the implementation.
- **No context-awareness**: Cannot check whether ordered items are compatible with available equipment (e.g., eggs + no stove). That requires domain-specific knowledge graphs.
- **English-only keywords**: Rule patterns are English keywords. Agent specs in other languages won't match.
- **No severity customization**: Severity weights are hardcoded. Different industries may need different risk calibrations.

## Why it matters for Claude-driven products

- **Agent factories**: Anyone building autonomous agent pipelines (agent-as-a-service, multi-agent orchestration) needs systematic pre-deployment safety checks. This tool provides a template for that audit step.
- **Lead-gen / marketing agents**: Agents that send outbound emails, place ad buys, or contact prospects share the same consent-boundary and urgency-escalation risks as the AI cafe. The checklist applies directly.
- **Voice AI**: Voice agents that place phone calls to external parties face identical consent and escalation risks -- amplified because voice is harder to ignore than email.
- **Compliance**: As AI agent regulations emerge, having a documented audit trail (checklist, findings, risk score) will become a baseline requirement. Building audit-first is cheaper than retrofitting.
