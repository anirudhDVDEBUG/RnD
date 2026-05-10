# Technical Details

## What It Does

OncoAgent is a multi-agent clinical decision support pipeline for oncology that processes natural-language case descriptions and returns guideline-grounded treatment recommendations. It implements a dual-tier routing system (fast triage vs. deep reasoning), a 4-stage Corrective RAG pipeline with anti-hallucination guarantees, and a deterministic reflexion critic that validates every output before it reaches a clinician.

The key insight is the separation of concerns: PHI never leaves the local system, complexity scoring determines compute allocation, and the critic is rule-based (not LLM-based) to avoid compounding hallucination risk. The architecture is designed for on-premises deployment where patient data cannot leave the hospital network.

## Architecture

```
Query → [Router] → [Ingestion/Redaction] → [Corrective RAG] → [Specialist] ↔ [Critic] → [HITL] → [Formatter] → Output
                                                                     ↓ (fail)
                                                                  [Fallback] → Safe Refusal
```

### Key Files

| File | Purpose |
|------|---------|
| `oncoagent/state.py` | `AgentState` dataclass — immutable audit trail with ~15 typed fields |
| `oncoagent/router.py` | Weighted complexity scoring (cancer type, stage, mutations, prior tx) |
| `oncoagent/redaction.py` | Regex-based PHI stripping (names, SSN, DOB, MRN, phone, email) |
| `oncoagent/rag.py` | 4-stage Corrective RAG: Recall → Distance Gate → Re-Rank → Trim |
| `oncoagent/specialist.py` | Template-based recommendation generator (mock for on-prem LLM) |
| `oncoagent/critic.py` | 4-check deterministic validator: format, safety patterns, citations, confidence |
| `oncoagent/guidelines.py` | 8 mock NCCN/ESMO guidelines with keyword search (mock for ChromaDB) |
| `oncoagent/graph.py` | Pipeline orchestrator — sequential node execution with retry loop |
| `main.py` | CLI entry point with 4 demo cases |

### Data Flow

1. **Input:** Free-text clinical query with potential PHI
2. **Redaction:** Regex patterns strip names, dates, MRN, SSN, phone, email
3. **Routing:** Weighted score from cancer type (0.30–0.40), stage (0.15–0.25), mutations (0.15–0.30), prior treatment (0.10) → Tier 1 if < 0.5, Tier 2 if >= 0.5
4. **RAG:** Keyword overlap search → distance gate → relevance re-ranking → context budget trimming (6000 chars)
5. **Specialist:** Structured OncoCoT output with guideline citations
6. **Critic:** Deterministic checks — no LLM involved. Checks format sections, prohibited language patterns, guideline ID presence, confidence floor (0.3)
7. **Retry:** Up to 2 retries if critic fails; then fallback safe refusal
8. **Output:** Formatted recommendation with audit trail

### Dependencies

**Demo (this repo):** Zero — pure Python 3.8+ standard library only.

**Production stack (from the paper):**
- `langgraph` — state machine orchestration
- `chromadb` — local vector store (HIPAA-compliant, no cloud)
- `sentence-transformers` — PubMedBERT embeddings (`pritamdeka/S-PubMedBert-MS-MARCO`)
- `cross-encoder` — MS-MARCO MiniLM re-ranker
- `presidio-analyzer` — Microsoft's PHI detection (NER-based, more robust than regex)
- On-premises LLM (e.g., Llama 3, Mixtral) via vLLM or Ollama

### Model Calls

This demo makes **zero LLM calls**. The specialist node uses template-based generation from retrieved guidelines. In production:
- **Tier 1:** Smaller model (7B–13B), 32K context, for standard cases
- **Tier 2:** Larger model (70B+), 128K context, for complex/rare cases
- Both tiers run on-premises — no data leaves the hospital network

## Limitations

- **Mock RAG:** Uses keyword overlap instead of real vector similarity search. Production needs PubMedBERT embeddings + ChromaDB.
- **Mock specialist:** Template-based output instead of LLM generation. The structured format is representative but lacks the reasoning depth of a real LLM.
- **Regex PHI redaction:** The regex approach catches common patterns but misses edge cases (misspelled names, unusual date formats). Production should use Presidio or a dedicated NER model.
- **8 guidelines only:** Real deployment needs 70+ NCCN/ESMO guidelines fully ingested and embedded.
- **No real HITL:** The human-in-the-loop gate auto-approves in demo mode. Production must integrate with clinical workflow systems (Epic, Cerner).
- **No persistence:** State is in-memory only. Production needs audit log persistence for regulatory compliance.

## Why It Matters for Claude-Driven Products

**Agent factory pattern:** The 8-node graph with conditional routing, retry loops, and deterministic validation is directly transferable to any domain where AI agents need safety guarantees — legal document review, financial compliance, insurance claims.

**Dual-tier routing for cost control:** The complexity-based model selection pattern applies to any multi-model deployment. Route simple queries to Claude Haiku, complex ones to Claude Opus — same principle, different domain.

**Corrective RAG as a reusable pattern:** The 4-stage retrieval pipeline (recall → gate → re-rank → trim) with confidence scoring is a production-ready RAG pattern applicable to lead-gen knowledge bases, marketing content systems, or support automation.

**Deterministic critic over LLM critic:** Using rule-based validation instead of a second LLM for safety checks avoids compounding hallucination risk. This pattern is valuable for any regulated domain where you need auditable, deterministic safety guarantees.

**Privacy-first architecture:** The zero-PHI, on-premises-only design is a template for any healthcare, legal, or financial AI system where data sovereignty is non-negotiable.
