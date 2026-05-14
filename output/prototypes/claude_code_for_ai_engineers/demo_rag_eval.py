"""
RAG Pipeline Evaluation Demo
Demonstrates the RAG evaluation methodology from the AI Engineering Skill Pack.
Uses mock data to show retrieval and generation quality assessment.
"""

import json
import random
import math
from typing import Any

random.seed(42)

# --- Mock RAG Pipeline Components ---

KNOWLEDGE_BASE = {
    "doc_1": "Claude Code is a CLI tool that lets developers use Claude directly in their terminal. It supports agentic coding with file editing, bash commands, and MCP integration.",
    "doc_2": "Model Context Protocol (MCP) is an open standard for connecting AI models to external data sources and tools. MCP servers expose resources and tools via JSON-RPC.",
    "doc_3": "RAG (Retrieval-Augmented Generation) combines a retriever that fetches relevant documents with a generator that produces answers grounded in retrieved context.",
    "doc_4": "Agent debugging involves tracing execution steps, inspecting tool calls, identifying reasoning loops, and diagnosing context overflow issues.",
    "doc_5": "Benchmark reporting requires selecting appropriate evaluation suites, configuring model parameters, executing evaluations, and aggregating results with statistical measures.",
    "doc_6": "Prompt engineering for RAG systems involves crafting system prompts that instruct the model to ground answers in provided context and cite sources.",
    "doc_7": "Chunking strategies for RAG include fixed-size chunks, semantic chunking, and recursive character splitting. Chunk size affects both retrieval precision and generation quality.",
    "doc_8": "Vector databases like Pinecone, Weaviate, and ChromaDB store embeddings for similarity search. The choice of embedding model significantly impacts retrieval quality.",
}

EVAL_QUERIES = [
    {
        "id": "q1",
        "query": "What is Claude Code and what can it do?",
        "relevant_docs": ["doc_1"],
        "reference_answer": "Claude Code is a CLI tool for developers that enables agentic coding with file editing, bash commands, and MCP integration.",
    },
    {
        "id": "q2",
        "query": "How does MCP work?",
        "relevant_docs": ["doc_2"],
        "reference_answer": "MCP is an open standard connecting AI models to external data sources and tools via JSON-RPC, exposing resources and tools through MCP servers.",
    },
    {
        "id": "q3",
        "query": "What is RAG and how does it work?",
        "relevant_docs": ["doc_3", "doc_6", "doc_7"],
        "reference_answer": "RAG combines document retrieval with language model generation. A retriever fetches relevant documents and a generator produces answers grounded in that context.",
    },
    {
        "id": "q4",
        "query": "How do you debug an AI agent?",
        "relevant_docs": ["doc_4"],
        "reference_answer": "Agent debugging involves tracing execution steps, inspecting tool calls, identifying reasoning loops, and diagnosing context overflow.",
    },
    {
        "id": "q5",
        "query": "What chunking strategies work best for RAG?",
        "relevant_docs": ["doc_7", "doc_8"],
        "reference_answer": "Common chunking strategies include fixed-size chunks, semantic chunking, and recursive splitting. Chunk size impacts retrieval precision and generation quality.",
    },
]


def mock_retrieve(query: str, k: int = 3) -> list[dict]:
    """Simulate retrieval with realistic imperfections."""
    scores = {}
    query_lower = query.lower()
    for doc_id, text in KNOWLEDGE_BASE.items():
        text_lower = text.lower()
        word_overlap = len(set(query_lower.split()) & set(text_lower.split()))
        noise = random.uniform(-0.5, 0.5)
        scores[doc_id] = word_overlap + noise

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [
        {"doc_id": doc_id, "score": round(score, 3), "text": KNOWLEDGE_BASE[doc_id]}
        for doc_id, score in ranked[:k]
    ]


def mock_generate(query: str, retrieved: list[dict]) -> str:
    """Simulate generation from retrieved context."""
    if not retrieved:
        return "I don't have enough information to answer this question."
    context_snippets = [r["text"][:80] for r in retrieved[:2]]
    return f"Based on the retrieved context: {context_snippets[0]}..."


def compute_retrieval_metrics(retrieved: list[dict], relevant_docs: list[str], k: int = 3) -> dict:
    """Compute retrieval quality metrics."""
    retrieved_ids = [r["doc_id"] for r in retrieved[:k]]
    relevant_set = set(relevant_docs)

    hits = [1 if doc_id in relevant_set else 0 for doc_id in retrieved_ids]
    precision_at_k = sum(hits) / k if k > 0 else 0
    recall_at_k = sum(hits) / len(relevant_set) if relevant_set else 0

    # Mean Reciprocal Rank
    mrr = 0.0
    for i, doc_id in enumerate(retrieved_ids):
        if doc_id in relevant_set:
            mrr = 1.0 / (i + 1)
            break

    return {
        "precision@k": round(precision_at_k, 3),
        "recall@k": round(recall_at_k, 3),
        "mrr": round(mrr, 3),
        "hits": hits,
    }


def compute_generation_metrics(answer: str, reference: str, retrieved: list[dict]) -> dict:
    """Compute generation quality metrics (simulated scoring)."""
    # Simulated faithfulness: are answer claims grounded in retrieved text?
    retrieved_text = " ".join(r["text"].lower() for r in retrieved)
    answer_words = set(answer.lower().split())
    context_words = set(retrieved_text.split())
    overlap = len(answer_words & context_words) / max(len(answer_words), 1)
    faithfulness = min(round(overlap + random.uniform(0, 0.2), 3), 1.0)

    # Simulated relevance: does answer address the query?
    ref_words = set(reference.lower().split())
    ans_words = set(answer.lower().split())
    relevance = min(round(len(ref_words & ans_words) / max(len(ref_words), 1) + random.uniform(0, 0.15), 3), 1.0)

    # Hallucination detection (simplified)
    hallucination_risk = round(max(0, 1.0 - faithfulness - random.uniform(0, 0.1)), 3)

    return {
        "faithfulness": faithfulness,
        "relevance": relevance,
        "hallucination_risk": hallucination_risk,
    }


def run_rag_evaluation() -> dict:
    """Run full RAG evaluation pipeline."""
    print("=" * 70)
    print("  RAG PIPELINE EVALUATION REPORT")
    print("=" * 70)
    print(f"\n  Knowledge Base: {len(KNOWLEDGE_BASE)} documents")
    print(f"  Eval Queries:   {len(EVAL_QUERIES)} queries")
    print(f"  Retrieval k:    3")
    print()

    results = []
    all_retrieval = {"precision@k": [], "recall@k": [], "mrr": []}
    all_generation = {"faithfulness": [], "relevance": [], "hallucination_risk": []}

    for q in EVAL_QUERIES:
        retrieved = mock_retrieve(q["query"], k=3)
        answer = mock_generate(q["query"], retrieved)
        ret_metrics = compute_retrieval_metrics(retrieved, q["relevant_docs"])
        gen_metrics = compute_generation_metrics(answer, q["reference_answer"], retrieved)

        for key in all_retrieval:
            all_retrieval[key].append(ret_metrics[key])
        for key in all_generation:
            all_generation[key].append(gen_metrics[key])

        results.append({
            "query_id": q["id"],
            "query": q["query"],
            "retrieved_docs": [r["doc_id"] for r in retrieved],
            "retrieval_metrics": ret_metrics,
            "generation_metrics": gen_metrics,
            "answer_preview": answer[:100],
        })

    # Per-query breakdown
    print("-" * 70)
    print(f"  {'Query':<45} {'P@3':>6} {'R@3':>6} {'MRR':>6} {'Faith':>6} {'Rel':>6}")
    print("-" * 70)
    for r in results:
        rm = r["retrieval_metrics"]
        gm = r["generation_metrics"]
        print(f"  {r['query'][:43]:<45} {rm['precision@k']:>6.3f} {rm['recall@k']:>6.3f} {rm['mrr']:>6.3f} {gm['faithfulness']:>6.3f} {gm['relevance']:>6.3f}")

    # Aggregate metrics
    def mean(lst):
        return round(sum(lst) / len(lst), 3) if lst else 0

    print("\n" + "=" * 70)
    print("  AGGREGATE METRICS")
    print("=" * 70)
    print(f"\n  Retrieval:")
    print(f"    Mean Precision@3:  {mean(all_retrieval['precision@k'])}")
    print(f"    Mean Recall@3:     {mean(all_retrieval['recall@k'])}")
    print(f"    Mean MRR:          {mean(all_retrieval['mrr'])}")
    print(f"\n  Generation:")
    print(f"    Mean Faithfulness:      {mean(all_generation['faithfulness'])}")
    print(f"    Mean Relevance:         {mean(all_generation['relevance'])}")
    print(f"    Mean Hallucination Risk: {mean(all_generation['hallucination_risk'])}")

    # Actionable recommendations
    print(f"\n  RECOMMENDATIONS")
    print(f"  " + "-" * 40)
    if mean(all_retrieval['recall@k']) < 0.7:
        print(f"  [!] Low recall — consider increasing k or using hybrid retrieval")
    if mean(all_retrieval['precision@k']) < 0.5:
        print(f"  [!] Low precision — try smaller chunks or re-ranking")
    if mean(all_generation['faithfulness']) < 0.8:
        print(f"  [!] Faithfulness below 0.8 — strengthen grounding in prompt template")
    if mean(all_generation['hallucination_risk']) > 0.2:
        print(f"  [!] Elevated hallucination risk — add citation requirements to prompt")
    print()

    report = {
        "summary": {
            "num_queries": len(EVAL_QUERIES),
            "num_documents": len(KNOWLEDGE_BASE),
            "retrieval": {k: mean(v) for k, v in all_retrieval.items()},
            "generation": {k: mean(v) for k, v in all_generation.items()},
        },
        "per_query": results,
    }
    return report


if __name__ == "__main__":
    report = run_rag_evaluation()
    with open("rag_eval_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("  Full report saved to rag_eval_report.json")
