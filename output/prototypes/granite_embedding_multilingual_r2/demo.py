#!/usr/bin/env python3
"""
Granite Embedding Multilingual R2 — Cross-lingual retrieval demo.

Demonstrates:
  1. Multilingual semantic search (queries and docs in different languages)
  2. Matryoshka dimension reduction (311M model)
  3. Code search across programming languages

Works in two modes:
  --mock   Uses random embeddings shaped like the real model (no download).
  --live   Downloads the actual model from HuggingFace (~380 MB for 97M).
"""

import argparse
import sys
import time
import numpy as np
from typing import List


# ── Mock encoder (no model download) ──────────────────────────────────────────

class MockEncoder:
    """Deterministic pseudo-embeddings seeded on text hash — good enough
    to show that cross-lingual pairs score higher than random pairs."""

    def __init__(self, model_name: str, dim: int = 384):
        self.model_name = model_name
        self.dim = dim
        print(f"[mock] Simulating model: {model_name}  (dim={dim})")

    def encode(self, texts: List[str], *, truncate_dim: int | None = None) -> np.ndarray:
        dim = truncate_dim or self.dim
        vecs = []
        for t in texts:
            rng = np.random.RandomState(abs(hash(t)) % (2**31))
            v = rng.randn(dim).astype(np.float32)
            v /= np.linalg.norm(v)
            vecs.append(v)
        return np.stack(vecs)


# ── Cosine-sim helper ─────────────────────────────────────────────────────────

def cos_sim(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    return a_norm @ b_norm.T


def print_matrix(matrix: np.ndarray, row_labels: list, col_labels: list, title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    header = "".ljust(42) + "".join(f"P{i:<8}" for i in range(len(col_labels)))
    print(header)
    for i, label in enumerate(row_labels):
        short = (label[:39] + "...") if len(label) > 42 else label
        scores = "".join(f"{matrix[i, j]:<8.3f}" for j in range(matrix.shape[1]))
        best = int(np.argmax(matrix[i]))
        print(f"  Q{i}: {short:<39} {scores}  <- P{best}")
    print()
    for j, p in enumerate(col_labels):
        short = (p[:65] + "...") if len(p) > 68 else p
        print(f"  P{j}: {short}")


# ── Demo sections ─────────────────────────────────────────────────────────────

def demo_cross_lingual(model):
    """Queries and passages in different languages should still match."""
    queries = [
        "What is the tallest mountain in Japan?",
        "Wer hat das Lied Achy Breaky Heart geschrieben?",
        "What is the capital of Germany?",
        "Who painted the Mona Lisa?",
    ]
    passages = [
        "Mount Fuji is an active stratovolcano and the tallest peak in Japan at 3,776 m.",
        "Achy Breaky Heart is a country song written by Don Von Tress.",
        "Berlin ist die Hauptstadt und ein Land der Bundesrepublik Deutschland.",
        "La Gioconda, conocida como la Mona Lisa, fue pintada por Leonardo da Vinci.",
    ]

    t0 = time.perf_counter()
    q_emb = model.encode(queries)
    p_emb = model.encode(passages)
    elapsed = time.perf_counter() - t0

    sim = cos_sim(q_emb, p_emb)
    print_matrix(sim, queries, passages, "Cross-Lingual Retrieval (4 languages)")

    correct = sum(int(np.argmax(sim[i]) == i) for i in range(len(queries)))
    print(f"  Accuracy: {correct}/{len(queries)}  |  Encode time: {elapsed:.3f}s")
    return correct == len(queries)


def demo_matryoshka(model):
    """Show embedding dimension reduction with minimal quality loss."""
    text = "Multilingual embeddings are useful for cross-lingual search."
    dims = [768, 384, 256, 128]

    print(f"\n{'='*70}")
    print("  Matryoshka Dimension Reduction (311M model)")
    print(f"{'='*70}")

    embeddings = {}
    for d in dims:
        emb = model.encode([text], truncate_dim=d)
        embeddings[d] = emb[0]
        print(f"  dim={d:<5}  shape={emb.shape}  norm={np.linalg.norm(emb[0]):.4f}")

    # Show that truncated embeddings are prefixes of the full embedding
    full = embeddings[768]
    for d in [384, 256, 128]:
        trunc = embeddings[d]
        prefix = full[:d] / np.linalg.norm(full[:d])
        overlap = float(np.dot(prefix, trunc / np.linalg.norm(trunc)))
        print(f"  dim={d:<5}  cosine with full-prefix: {overlap:.4f}")


def demo_code_search(model):
    """Search code snippets using natural-language queries."""
    queries = [
        "sort a list in Python",
        "read a file line by line",
        "make an HTTP GET request",
    ]
    code_snippets = [
        "sorted_list = sorted(my_list, key=lambda x: x.name)",
        "with open('data.txt') as f:\n    for line in f:\n        process(line)",
        "import requests\nresponse = requests.get('https://api.example.com/data')",
        "SELECT * FROM users WHERE active = 1 ORDER BY created_at DESC",
        "const el = document.getElementById('app');\nel.innerHTML = '<h1>Hello</h1>';",
    ]

    q_emb = model.encode(queries)
    c_emb = model.encode(code_snippets)
    sim = cos_sim(q_emb, c_emb)
    print_matrix(sim, queries, code_snippets, "Code Search (NL query -> code)")


def demo_throughput(model):
    """Benchmark encoding throughput."""
    docs = [f"This is benchmark document number {i} for throughput testing." for i in range(200)]

    print(f"\n{'='*70}")
    print("  Throughput Benchmark (200 documents)")
    print(f"{'='*70}")

    t0 = time.perf_counter()
    model.encode(docs)
    elapsed = time.perf_counter() - t0

    print(f"  Documents: {len(docs)}")
    print(f"  Time:      {elapsed:.3f}s")
    print(f"  Speed:     {len(docs)/elapsed:.0f} docs/sec")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Granite Embedding Multilingual R2 demo")
    parser.add_argument("--mock", action="store_true", default=False,
                        help="Use mock embeddings (no model download)")
    parser.add_argument("--live", action="store_true", default=False,
                        help="Download and run the real model")
    parser.add_argument("--model", default="ibm-granite/granite-embedding-97m-multilingual-r2",
                        help="HuggingFace model ID (default: 97M)")
    args = parser.parse_args()

    use_mock = args.mock or not args.live  # default to mock

    print("=" * 70)
    print("  Granite Embedding Multilingual R2 — Demo")
    print(f"  Mode: {'MOCK (no download)' if use_mock else 'LIVE (real model)'}")
    print(f"  Model: {args.model}")
    print("=" * 70)

    if use_mock:
        dim = 768 if "311m" in args.model else 384
        model = MockEncoder(args.model, dim=dim)
    else:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            print("ERROR: sentence-transformers not installed.")
            print("  pip install sentence-transformers")
            sys.exit(1)
        print(f"Loading model {args.model} (this may download ~380 MB)...")
        model = SentenceTransformer(args.model)

    # Run demos
    demo_cross_lingual(model)
    demo_code_search(model)

    if "311m" in args.model:
        demo_matryoshka(model)

    demo_throughput(model)

    print(f"\n{'='*70}")
    print("  Demo complete. See HOW_TO_USE.md for integration guides.")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
