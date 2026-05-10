---
name: premortem_risk_analysis
description: |
  Premortem risk analysis skill — finds the concrete ways a plan could fail before you commit.
  Multi-agent silent scan, mitigation triplets, history snapshots, and reverse-premortem.
  Based on Gary Klein (2007) prospective hindsight and Kahneman's outside view.

  Triggers:
  - User says "premortem", "pre-mortem", or "what could go wrong"
  - User asks to analyze risks, failure modes, or blind spots in a plan
  - User wants to stress-test a decision or architecture before committing
  - User asks "how could this fail" or "find the risks"
---

# Premortem Risk Analysis

Find the concrete ways a plan could fail **before** you commit. Uses Gary Klein's premortem technique (2007) combined with Kahneman's outside view to surface risks, blind spots, and failure modes.

## When to use

- "Run a premortem on this plan"
- "What could go wrong with this approach?"
- "Find the failure modes before we commit"
- "Stress-test this architecture / decision"
- "What are the blind spots in this design?"

## How to use

### Step 1 — Frame the plan

Clearly state the plan, decision, or architecture under review. Gather context from the codebase, docs, or conversation.

### Step 2 — Prospective hindsight ("Imagine it failed")

Imagine it is 6 months from now and the plan has **failed spectacularly**. Working backwards from that imagined failure, independently generate failure scenarios across these dimensions:

| Dimension | Example failure |
|---|---|
| **Technical** | Race condition under load, schema migration breaks rollback |
| **Integration** | Third-party API changes contract, auth token expiry unhandled |
| **Operational** | No runbook for failover, monitoring gaps miss cascading failure |
| **Human / Process** | Key-person dependency, unclear ownership during incident |
| **External / Market** | Regulatory change, competitor move invalidates assumption |

### Step 3 — Multi-agent silent scan

For each dimension, act as a separate critical reviewer (Devil's Advocate, Pessimist, Security Auditor, Ops Engineer, End User). Each reviewer independently surfaces risks the others might miss.

### Step 4 — Mitigation triplets

For every identified risk, produce a **mitigation triplet**:

```
Risk:        [Concrete failure scenario]
Likelihood:  [High / Medium / Low]
Mitigation:  [Specific, actionable countermeasure]
```

Rank by `likelihood x impact` and present the top risks first.

### Step 5 — Reverse-premortem ("Imagine it succeeded wildly")

Now imagine the plan succeeded beyond expectations. Ask:
- What **lucky breaks** did we depend on?
- Which assumptions **must** hold for success?
- What would we wish we had built differently at 10x scale?

### Step 6 — History snapshot

Summarize the analysis in a structured output:

```markdown
## Premortem Summary — [Plan Name] — [Date]

### Top Risks (ranked)
1. **[Risk title]** — Likelihood: X, Impact: Y
   - Mitigation: ...
2. ...

### Assumptions That Must Hold
- ...

### Reverse-Premortem Insights
- ...

### Recommended Actions Before Committing
- [ ] ...
```

Offer to save this snapshot to a file (e.g., `docs/premortem-YYYY-MM-DD.md`) for future reference.

## References

- **Source**: [AndyShaman/premortem](https://github.com/AndyShaman/premortem) — Claude Code skill for premortem risk analysis
- **Theory**: Klein, G. (2007). "Performing a Project Premortem." *Harvard Business Review.*
- **Theory**: Kahneman, D. — Outside view / reference class forecasting
