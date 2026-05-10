# How to Use OncoAgent

## Install

```bash
git clone <this-repo>
cd oncoagent_clinical_decision_support
# No pip install needed — zero external dependencies for the demo
```

Python 3.8+ required (uses dataclasses + typing). No API keys needed.

For production use with real LLMs and vector stores, install the full stack:
```bash
pip install langgraph chromadb sentence-transformers presidio-analyzer
```

## Run

```bash
bash run.sh
```

Or directly:
```bash
python3 main.py
```

Single query mode:
```bash
python3 main.py "Stage IV NSCLC with EGFR exon 19 deletion, first-line therapy"
```

## Claude Skill Setup

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/oncoagent_clinical_decision_support
cp SKILL.md ~/.claude/skills/oncoagent_clinical_decision_support/SKILL.md
```

**Trigger phrases that activate it:**
- "Build a multi-agent clinical decision support system for oncology"
- "Create a privacy-preserving medical AI pipeline with RAG"
- "Set up a dual-tier LLM routing system that triages by case complexity"
- "Implement a Corrective RAG pipeline with anti-hallucination safeguards"
- "Design an on-premises healthcare AI system with HIPAA-compliant data handling"

## First 60 Seconds

**Input:**
```
Patient John Smith (MRN: 12345) diagnosed with stage IV NSCLC,
EGFR exon 19 deletion. No prior treatment. DOB: 03/15/1958.
Requesting first-line therapy recommendation.
```

**What happens:**
1. PHI redacted: `John Smith` → `[REDACTED_NAME]`, `MRN: 12345` → `[REDACTED_MRN]`, DOB stripped
2. Complexity router: score 0.40 → Tier 1 (standard case)
3. Corrective RAG: retrieves NCCN NSCLC EGFR guideline, confidence 0.75
4. Specialist: generates structured recommendation citing osimertinib 80mg daily
5. Critic: validates format, citations, safety — PASS
6. HITL gate: auto-approved (demo mode)

**Output (excerpt):**
```
## Clinical Recommendation (Tier 1)

**Primary Guideline:** NCCN NSCLC Guidelines v4.2024 — First-Line Therapy
**Guideline ID:** NCCN-NSCLC-2024-01

### Recommendation
For metastatic NSCLC with EGFR exon 19 deletion or L858R mutation,
first-line osimertinib (80 mg daily) is the preferred regimen (Category 1).
Median PFS: 18.9 months vs 10.2 months for comparator TKIs.

### Clinical Notes
- Complexity Score: 0.40
- RAG Confidence: 0.750
- Model Tier: 1
- Documents Retrieved: 3
```

## Integration Patterns

**As a Python library:**
```python
from oncoagent.graph import run_pipeline

state = run_pipeline("Stage IV NSCLC EGFR exon 19 deletion, first-line")
print(state.final_output)
print(f"Confidence: {state.rag_confidence}")
print(f"Tier: {state.selected_tier}")
```

**Key state fields you can inspect:**
- `state.redacted_query` — PHI-stripped input
- `state.complexity_score` — routing score (0.0–1.0)
- `state.selected_tier` — 1 (fast) or 2 (deep)
- `state.rag_documents` — retrieved guideline chunks
- `state.rag_confidence` — retrieval confidence
- `state.critic_pass` — whether safety validation passed
- `state.audit_log` — full execution trace
