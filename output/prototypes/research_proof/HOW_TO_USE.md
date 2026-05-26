# How to Use Research Proof

## This is a Claude Code Skill

Research Proof is a **Claude Code skill** — a structured prompt that teaches Claude a repeatable methodology. It does not require `pip install` or `npm install`.

## Install the Skill

1. Clone the source repo (or copy the SKILL.md file):

```bash
git clone https://github.com/tonyblu331/research-proof.git
```

2. Copy the skill into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/research-proof
cp research-proof/SKILL.md ~/.claude/skills/research-proof/SKILL.md
```

3. Restart Claude Code (or open a new session). The skill is now active.

## Trigger Phrases

Say any of these to Claude Code and it will activate the Research Proof pipeline:

- `"verify this claim"`
- `"pressure test"`
- `"falsify"`
- `"proof ledger"`
- `"research proof"`
- `"evidence plan"`

## First 60 Seconds

**Input** (paste into Claude Code):

```
Pressure test this claim: "RAG eliminates hallucinations in production LLM systems"
```

**Output** (Claude produces all six sections):

```
## 1. Claim List
  1. RAG eliminates hallucinations in production LLM systems

## 2. Falsifiable Evidence Plans
  - Confirming: Production system with 0% hallucination rate over 10k queries
  - Falsifying: Any documented hallucination in a RAG-equipped production system

## 3. Adversarial Report
  Confidence: LOW — "eliminates" is absolute; no system achieves zero hallucinations.
  Fallacies: Absolute claim is unfalsifiable in practice
  Biases: Cherry-picked examples in RAG demos

## 4. Frozen Verifiers
  - Hallucination rate = 0% across 10k diverse queries
  - Locked before evidence review: Yes

## 5. Proof Ledger
| # | Claim | Falsifiable? | Verifier Status | Verdict |
|---|-------|-------------|-----------------|---------|
| 1 | RAG eliminates hallucinations... | Yes | FAIL | REFUTED |

## 6. Summary Verdict
  Claims tested: 1 | Supported: 0 | Refuted: 1 | Overall confidence: LOW
  Recommendation: Reframe claim as "RAG significantly reduces hallucinations"
```

## Running the Standalone Demo

To see the pipeline in action without Claude Code:

```bash
bash run.sh
```

This runs `research_proof.py` with four mock AI research claims and prints the full report to stdout. It also writes `proof_ledger.json` with structured output.

## Using the Python Module Directly

```python
from research_proof import extract_claims, evaluate_claim, render_full_report

claims = extract_claims("LLMs write bug-free code\nFine-tuning always beats prompting")
results = [evaluate_claim(i+1, c) for i, c in enumerate(claims)]
print(render_full_report(results))
```
