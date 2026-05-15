# How to Use Granite Embedding Multilingual R2

## Install

```bash
pip install sentence-transformers numpy
```

That's it. Models auto-download from HuggingFace on first use (~380 MB for 97M, ~1.2 GB for 311M).

## Claude Skill Setup

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/granite_embedding_multilingual_r2
cp SKILL.md ~/.claude/skills/granite_embedding_multilingual_r2/SKILL.md
```

**Trigger phrases that activate the skill:**
- "I need multilingual embeddings"
- "Set up cross-lingual retrieval"
- "Use Granite embeddings with LangChain"
- "Help me with multilingual RAG pipeline"
- "I need code search embeddings"
- "sub-100M embedding model"
- "32K context embeddings"

Once installed, Claude will automatically use this skill when you mention any of the above contexts.

## First 60 Seconds

### Mock mode (no download, instant):
```bash
bash run.sh
```

Output shows cross-lingual retrieval, code search, and throughput benchmarks using simulated embeddings.

### Live mode (real model):
```bash
pip install sentence-transformers
python3 demo.py --live
```

### Minimal Python snippet:
```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("ibm-granite/granite-embedding-97m-multilingual-r2")

# Encode query and documents
q = model.encode(["What is machine learning?"])
d = model.encode(["Machine learning is a subset of AI that learns from data."])

# Cosine similarity
print(util.cos_sim(q, d))  # tensor([[0.85+]])
```

**Input:** Any text string in 200+ languages (up to 32K tokens).
**Output:** Dense float32 vector — 384-dim (97M model) or 768-dim (311M model).

## Integration Cheat Sheet

### LangChain
```python
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="ibm-granite/granite-embedding-97m-multilingual-r2"
)
```

### LlamaIndex
```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
Settings.embed_model = HuggingFaceEmbedding(
    model_name="ibm-granite/granite-embedding-97m-multilingual-r2"
)
```

### Haystack
```python
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
embedder = SentenceTransformersDocumentEmbedder(
    model="ibm-granite/granite-embedding-97m-multilingual-r2"
)
```

### Milvus
```python
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("ibm-granite/granite-embedding-97m-multilingual-r2")
client = MilvusClient("./milvus.db")
client.create_collection(collection_name="docs", dimension=384)
```

## Model Selection

| Model | Params | Dim | Use case |
|-------|--------|-----|----------|
| `granite-embedding-97m-multilingual-r2` | 97M | 384 | Speed, edge, low latency |
| `granite-embedding-311m-multilingual-r2` | 311M | 768 | Best quality, Matryoshka dims |

Both support 32K token context and 200+ languages.
