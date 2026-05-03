---
name: mem0_memory_layer
description: |
  Integrate mem0 as a universal memory layer for AI agents and chatbots.
  TRIGGER when: code imports `mem0`, user mentions "mem0", "memory layer for agents",
  "persistent agent memory", "long-term memory for LLM", or wants to add/search/manage
  memories across AI agent sessions.
  DO NOT TRIGGER when: general vector DB usage without mem0, or unrelated memory/RAM topics.
---

# mem0 — Universal Memory Layer for AI Agents

Add persistent, structured memory to any AI agent or chatbot using [mem0](https://github.com/mem0ai/mem0). mem0 automatically extracts, stores, and retrieves relevant memories from conversations, enabling personalized and context-aware interactions across sessions.

## When to use

- "Add long-term memory to my AI agent"
- "I want my chatbot to remember user preferences across sessions"
- "Integrate mem0 for persistent agent memory"
- "Set up a memory layer with vector search for my LLM app"
- "Use mem0 to store and retrieve conversation context"

## How to use

### 1. Install mem0

```bash
pip install mem0ai
```

### 2. Basic usage (open-source, in-process)

```python
from mem0 import Memory

# Initialize with defaults (uses in-memory vector store + OpenAI)
m = Memory()

# Add a memory for a specific user
result = m.add(
    "I prefer dark mode and Python over JavaScript.",
    user_id="alice",
    metadata={"category": "preferences"}
)
print(result)  # Returns memory ID and extracted facts

# Search memories by natural language query
results = m.search("What programming language does she like?", user_id="alice")
for r in results:
    print(r["memory"], r["score"])

# Get all memories for a user
all_memories = m.get_all(user_id="alice")

# Get a specific memory by ID
memory = m.get(memory_id="<memory_id>")

# Update a memory
m.update(memory_id="<memory_id>", data="I now prefer light mode.")

# View memory history (tracks changes over time)
history = m.history(memory_id="<memory_id>")

# Delete a specific memory
m.delete(memory_id="<memory_id>")

# Delete all memories for a user
m.delete_all(user_id="alice")

# Reset all memories
m.reset()
```

### 3. Custom configuration

mem0 supports pluggable vector stores, LLMs, and embedding models:

```python
from mem0 import Memory

config = {
    "vector_store": {
        "provider": "qdrant",  # or "chroma", "pgvector", "milvus", "pinecone", etc.
        "config": {
            "collection_name": "agent_memories",
            "host": "localhost",
            "port": 6333,
        }
    },
    "llm": {
        "provider": "openai",  # or "anthropic", "ollama", "groq", etc.
        "config": {
            "model": "gpt-4o",
            "temperature": 0.1,
        }
    },
    "embedder": {
        "provider": "openai",  # or "huggingface", "ollama", etc.
        "config": {
            "model": "text-embedding-3-small",
        }
    },
    "graph_store": {  # Optional: enable graph memory for relationship tracking
        "provider": "neo4j",
        "config": {
            "url": "neo4j://localhost:7687",
            "username": "neo4j",
            "password": "password",
        }
    },
    "version": "v1.1"
}

m = Memory.from_config(config)
```

### 4. Platform (managed) usage

```python
from mem0 import MemoryClient

client = MemoryClient(api_key="your-mem0-api-key")

# Same API as open-source: add, search, get_all, delete, etc.
client.add("Likes hiking on weekends", user_id="bob")
results = client.search("hobbies", user_id="bob")
```

### 5. Multi-level memory organization

mem0 supports scoping memories to different levels:

```python
# User-level memory
m.add("Prefers concise answers", user_id="alice")

# Agent-level memory (shared across users for a specific agent)
m.add("This agent handles billing inquiries", agent_id="billing-bot")

# Session-level memory (scoped to a conversation)
m.add("Currently discussing order #12345", user_id="alice", run_id="session-abc")
```

### Key design decisions

- **Automatic extraction**: mem0's LLM extracts structured facts from raw messages — you don't manually craft memory entries.
- **Deduplication**: Adding overlapping information updates existing memories rather than creating duplicates.
- **Relevance scoring**: Search returns scored results so you can threshold or rank.
- **Set `OPENAI_API_KEY`** (or relevant provider key) in your environment before using.

## References

- **Repository**: https://github.com/mem0ai/mem0
- **Documentation**: https://docs.mem0.ai
- **PyPI**: https://pypi.org/project/mem0ai/
