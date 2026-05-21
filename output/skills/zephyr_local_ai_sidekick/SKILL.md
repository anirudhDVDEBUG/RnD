---
name: zephyr_local_ai_sidekick
description: |
  Set up and run Zephyr, a local-first AI sidekick with a React control room, FastAPI bridge, MCP client support, RAG, and self-healing agentic workflows.
  Triggers: zephyr, local ai sidekick, local-first agent, react control room fastapi, self-healing ai agent, mcp client setup, rag local llm
---

# Zephyr Local AI Sidekick

Scaffold and operate **Zephyr** — a local-first AI sidekick featuring a React control room UI backed by a FastAPI bridge over a shared Python runtime. The browser UI is the default interface; the CLI remains available as an explicit fallback/operator surface.

## When to use

- "Set up a local-first AI agent with a browser UI and FastAPI backend"
- "I need a self-healing agentic workflow with RAG and MCP client support"
- "Help me build a Zephyr-style React control room backed by FastAPI"
- "Configure a local LLM orchestration system with retrieval-augmented generation"
- "Create an AI sidekick with skills, auto-improvement, and MCP integration"

## How to use

### 1. Clone and install Zephyr

```bash
git clone https://github.com/nabcht/Zephyr.git
cd Zephyr
```

Install Python dependencies (FastAPI bridge + shared runtime):

```bash
pip install -r requirements.txt
```

Install the React control room frontend:

```bash
cd frontend   # or wherever the React app lives
npm install
```

### 2. Architecture overview

Zephyr has three layers:

| Layer | Tech | Role |
|-------|------|------|
| **Control Room** | React + TypeScript | Browser-based default UI for interacting with the agent |
| **Bridge** | FastAPI (Python) | HTTP/WebSocket API bridging the UI to the shared Python runtime |
| **Runtime** | Python | Core agent logic — LLM orchestration, RAG pipeline, MCP client, skills, self-healing loops |

### 3. Key features to configure

- **Local LLM orchestration** — Runs against local models; no cloud dependency required.
- **RAG (Retrieval-Augmented Generation)** — Indexes local documents and augments LLM context with retrieved chunks.
- **MCP Client** — Connects to MCP servers to extend agent capabilities with external tools.
- **Self-healing AI** — Detects failures in agentic workflows and auto-retries or patches execution plans.
- **Skills system** — Modular skill definitions that the agent can discover and invoke.
- **Auto-improvement** — The agent can refine its own prompts and workflows over time.

### 4. Run the stack

Start the FastAPI bridge:

```bash
uvicorn main:app --reload --port 8000
```

Start the React control room:

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` (or the port shown) to access the control room.

The CLI fallback is available for operator/headless use:

```bash
python cli.py
```

### 5. Extending with MCP servers

Configure MCP server connections in the Zephyr config to give the agent access to additional tools (file systems, databases, APIs). The MCP client in the runtime handles discovery and invocation.

### 6. Adding RAG sources

Point the RAG pipeline at local directories or documents. The system will index content and use it to ground LLM responses with retrieved context.

## References

- **Source repository**: [nabcht/Zephyr](https://github.com/nabcht/Zephyr)
- **Topics**: agentic-workflow, ai-agents, auto-improvement, desktop-app, fastapi, llm-orchestration, local-llm, mcp, mcp-client, python, rag, retrieval-augmented-generation, self-healing-ai, skills, typescript
