# How to Use — Zephyr Local AI Sidekick

## Install

```bash
# Clone this prototype
cd zephyr_local_ai_sidekick

# Install Python deps (Python 3.10+)
pip install -r requirements.txt
```

No Node/npm needed for the demo — the React control room is part of the full
Zephyr repo. This prototype focuses on the Python runtime + FastAPI bridge.

## Run the Demo

```bash
bash run.sh
```

This runs two things:
1. **Standalone demo** (`demo.py`) — exercises all 5 subsystems with colourful terminal output
2. **FastAPI bridge smoke test** — starts the server, hits every endpoint, prints JSON responses

No API keys, GPU, or external services required.

## First 60 Seconds

**Input:**
```bash
bash run.sh
```

**Output (abbreviated):**
```
══════════════════════════════════════════════════════════
   ZEPHYR  —  Local-First AI Sidekick Demo
══════════════════════════════════════════════════════════

── 1. Local LLM Orchestration ──────────────────────────
  > Hello Zephyr!
    Reasoning locally...
    Hello! I'm Zephyr, your local-first AI sidekick. How can I help?

── 2. RAG — Retrieval-Augmented Generation ─────────────
  Ingested 4 documents from sample_docs/
  Query: How does Zephyr use RAG to ground responses?
    [rag_explained.md] RAG retrieves relevant chunks from local documents...
  Answer: Based on the retrieved documents, the answer is: ...

── 3. MCP Client — Tool Discovery & Invocation ────────
  Connected to filesystem: tools=['read_file', 'write_file', 'list_directory']
  Invoke filesystem.read_file: {"result": "[mock] read_file executed successfully"}

── 4. Skills System ────────────────────────────────────
  Registered skills: 4
  Query: Please summarize the project README
  Matched skill: summarizer

── 5. Self-Healing Agentic Workflow ────────────────────
  Step fetch_data:    OK    result=fetch_data completed
  Step parse_response: EXHAUSTED  result=None
  ...

── FastAPI Bridge ──────────────────────────────────────
  GET /health:     {"status": "ok", "model": "mock-7b-q4", "rag_docs": 3}
  POST /chat:      {"response": "Based on the retrieved documents...", ...}
  GET /skills:     [{"name": "summarizer", ...}, ...]
  GET /mcp/tools:  [{"server": "filesystem", ...}, ...]
```

## Use as a Claude Skill

Drop the skill definition into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/zephyr_local_ai_sidekick
cp SKILL.md ~/.claude/skills/zephyr_local_ai_sidekick/SKILL.md
```

**Trigger phrases** that activate the skill:
- "zephyr"
- "local ai sidekick"
- "local-first agent"
- "react control room fastapi"
- "self-healing ai agent"
- "mcp client setup"
- "rag local llm"

## Use the FastAPI Bridge Directly

Start the server:
```bash
uvicorn bridge:app --reload --port 8000
```

Endpoints:
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check + model info |
| POST | `/chat` | Send a message, get RAG-augmented response |
| GET | `/skills` | List registered skills |
| GET | `/mcp/tools` | List connected MCP tools |
| POST | `/mcp/invoke` | Invoke an MCP tool |
| POST | `/self-heal/demo` | Run a flaky step through self-healing |
| WS | `/ws/chat` | WebSocket streaming chat |

Example:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Summarize Zephyr architecture", "use_rag": true}'
```

## Full Zephyr (with React Control Room)

For the complete experience with browser UI:

```bash
git clone https://github.com/nabcht/Zephyr.git
cd Zephyr
pip install -r requirements.txt
cd frontend && npm install && npm run dev
# In another terminal:
uvicorn main:app --reload --port 8000
```
