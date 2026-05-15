---
name: granite_embedding_multilingual_r2
description: |
  Integrate IBM Granite Embedding Multilingual R2 models for multilingual and cross-lingual text retrieval, semantic search, and RAG pipelines.
  TRIGGER: user wants multilingual embeddings, cross-lingual retrieval, multilingual semantic search, granite embedding, sub-100M embedding model, 32K context embeddings, multilingual RAG pipeline, Matryoshka embeddings, or code search embeddings
---

# Granite Embedding Multilingual R2

Open-source (Apache 2.0) multilingual embedding models from IBM, built on ModernBERT with 32K token context and support for 200+ languages.

## When to use

- "I need multilingual embeddings for semantic search across languages"
- "Set up a RAG pipeline with cross-lingual retrieval"
- "I want a small, fast embedding model that supports many languages"
- "Help me use Granite embeddings with LangChain / LlamaIndex / Haystack / Milvus"
- "I need code search embeddings for Python, Java, JS, etc."

## Model Selection

| Model | Params | Embed Dim | Context | Best For |
|-------|--------|-----------|---------|----------|
| `ibm-granite/granite-embedding-311m-multilingual-r2` | 311M | 768 | 32K | Best quality, Matryoshka support (truncate to 512/384/256/128 dims) |
| `ibm-granite/granite-embedding-97m-multilingual-r2` | 97M | 384 | 32K | Max throughput, edge deployment, low latency (~2500 docs/sec on H100) |

## How to use

### 1. Install dependencies

```bash
pip install sentence-transformers
```

### 2. Basic multilingual embedding and retrieval

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("ibm-granite/granite-embedding-97m-multilingual-r2")

queries = [
    "What is the tallest mountain in Japan?",
    "Wer hat das Lied Achy Breaky Heart geschrieben?",
]
passages = [
    "Mount Fuji is the tallest peak in Japan at 3,776 m.",
    "Achy Breaky Heart is a country song written by Don Von Tress.",
]

q_emb = model.encode(queries)
p_emb = model.encode(passages)
print(util.cos_sim(q_emb, p_emb))
```

### 3. Matryoshka embeddings (311M model only)

```python
model = SentenceTransformer("ibm-granite/granite-embedding-311m-multilingual-r2")
full = model.encode(["example"])                      # (1, 768)
small = model.encode(["example"], truncate_dim=384)   # (1, 384)
tiny = model.encode(["example"], truncate_dim=128)    # (1, 128)
```

### 4. LangChain integration

```bash
pip install langchain-huggingface
```

```python
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="ibm-granite/granite-embedding-97m-multilingual-r2"
)
```

### 5. LlamaIndex integration

```bash
pip install llama-index-embeddings-huggingface
```

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
Settings.embed_model = HuggingFaceEmbedding(
    model_name="ibm-granite/granite-embedding-97m-multilingual-r2"
)
```

## Key facts

- **No task-specific instructions required** — works out of the box for queries and passages
- **32K token context** — handles long documents natively
- **ONNX & OpenVINO weights** available for CPU-optimized inference
- **97M model** scores 60.3 on MTEB Multilingual (vs 50.9 for multilingual-e5-small)
- **311M model** ranks #2 among open models under 500M params on MTEB Multilingual (65.2)
- **Languages:** 52 optimized + 200+ supported. Code: Python, Go, Java, JS, PHP, Ruby, SQL, C, C++
