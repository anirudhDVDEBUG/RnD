# How to Use mem0

## Install

```bash
pip install mem0ai
```

For the managed platform (no infra to run):
```bash
pip install mem0ai
# Get API key from https://app.mem0.ai
```

## Claude Skill Setup

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/mem0_memory_layer
cp SKILL.md ~/.claude/skills/mem0_memory_layer/SKILL.md
```

**Trigger phrases** that activate the skill:
- "Add long-term memory to my AI agent"
- "Integrate mem0 for persistent agent memory"
- "Set up a memory layer with vector search"
- "I want my chatbot to remember user preferences"
- Any code that `import mem0`

## First 60 Seconds

### Without API keys (mock demo)

```bash
bash run.sh
```

This runs a full lifecycle demo (add, search, retrieve, delete, multi-level scoping) using mocked LLM/embedding calls. No external services needed.

### With a real OpenAI key

```bash
export OPENAI_API_KEY="sk-..."
python3 -c "
from mem0 import Memory
m = Memory()

# Add a memory
m.add('I prefer Python and dark mode.', user_id='alice')

# Search it back
results = m.search('programming language preference', user_id='alice')
for r in results:
    print(r['memory'], r['score'])
"
```

**Input:** Raw conversation text + a `user_id`.
**Output:** Extracted facts stored in a vector DB, retrievable by semantic search.

### With the managed platform

```python
from mem0 import MemoryClient

client = MemoryClient(api_key="your-mem0-api-key")  # from https://app.mem0.ai
client.add("Likes hiking on weekends", user_id="bob")
results = client.search("hobbies", user_id="bob")
print(results)
```

## Configuration Options

### Custom vector store (e.g., Qdrant)

```python
from mem0 import Memory

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "agent_memories",
            "host": "localhost",
            "port": 6333,
        }
    },
    "llm": {
        "provider": "openai",
        "config": {"model": "gpt-4o", "temperature": 0.1}
    },
    "version": "v1.1"
}

m = Memory.from_config(config)
```

### Supported backends

| Component | Providers |
|-----------|-----------|
| Vector store | Qdrant, Chroma, PGVector, Milvus, Pinecone (default: in-memory) |
| LLM | OpenAI, Anthropic, Ollama, Groq, Together |
| Embedder | OpenAI, HuggingFace, Ollama |
| Graph store | Neo4j (optional, for relationship tracking) |

## Memory Scoping

```python
# User-level (personal preferences)
m.add("Prefers concise answers", user_id="alice")

# Agent-level (shared behavior)
m.add("This agent handles billing", agent_id="billing-bot")

# Session-level (conversation context)
m.add("Discussing order #12345", user_id="alice", run_id="session-abc")
```
