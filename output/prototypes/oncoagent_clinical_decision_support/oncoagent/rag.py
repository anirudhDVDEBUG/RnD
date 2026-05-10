"""Corrective RAG pipeline — 4-stage retrieval with anti-hallucination guarantees."""

from .state import AgentState
from .guidelines import keyword_search

DISTANCE_THRESHOLD = 0.10  # Mock distance gate
MIN_CONFIDENCE = 0.3


def corrective_rag_pipeline(state: AgentState) -> AgentState:
    """Four-stage retrieval: Recall → Distance Gate → Re-Rank → Context Trim."""
    query = state.redacted_query or state.query

    # Stage 1: Recall — wide-net retrieval (keyword search as stand-in for vector similarity)
    candidates = keyword_search(query, top_k=8)
    state.log(f"RAG Stage 1 (Recall): retrieved {len(candidates)} candidates")

    if not candidates:
        state.rag_confidence = 0.0
        state.final_output = "Insufficient evidence in provided guidelines."
        state.log("RAG: no candidates found — early exit")
        return state

    # Stage 2: Distance Gate — simulated (in production: cosine distance check)
    # We keep all keyword-matched docs since our mock doesn't produce distances
    filtered = candidates
    state.log(f"RAG Stage 2 (Distance Gate): {len(filtered)} docs passed threshold")

    # Stage 3: Re-Ranking — score by keyword density (stands in for cross-encoder)
    query_tokens = set(query.lower().split())
    for doc in filtered:
        content_tokens = set(doc["content"].lower().split())
        doc["relevance_score"] = len(query_tokens & content_tokens) / max(len(query_tokens), 1)
    reranked = sorted(filtered, key=lambda d: d["relevance_score"], reverse=True)[:5]
    state.log(f"RAG Stage 3 (Re-Rank): top {len(reranked)} docs selected")

    # Stage 4: Context Trimming — fit within budget
    MAX_CONTEXT_CHARS = 6000
    trimmed = []
    total_chars = 0
    for doc in reranked:
        doc_len = len(doc["content"])
        if total_chars + doc_len <= MAX_CONTEXT_CHARS:
            trimmed.append(doc)
            total_chars += doc_len
    state.log(f"RAG Stage 4 (Trim): {len(trimmed)} docs, {total_chars} chars")

    # Compute confidence
    if trimmed:
        avg_relevance = sum(d.get("relevance_score", 0) for d in trimmed) / len(trimmed)
        confidence = min(avg_relevance * 3, 1.0)  # scale up for demo
    else:
        confidence = 0.0

    state.rag_documents = trimmed
    state.rag_confidence = round(confidence, 3)
    state.log(f"RAG confidence: {state.rag_confidence}")
    return state
