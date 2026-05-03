# Technical Details: mem0

## What It Does

mem0 is a memory management library that sits between your AI agent and a vector database. When you feed it raw conversation text, it uses an LLM to extract structured facts (e.g., "user prefers Python"), generates embeddings, and stores them in a vector store with metadata (user_id, agent_id, timestamps). On retrieval, it performs semantic search over stored memories and returns ranked results.

The key differentiator over raw vector DB usage: mem0 handles fact extraction, deduplication (adding overlapping info updates existing memories rather than creating duplicates), and temporal tracking (memory history) automatically. You pass in natural language; it manages the structured memory lifecycle.

## Architecture

```
Conversation text
       |
       v
  +----------+     +----------+     +--------------+
  |  mem0     | --> |  LLM     | --> | Fact         |
  |  .add()   |     | (OpenAI/ |     | Extraction   |
  |           |     | Claude/  |     | (JSON)       |
  +----------+     | Ollama)  |     +--------------+
       |           +----------+            |
       v                                   v
  +----------+     +----------+     +--------------+
  |  Embedder | --> | Vector   | <-- | Deduplicated |
  |  (OpenAI/ |     | Store    |     | Facts +      |
  |  HF)     |     | (Qdrant/ |     | Metadata     |
  +----------+     | Chroma/  |     +--------------+
                    | PGVector)|
                    +----------+
                         |
                         v
                    .search() / .get_all()
```

### Key Files (in the mem0 repo)

- `mem0/memory/main.py` -- Core `Memory` class, orchestrates add/search/update/delete
- `mem0/llms/` -- LLM provider adapters (OpenAI, Anthropic, Ollama, etc.)
- `mem0/vector_stores/` -- Vector DB adapters (Qdrant, Chroma, PGVector, etc.)
- `mem0/embeddings/` -- Embedding provider adapters
- `mem0/graphs/` -- Optional graph memory via Neo4j
- `mem0/configs/` -- Configuration schema and defaults

### Data Flow

1. **Add:** text -> LLM extracts facts -> embeddings generated -> upserted into vector store with user/agent/session metadata
2. **Search:** query -> embedding generated -> vector similarity search -> results ranked by score
3. **Update:** new text -> LLM re-extracts -> existing memory entry updated (not duplicated)
4. **History:** each update creates a versioned entry, enabling temporal queries

### Dependencies

- **Required:** `openai` (default LLM + embedder), `pydantic`
- **Optional:** `qdrant-client`, `chromadb`, `pgvector`, `neo4j`, `anthropic`, `ollama`
- Default mode uses an in-memory vector store (no external DB needed)

### Model Calls

- **add():** 1 LLM call (fact extraction) + 1 embedding call per input
- **search():** 1 embedding call per query (no LLM call)
- **update():** 1 LLM call + 1 embedding call

## Limitations

- **LLM dependency for writes:** Every `add()` call requires an LLM to extract facts. This adds latency (~1-2s) and cost per write. High-throughput ingestion can be expensive.
- **Extraction quality:** Fact extraction is only as good as the underlying LLM. Smaller/cheaper models may miss nuance or extract irrelevant facts.
- **No built-in auth:** Memory scoping (user_id, agent_id) is application-enforced. There's no access control layer -- any code with the Memory instance can read/write any user's data.
- **In-memory default is ephemeral:** The default vector store doesn't persist across restarts. Production use requires configuring Qdrant, Chroma, PGVector, etc.
- **No streaming:** add/search operations are synchronous. No async API in the open-source version.
- **Graph memory requires Neo4j:** The relationship-tracking feature needs a separate Neo4j instance.

## Why It Matters for Claude-Driven Products

| Use Case | How mem0 Helps |
|----------|----------------|
| **Agent factories** | Give each spawned agent persistent memory without building custom storage. Drop-in memory layer for multi-tenant agent platforms. |
| **Lead-gen / marketing bots** | Remember prospect preferences, past conversations, and objections across sessions. Personalize follow-ups automatically. |
| **Ad creative agents** | Store brand guidelines, past campaign performance notes, and client preferences. Retrieve relevant context for each new creative brief. |
| **Voice AI** | Maintain conversation context across calls. Remember user preferences for voice assistants that feel continuous, not stateless. |
| **Claude skill integration** | Use as a persistent knowledge layer behind Claude skills -- the skill extracts and stores insights, future invocations retrieve them. |

mem0 eliminates the need to build custom memory infrastructure. For teams shipping Claude-powered products, it's the difference between a stateless chatbot and a personalized agent that improves over time.
