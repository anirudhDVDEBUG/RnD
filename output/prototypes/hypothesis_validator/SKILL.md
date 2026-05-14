---
name: hypothesis_validator
description: |
  Validate startup hypotheses with evidence, ICP clarity, money signals, and GTM reality checks.
  No-fluff framework for solopreneurs and founders to stress-test ideas before building.
  Covers customer discovery, jobs-to-be-done, willingness to pay, and go-to-market feasibility.

  Triggers:
  - User wants to validate a startup idea or business hypothesis
  - User asks about product-market fit, ICP, or customer discovery
  - User wants to assess willingness to pay or money signals
  - User asks for a go-to-market reality check
  - User says "validate my hypothesis" or "is this idea worth building"
---

# Hypothesis Validator

Validate startup hypotheses with structured evidence gathering, ICP clarity, money signals, and go-to-market reality checks. Built for solopreneurs and founders who want a no-fluff assessment before committing time and resources.

## When to use

- "Validate my startup hypothesis"
- "Is this idea worth building? Here's my thesis..."
- "Who is my ideal customer and will they pay?"
- "Run a go-to-market reality check on this product"
- "Help me find product-market fit signals for my idea"

## How to use

### Step 1 -- Capture the hypothesis

Ask the user to state their hypothesis clearly using this format:

```
Hypothesis: [Target customer] has [problem/need] and will [desired action/pay $X] for [proposed solution] because [key assumption].
```

If the user provides a loose idea, help them refine it into this structured format before proceeding.

### Step 2 -- ICP (Ideal Customer Profile) clarity check

Evaluate the specificity and reachability of the target customer:

| Dimension | Question |
|---|---|
| **Who exactly?** | Can you name 5 real people or companies that fit this profile? |
| **Where do they gather?** | What communities, platforms, or channels can you reach them on today? |
| **How big is the segment?** | Is this a niche you can dominate or a vague mass market? |
| **Urgency** | Is this a painkiller (must-have) or vitamin (nice-to-have) for them? |

Rate ICP clarity: **Sharp** (specific, reachable, urgent) / **Fuzzy** (vague, broad, unclear urgency) / **Missing** (no defined customer yet).

### Step 3 -- Evidence & signal scan

Search for existing evidence that supports or contradicts the hypothesis:

- **Demand signals**: Are people actively searching for solutions? (Google Trends, Reddit threads, forum complaints, review pain points)
- **Existing alternatives**: What do customers use today? Why is it insufficient?
- **Failed predecessors**: Has someone tried this before? Why did they fail?
- **Market timing**: Why now? What changed that makes this viable today?

Use web search to gather real data points. Summarize findings as **Supporting**, **Neutral**, or **Contradicting** evidence.

### Step 4 -- Money signals & willingness to pay

Assess whether real money signals exist:

| Signal | Evidence |
|---|---|
| **Already paying** | Are customers paying for inferior alternatives? How much? |
| **Budget exists** | Is there an allocated budget line for this type of solution? |
| **Price anchors** | What comparable products cost in this space? |
| **JTBD value** | What job-to-be-done does this fulfill? What is that job worth? |
| **Switching cost** | How painful is it to switch from current solution? |

Rate money signals: **Strong** (clear willingness to pay) / **Weak** (interest but no spend evidence) / **None** (no money signals found).

### Step 5 -- GTM (Go-to-Market) reality check

Evaluate whether the founder can realistically reach customers:

- **Channel access**: Can you reach your ICP without paid ads? What organic channels exist?
- **First 10 customers**: How specifically would you get your first 10 paying customers?
- **Sales cycle**: Is this self-serve, sales-assisted, or enterprise sales? Does that match your resources?
- **Unfair advantage**: Do you have domain expertise, existing audience, or unique distribution?
- **Solo-feasibility**: Can one person build, launch, and sell this? What's the minimum viable team?

Rate GTM feasibility: **Clear path** / **Needs experimentation** / **No obvious path**.

### Step 6 -- Verdict & next actions

Produce a structured validation report:

```markdown
## Hypothesis Validation Report -- [Date]

### Hypothesis
[Restated hypothesis]

### Scorecard
| Dimension | Rating | Key Finding |
|---|---|---|
| ICP Clarity | Sharp/Fuzzy/Missing | ... |
| Evidence | Supporting/Neutral/Contradicting | ... |
| Money Signals | Strong/Weak/None | ... |
| GTM Feasibility | Clear/Experiment/No path | ... |

### Overall Verdict
GREEN **Validate further** -- Strong signals, worth running experiments
YELLOW **Pivot needed** -- Some signals but key assumptions are weak
RED **Kill or rethink** -- No evidence of demand, willingness to pay, or reachable customers

### Recommended Next Steps
1. [ ] ...
2. [ ] ...
3. [ ] ...

### Key Risks
- ...
```

Offer to save the report to a file (e.g., `docs/hypothesis-validation-YYYY-MM-DD.md`).

## References

- **Source**: [evgeniy038/hypothesis-validator](https://github.com/evgeniy038/hypothesis-validator) -- AI agent skill for validating startup hypotheses
- **Framework**: Jobs-to-be-Done (JTBD) -- Clayton Christensen
- **Framework**: Customer Discovery -- Steve Blank, *The Four Steps to the Epiphany*
- **Framework**: Mom Test -- Rob Fitzpatrick
