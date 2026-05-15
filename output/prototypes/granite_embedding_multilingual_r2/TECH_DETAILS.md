# Technical Details — Granite Embedding Multilingual R2

## What it does

Granite Embedding Multilingual R2 is a family of two dense text embedding models (97M and 311M parameters) from IBM Research that convert text in 200+ languages into fixed-dimensional vectors for semantic similarity, retrieval, and RAG. Built on the ModernBERT architecture with rotary positional encodings, they handle up to 32K tokens of context — a 64x increase over the R1 generation. The models require no task-specific query prefixes or instructions; you encode queries and documents identically.

Training uses a three-stage pipeline: (1) weakly-supervised contrastive pre-training on ~1B text pairs, (2) fine-tuning on curated retrieval datasets across 52 languages plus 9 programming languages, and (3) Matryoshka Representation Learning (311M only) so the embedding can be truncated to 512/384/256/128 dimensions with minimal quality loss (~0.3% at 384d).

## Architecture

- **Base:** ModernBERT (encoder-only transformer with Flash Attention 2, rotary embeddings)
- **97M model:** 384-dim output, ~380 MB download, ~2500 docs/sec on H100
- **311M model:** 768-dim output, ~1.2 GB download, Matryoshka support
- **Context:** 32,768 tokens (BPE tokenizer)
- **License:** Apache 2.0

### Data flow

```
Text input (any language, up to 32K tokens)
  -> ModernBERT tokenizer (BPE)
  -> Transformer encoder (6 or 12 layers)
  -> [CLS] token pooling
  -> L2-normalized dense vector (384d or 768d)
  -> Cosine similarity for retrieval
```

### Key dependencies

- `sentence-transformers` (primary interface)
- `transformers` + `torch` (underlying inference)
- ONNX / OpenVINO weights available for CPU-optimized deployment

## Benchmark results

| Benchmark | 97M | 311M | Comparison |
|-----------|-----|------|------------|
| MTEB Multilingual | 60.3 | 65.2 | multilingual-e5-small: 50.9 |
| MTEB English | — | 68.1 | #2 among open <500M models |
| Matryoshka 384d | — | 64.9 | Only 0.3% below full 768d |

## Limitations

- **Not a reranker.** These are bi-encoders — they produce independent embeddings, not cross-attention scores. For reranking, pair with a cross-encoder.
- **No generative capability.** Embedding-only; cannot answer questions or summarize.
- **52 optimized languages.** While 200+ languages are nominally supported, only 52 have dedicated training data. Low-resource languages will have weaker retrieval quality.
- **GPU recommended for throughput.** CPU inference works (especially with ONNX) but is 10-50x slower for batch encoding.
- **No sparse/hybrid retrieval.** Dense vectors only — no BM25-style term matching built in.

## Why this matters for Claude-driven products

### RAG pipelines
The 32K context means you can embed entire documents without chunking, reducing retrieval noise. For Claude-based assistants serving multilingual users, these embeddings let you build a single vector index across all languages instead of maintaining per-language collections.

### Lead-gen and marketing
Cross-lingual retrieval enables matching prospect queries in their native language against your English content database. A Claude agent doing market research across Japanese, German, and Spanish sources can use a single embedding space.

### Agent factories
The 97M model's small size (~380 MB) and high throughput (~2500 docs/sec) make it viable for embedding-on-the-fly in agent workflows without dedicated GPU infrastructure. Matryoshka support in the 311M model lets you trade quality for speed/storage dynamically.

### Code search
Native support for 9 programming languages means Claude agents can retrieve relevant code snippets using natural-language queries, useful for code-gen agents that need to find existing patterns in a codebase before writing new code.

### Voice AI
Low-latency embedding (97M model) is fast enough for real-time voice assistant pipelines where you need to retrieve context before generating a spoken response.
