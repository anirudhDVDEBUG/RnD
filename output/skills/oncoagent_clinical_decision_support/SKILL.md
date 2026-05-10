---
name: oncoagent_clinical_decision_support
description: |
  Build a privacy-preserving, dual-tier multi-agent oncology clinical decision support system inspired by the OncoAgent architecture. Uses LangGraph orchestration, Corrective RAG with medical embeddings, reflexion-based safety validation, and on-premises LLM deployment.
  Triggers: multi-agent clinical AI, oncology decision support, privacy-preserving medical AI, corrective RAG pipeline, dual-tier LLM routing
---

# OncoAgent: Dual-Tier Multi-Agent Clinical Decision Support

Build a privacy-preserving, multi-agent oncology clinical decision support system using the OncoAgent architecture: dual-tier LLM routing, Corrective RAG, reflexion safety validation, and on-premises deployment.

## When to use

- "Build a multi-agent clinical decision support system for oncology"
- "Create a privacy-preserving medical AI pipeline with RAG and safety layers"
- "Set up a dual-tier LLM routing system that triages by case complexity"
- "Implement a Corrective RAG pipeline with anti-hallucination safeguards for medical guidelines"
- "Design an on-premises healthcare AI system with HIPAA-compliant data handling"

## How to use

### Step 1: Define the Agent Graph (LangGraph)

Create an 8-node stateful graph with LangGraph:

```
Router → Ingestion → Corrective RAG → Specialist ↔ Critic → HITL Gate → Formatter → END
                                                       ↓
                                                    Fallback → END
```

Use an immutable `AgentState` TypedDict (~30 typed keys) for a complete audit trail. Wire 5 conditional edges routing based on complexity and confidence scores.

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional, List

class AgentState(TypedDict):
    patient_id: str
    query: str
    redacted_query: str
    complexity_score: float
    selected_tier: int
    rag_documents: List[dict]
    rag_confidence: float
    specialist_output: str
    critic_feedback: str
    critic_pass: bool
    retry_count: int
    final_output: str
    # ... additional audit fields

graph = StateGraph(AgentState)
graph.add_node("router", complexity_router)
graph.add_node("ingestion", ingest_and_redact)
graph.add_node("corrective_rag", corrective_rag_pipeline)
graph.add_node("specialist", specialist_node)
graph.add_node("critic", reflexion_critic)
graph.add_node("hitl_gate", human_in_the_loop)
graph.add_node("formatter", format_output)
graph.add_node("fallback", safe_refusal)
```

### Step 2: Implement Dual-Tier Model Routing

Route cases to Tier 1 (fast, smaller model) or Tier 2 (deep reasoning, larger model) based on a weighted complexity score:

```python
def compute_complexity(case: dict) -> float:
    score = 0.0
    # Cancer type weighting
    if case.get("cancer_type") in RARE_CANCERS:
        score += 0.40
    elif case.get("cancer_type") == "unknown_primary":
        score += 0.30
    # Stage weighting
    if case.get("stage") == "IV":
        score += 0.25
    elif case.get("stage") == "III":
        score += 0.15
    # Mutation weighting
    n_mutations = len(case.get("mutations", []))
    if n_mutations >= 2:
        score += 0.30
    elif n_mutations == 1:
        score += 0.15
    # Prior treatment
    if case.get("prior_treatment"):
        score += 0.10
    return score

def complexity_router(state: AgentState) -> AgentState:
    score = compute_complexity(state)
    tier = 2 if score >= 0.5 else 1
    return {**state, "complexity_score": score, "selected_tier": tier}
```

| Parameter | Tier 1 | Tier 2 |
|-----------|--------|--------|
| Purpose | Speed-optimized triage | Deep reasoning for complex cases |
| Routing Trigger | Complexity < 0.5 | Complexity >= 0.5 |
| Context Window | 32K tokens | 128K tokens |

### Step 3: Build the Corrective RAG Pipeline

Implement a four-stage retrieval pipeline with anti-hallucination guarantees:

```python
def corrective_rag_pipeline(state: AgentState) -> AgentState:
    query = state["redacted_query"]

    # Stage 1: Recall — wide-net retrieval with PubMedBERT bi-encoder
    candidates = vector_store.similarity_search(query, k=15)

    # Stage 2: Distance Gate — anti-hallucination floor
    DISTANCE_THRESHOLD = 0.10
    filtered = [doc for doc in candidates if doc.distance <= DISTANCE_THRESHOLD]
    if not filtered:
        return {**state, "rag_confidence": 0.0,
                "final_output": "Insufficient evidence in provided guidelines."}

    # Stage 3: Re-Ranking — cross-encoder joint relevance scoring
    reranked = cross_encoder.rerank(query, filtered, top_k=5)

    # Stage 4: Context Trimming — fit within context budget
    MAX_CONTEXT_CHARS = 6000
    trimmed = trim_to_budget(reranked, MAX_CONTEXT_CHARS)

    confidence = compute_rag_confidence(trimmed)
    return {**state, "rag_documents": trimmed, "rag_confidence": confidence}
```

**Key components:**
- **Embeddings:** `pritamdeka/S-PubMedBert-MS-MARCO` (PubMed/MS-MARCO fine-tuned)
- **Vector store:** ChromaDB (local, zero-PHI compliant)
- **Re-ranker:** MS-MARCO MiniLM cross-encoder
- **Knowledge base:** 70+ NCCN/ESMO physician-grade oncology guidelines

### Step 4: Implement the 4-Layer Safety Framework

**Layer 1 — Zero-PHI Redaction (Ingestion Node):**
```python
def ingest_and_redact(state: AgentState) -> AgentState:
    redacted = redact_phi(state["query"])  # Names, DOB, MRN, addresses
    return {**state, "redacted_query": redacted}
```

**Layer 2 — Confidence Gate:**
Automatically block outputs when `rag_confidence < 0.3`.

**Layer 3 — Reflexion Critic (Deterministic Code, Not LLM):**
```python
def reflexion_critic(state: AgentState) -> AgentState:
    output = state["specialist_output"]
    # 1. Formatting check — validate OncoCoT schema compliance
    fmt_ok = validate_format(output)
    # 2. Safety check — rule-based scan for prohibited patterns
    safety_ok = check_no_absolute_dosing_without_citation(output)
    safety_ok &= check_drug_interactions(output)
    # 3. Entailment check — verify recommendations supported by RAG context
    entailment_ok = verify_entailment(output, state["rag_documents"])

    passed = fmt_ok and safety_ok and entailment_ok
    if not passed and state["retry_count"] < 2:
        feedback = build_feedback(fmt_ok, safety_ok, entailment_ok)
        return {**state, "critic_pass": False, "critic_feedback": feedback,
                "retry_count": state["retry_count"] + 1}
    return {**state, "critic_pass": passed}
```

**Layer 4 — Human-in-the-Loop Gate:**
Mandatory clinician interrupt for all Tier 2 cases and any output with low confidence.

### Step 5: Fine-Tune with QLoRA on AMD MI300X (Optional)

Use QLoRA with Unsloth for efficient on-premises fine-tuning:

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="Qwen/Qwen3.5-9B",
    load_in_4bit=True,
    dtype=None,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank (32 for Tier 2)
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    use_gradient_checkpointing="unsloth",
)
```

**Training corpus (OncoCoT): 266,854 samples** from PMC-Patients, Asclepius, and synthetic generation. Sequence packing at 2048 tokens achieves ~50 minute full training on MI300X.

### Step 6: Build the Clinical Interface

Deploy with Gradio using real-time streaming from LangGraph:

```python
import gradio as gr

def stream_consultation(query: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = {"query": query, "retry_count": 0}
    for event in compiled_graph.stream(state, config, stream_mode="updates"):
        node_name = list(event.keys())[0]
        label = NODE_LABELS.get(node_name, node_name)
        yield f"**{label}**\n{event[node_name].get('specialist_output', '...')}"

NODE_LABELS = {
    "corrective_rag": "Retrieving NCCN/ESMO guidelines",
    "specialist": "Analyzing clinical case",
    "critic": "Validating recommendation",
}
```

Each session gets a unique `PT-XXXX` thread ID for per-patient memory isolation.

### Architecture Summary

```
┌─────────────────────────────────────────────────────┐
│                    OncoAgent                         │
│                                                     │
│  ┌──────────┐   ┌───────────┐   ┌────────────────┐  │
│  │ Zero-PHI │──▶│ Complexity│──▶│ Corrective RAG │  │
│  │ Redaction│   │  Router   │   │ (4-stage)      │  │
│  └──────────┘   └───────────┘   └───────┬────────┘  │
│                                         │           │
│                  ┌──────────────────────┐│           │
│                  │  Tier 1 (9B) or     ││           │
│                  │  Tier 2 (27B)       │◀┘           │
│                  │  Specialist          │            │
│                  └──────────┬───────────┘            │
│                             │                        │
│                  ┌──────────▼───────────┐            │
│                  │  Reflexion Critic    │            │
│                  │  (deterministic)     │            │
│                  └──────────┬───────────┘            │
│                             │                        │
│                  ┌──────────▼───────────┐            │
│                  │  HITL Gate           │            │
│                  │  (clinician review)  │            │
│                  └─────────────────────┘            │
└─────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **100% on-premises** — no cloud API dependency
2. **Zero-PHI guarantee** — redaction before any LLM processing
3. **Anti-hallucination** — cosine distance gate (0.10 threshold) blocks out-of-domain queries
4. **Deterministic safety** — critic uses rule-based code, not LLM, preventing adversarial bypass
5. **Auditability** — immutable state with complete decision trail
6. **HIPAA/GDPR by design** — local vector store, per-patient memory isolation

## References

- [OncoAgent Official Paper (Hugging Face Blog)](https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/oncoagent-official-paper)
- Architecture: LangGraph multi-agent orchestration with 8 nodes, 5 conditional edges
- Models: Qwen 3.5 (9B) + Qwen 3.6 (27B) with QLoRA fine-tuning
- Training: 266,854 OncoCoT samples, ~50 min on AMD Instinct MI300X
- Knowledge: 70+ NCCN/ESMO oncology guidelines, ChromaDB vector store
- Embeddings: PubMedBERT (S-PubMedBert-MS-MARCO)
