---
name: AI Maintenance Cost Auditor
description: |
  Audits AI-generated code for maintenance cost impact. Applies James Shore's inverse-rate principle:
  if AI doubles code output, maintenance costs must halve — otherwise you're accumulating debt faster.
  TRIGGER: when reviewing AI-generated code, assessing technical debt from AI output, evaluating
  code quality of agent-written code, or planning AI-assisted development workflows.
---

# AI Maintenance Cost Auditor

Audit AI-generated or AI-assisted code changes to ensure they reduce — not increase — long-term maintenance costs.

## When to use

- "Review this AI-generated code for maintainability"
- "Audit the technical debt impact of these changes"
- "Is this AI-written code going to cost us later?"
- "Assess maintenance cost of this PR / diff"
- "Check if our AI coding output is sustainable"

## Core Principle

> Your AI coding agent needs to reduce your maintenance costs. Not by a little bit, either.
> You write code twice as quick now? Better hope you've halved your maintenance costs.
> Three times as productive? One third the maintenance costs. Otherwise, you're screwed.
> You're trading a temporary speed boost for permanent indenture.
>
> The math only works if the LLM *decreases* your maintenance costs, and by exactly the
> inverse of the rate it adds code.
>
> — James Shore, *You Need AI That Reduces Maintenance Costs*

## How to use

### Step 1: Identify the AI-generated scope

Determine which files/functions were written or substantially modified by AI. Look at recent diffs, PR descriptions, or ask the developer.

### Step 2: Run the maintenance cost checklist

For each AI-generated change, evaluate these maintenance multipliers:

| Factor | Low Cost (good) | High Cost (red flag) |
|---|---|---|
| **Readability** | Clear intent, self-documenting | Verbose, obscure variable names, over-abstracted |
| **Duplication** | DRY, reuses existing patterns | Copy-pasted logic, near-duplicate functions |
| **Test coverage** | Tests generated alongside code | No tests, or tests that just assert current behavior |
| **Coupling** | Loose coupling, clear interfaces | Tightly coupled to implementation details |
| **Complexity** | Simple, minimal branching | Unnecessary abstractions, deep nesting, premature generalization |
| **Consistency** | Matches project conventions | Introduces new patterns/styles inconsistent with codebase |
| **Dead code** | Only what's needed | Unused imports, commented-out blocks, unreachable branches |
| **Error handling** | Appropriate, follows project patterns | Over-defensive, swallows errors, or missing entirely |

### Step 3: Calculate the maintenance ratio

Estimate:
- **Speed multiplier**: How much faster was this code produced vs. manual? (e.g., 2x, 3x)
- **Maintenance multiplier**: Will maintaining this code cost more (>1x), the same (1x), or less (<1x) than hand-written equivalent?

**The product must be <= 1.** If speed is 3x and maintenance cost is 0.5x, the product is 1.5x — still unsustainable. Target: speed x maintenance <= 1.0.

### Step 4: Produce actionable recommendations

For each red flag found:
1. Identify the specific file and location
2. Explain the maintenance cost impact
3. Suggest a concrete fix (refactor, delete, consolidate, add tests)
4. Estimate effort to fix now vs. cost of deferring

### Step 5: Summarize the verdict

Provide a summary rating:
- **Sustainable**: maintenance ratio <= 1.0, few red flags
- **Risky**: maintenance ratio 1.0-2.0, several red flags that should be addressed before merge
- **Unsustainable**: maintenance ratio > 2.0, significant rework needed — the speed gain is illusory

## References

- [James Shore — You Need AI That Reduces Maintenance Costs](https://www.jamesshore.com/v2/blog/2026/you-need-ai-that-reduces-your-maintenance-costs)
- [Simon Willison — Quoting James Shore](https://simonwillison.net/2026/May/11/james-shore/#atom-everything)
