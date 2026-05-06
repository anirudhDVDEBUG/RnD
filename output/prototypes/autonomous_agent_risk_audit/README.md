# Autonomous Agent Risk Audit

**Audit autonomous AI agents for real-world harm before they order 6,000 napkins.**

A zero-dependency Python tool that analyzes an autonomous agent's design spec and produces a risk report covering consent violations, resource waste, uncontrolled external communications, irreversible actions, and missing guardrails. Inspired by the [AI cafe in Stockholm](https://simonwillison.net/2026/May/5/our-ai-started-a-cafe-in-stockholm/#atom-everything) that ordered 120 eggs with no stove and applied for government permits with AI-generated sketches.

## Headline result

```
Agent: AI Cafe Manager (Stockholm)    Risk: 100/100   Findings: 14   Grade: F - DO NOT DEPLOY
Agent: Inventory Assistant (guarded)  Risk:   0/100   Findings:  0   Grade: A - Low risk
```

Same business domain. Night-and-day safety difference based on guardrail design.

## Quick links

- [HOW_TO_USE.md](HOW_TO_USE.md) -- Install, run, integrate as a Claude skill
- [TECH_DETAILS.md](TECH_DETAILS.md) -- Architecture, rule engine, limitations
