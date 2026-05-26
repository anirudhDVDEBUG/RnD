---
name: Research Proof
description: |
  Pressure-test research claims with falsifiable evidence plans, adversarial checks, frozen verifiers, and proof ledgers.
  Triggers: "verify this claim", "pressure test", "falsify", "proof ledger", "research proof", "evidence plan"
---

# Research Proof

Pressure-test research claims by generating falsifiable evidence plans, running adversarial checks, freezing verifier criteria, and maintaining a proof ledger.

## When to use

- "Pressure-test this research claim for me"
- "Create a falsifiable evidence plan for this hypothesis"
- "Run adversarial checks on these findings"
- "Build a proof ledger for this study"
- "Verify this claim with frozen verifiers"

## How to use

### Step 1: Claim Extraction
Identify the core claim(s) from the research input. Break compound claims into atomic, testable propositions.

### Step 2: Falsifiable Evidence Plan
For each claim, generate a falsifiable evidence plan:
- State the claim precisely
- Define what evidence would **confirm** the claim
- Define what evidence would **falsify** the claim (critical)
- Identify assumptions that must hold
- List required data sources or experiments

### Step 3: Adversarial Checks
Apply adversarial reasoning to each claim:
- Identify logical fallacies or reasoning gaps
- Check for confounding variables
- Look for survivorship bias, cherry-picked data, or p-hacking indicators
- Propose steel-man counter-arguments
- Rate confidence: HIGH / MEDIUM / LOW with justification

### Step 4: Frozen Verifiers
Define immutable verification criteria **before** examining evidence:
- Lock acceptance/rejection thresholds upfront
- Specify statistical or logical criteria that cannot be moved post-hoc
- Document these as the "frozen verifier" contract

### Step 5: Proof Ledger
Maintain a structured proof ledger as a markdown table:

| # | Claim | Falsifiable? | Evidence Plan | Adversarial Finding | Verifier Status | Verdict |
|---|-------|-------------|---------------|--------------------|-----------------|---------|
| 1 | ...   | Yes/No      | ...           | ...                | PASS/FAIL/PENDING | SUPPORTED/REFUTED/INCONCLUSIVE |

### Step 6: Summary Verdict
Provide an overall assessment:
- Number of claims tested
- Pass/fail ratio
- Key vulnerabilities identified
- Confidence level in the research as a whole
- Recommended next steps (additional data needed, replication suggestions)

## Output Format

Always output:
1. **Claim List** — numbered atomic claims
2. **Evidence Plans** — per-claim falsification criteria
3. **Adversarial Report** — vulnerabilities found
4. **Frozen Verifiers** — locked criteria
5. **Proof Ledger** — summary table
6. **Verdict** — overall assessment with confidence rating

## References

- Source: [tonyblu331/research-proof](https://github.com/tonyblu331/research-proof)
- Methodology: Based on scientific method principles — falsifiability (Popper), pre-registration of criteria, and adversarial review
