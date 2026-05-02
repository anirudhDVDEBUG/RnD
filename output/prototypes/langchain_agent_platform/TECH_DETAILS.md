# Technical Details

## What LangChain Actually Does

LangChain is a Python/JS framework for building LLM-powered applications through composable abstractions. Its core innovation is **LangChain Expression Language (LCEL)** — a declarative way to chain prompts, models, retrievers, and output parsers using the `|` pipe operator. Each component implements a `Runnable` interface with `invoke()`, `stream()`, `batch()`, and async variants, making any chain automatically streamable and batchable.

The framework is modular: `langchain-core` provides base abstractions, provider packages (`langchain-anthropic`, `langchain-openai`) wrap specific APIs, and `langchain-community` offers 700+ integrations (vector stores, document loaders, tools).

## Architecture

```
User Query
    |
    v
[PromptTemplate] -- formats input variables into messages
    |
    v
[ChatModel] -- calls LLM (Anthropic/OpenAI/local)
    |
    v
[OutputParser] -- extracts structured data or plain text
    |
    v
Result

For RAG:
[DocumentLoader] -> [TextSplitter] -> [Embeddings] -> [VectorStore]
                                                           |
User Query -> [Retriever] -> retrieved docs -> [PromptTemplate] -> [LLM] -> Answer
```

### Key Files in This Demo

| File | Purpose |
|------|---------|
| `mock_llm.py` | Fake ChatModel that returns canned responses (no API key needed) |
| `demo_chain.py` | LCEL chain: prompt | llm | StrOutputParser |
| `demo_agent.py` | Tool-calling agent with calculator tool |
| `demo_rag.py` | Full RAG pipeline: load docs, split, embed, retrieve, answer |
| `demo_structured.py` | Pydantic structured output parsing |
| `run.sh` | Orchestrator that runs all demos sequentially |

### Dependencies

- **langchain-core** (0.3+): Runnable protocol, prompt templates, output parsers
- **langchain** (0.3+): Higher-level chains and agent utilities
- **langchain-community** (0.3+): FAISS vector store, HuggingFace embeddings (mocked here)
- **faiss-cpu**: Facebook's vector similarity search library
- **pydantic** (v2): Structured output schema validation

## Limitations

- **No streaming in mock mode** — the mock LLM returns full responses, not token-by-token
- **No real embeddings** — uses deterministic fake embeddings for demo reproducibility
- **Agent loop is simulated** — real tool-calling requires a model that supports function calling
- **No persistence** — vector store lives in memory; production would use Chroma/Pinecone/pgvector
- **No LangSmith tracing** — would need `LANGCHAIN_API_KEY` for observability

## Why This Matters for Claude-Driven Products

| Use Case | LangChain Role |
|----------|---------------|
| **Lead-gen chatbots** | RAG over product docs + structured extraction of lead info |
| **Marketing content** | LCEL chains for multi-step content generation pipelines |
| **Agent factories** | Tool-calling agents that can browse, calculate, query databases |
| **Ad creatives** | Structured output for generating ad copy in specific formats |
| **Voice AI** | Streaming chains with low-latency token delivery |

LangChain provides the plumbing so you focus on business logic, not LLM API wrangling. Combined with LangGraph (for stateful multi-step agents) and LangSmith (for tracing/evaluation), it's a full production stack.
