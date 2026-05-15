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

**Languages:** 52 optimized languages including English, Chinese, Japanese, German, French, Spanish, Arabic, Hindi, Korean, and many more. 200+ languages supported total.

**Code:** Python, Go, Java, JavaScript, PHP, Ruby, SQL, C, C++

## How to use

### 1. Install dependencies

```bash
pip install sentence-transformers
```

### 2. Basic multilingual embedding and retrieval

```python
from sentence_transformers import SentenceTransformer, util

# Choose model: 97m for speed, 311m for quality
model = SentenceTransformer("ibm-granite/granite-embedding-97m-multilingual-r2")

queries = [
    "What is the tallest mountain in Japan?",
    "Wer hat das Lied Achy Breaky Heart geschrieben?",
    "ドイツの首都はどこですか？",
]

passages = [
    "富士山は、静岡県と山梨県にまたがる活火山で、標高3776.12 mで日本最高峰の独立峰である。",
    "Achy Breaky Heart is a country song written by Don Von Tress.",
    "Berlin ist die Hauptstadt und ein Land der Bundesrepublik Deutschland.",
]

q_emb = model.encode(queries)
p_emb = model.encode(passages)
print(util.cos_sim(q_emb, p_emb))
# Cross-lingual: each query matches its correct passage regardless of language
```

### 3. Matryoshka embeddings (311M model only)

Reduce embedding dimensions with minimal quality loss (~0.3% drop at 384d):

```python
model = SentenceTransformer("ibm-granite/granite-embedding-311m-multilingual-r2")

full = model.encode(["example"])           # shape: (1, 768)
small = model.encode(["example"], truncate_dim=384)  # shape: (1, 384)
tiny = model.encode(["example"], truncate_dim=128)   # shape: (1, 128)
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

doc_vectors = embeddings.embed_documents(["Doc text in any language..."])
query_vector = embeddings.embed_query("Query in any language")
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

### 6. Haystack integration

```bash
pip install sentence-transformers haystack-ai
```

```python
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.dataclasses import Document

MODEL = "ibm-granite/granite-embedding-97m-multilingual-r2"

doc_embedder = SentenceTransformersDocumentEmbedder(model=MODEL)
query_embedder = SentenceTransformersTextEmbedder(model=MODEL)
doc_embedder.warm_up()
query_embedder.warm_up()

store = InMemoryDocumentStore()
result = doc_embedder.run(documents=[Document(content="Your text here")])
store.write_documents(result["documents"])

query_result = query_embedder.run(text="Search query")
retriever = InMemoryEmbeddingRetriever(document_store=store)
results = retriever.run(query_embedding=query_result["embedding"], top_k=5)
```

### 7. Milvus vector database

```bash
pip install pymilvus sentence-transformers
```

```python
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("ibm-granite/granite-embedding-97m-multilingual-r2")

client = MilvusClient("./milvus.db")  # local file or server URI
client.create_collection(collection_name="docs", dimension=384)

docs = ["Text in any language..."]
embeddings = model.encode(docs).tolist()
client.insert(
    collection_name="docs",
    data=[{"id": i, "vector": emb, "text": doc}
          for i, (emb, doc) in enumerate(zip(embeddings, docs))],
)

query_emb = model.encode(["Search query"]).tolist()
results = client.search(
    collection_name="docs", data=query_emb, limit=5, output_fields=["text"]
)
```

## Key facts

- **No task-specific instructions required** — works out of the box for queries and passages
- **32K token context** — handles long documents natively (64x increase over R1)
- **ONNX & OpenVINO weights** available for CPU-optimized inference
- **97M model** is the best sub-100M retrieval model, scoring 60.3 on MTEB Multilingual (vs 50.9 for multilingual-e5-small)
- **311M model** ranks #2 among open models under 500M params on MTEB Multilingual (65.2)
- **Matryoshka** (311M only): truncate to 384 dims with only 0.3% quality loss

## References

- Blog post: https://huggingface.co/blog/ibm-granite/granite-embedding-multilingual-r2
- 97M model: https://huggingface.co/ibm-granite/granite-embedding-97m-multilingual-r2
- 311M model: https://huggingface.co/ibm-granite/granite-embedding-311m-multilingual-r2
- GitHub: https://github.com/ibm-granite/granite-embedding-models
- Technical report: https://arxiv.org/abs/2605.13521
