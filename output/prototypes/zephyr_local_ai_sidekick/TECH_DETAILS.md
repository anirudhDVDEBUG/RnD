# Technical Details — Zephyr Local AI Sidekick

## What It Does

Zephyr is a **local-first AI agent** that runs entirely on your machine. It combines a React browser UI ("control room") with a FastAPI Python backend ("bridge") over a shared runtime that orchestrates local LLM inference, retrieval-augmented generation, MCP-based tool discovery, a modular skills system, and self-healing workflow execution.

The core value proposition: **an agent that operates without cloud dependencies**, keeping data local while still supporting extensibility through MCP and a plugin-like skills architecture. The self-healing engine adds resilience to multi-step agentic workflows by automatically retrying and adjusting execution plans on transient failures.

## Architecture

```
┌─────────────────────────────┐
│   React Control Room (UI)   │  Browser-based default interface
│   TypeScript + WebSocket    │  Communicates over HTTP/WS
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│      FastAPI Bridge         │  bridge.py
│  REST + WebSocket endpoints │  /chat, /skills, /mcp/*, /self-heal/*
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│     Python Runtime          │  runtime/
│  ┌─────────┐ ┌───────────┐ │
│  │ LocalLLM│ │RAGPipeline│ │  llm.py, rag.py
│  └─────────┘ └───────────┘ │
│  ┌─────────┐ ┌───────────┐ │
│  │MCPClient│ │  Skills   │ │  mcp_client.py, skills.py
│  └─────────┘ └───────────┘ │
│  ┌─────────────────────────┐│
│  │  SelfHealingEngine      ││  self_heal.py
│  └─────────────────────────┘│
└─────────────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `bridge.py` | FastAPI app with REST + WebSocket endpoints |
| `demo.py` | Standalone demo exercising all subsystems |
| `runtime/llm.py` | Mock local LLM with latency simulation and token counting |
| `runtime/rag.py` | Keyword-based inverted-index RAG pipeline |
| `runtime/mcp_client.py` | Mock MCP client — connect, discover tools, invoke |
| `runtime/skills.py` | Skill registry with trigger matching and execution |
| `runtime/self_heal.py` | Retry engine with exponential backoff and failure logging |
| `sample_docs/` | Markdown files ingested by the RAG pipeline |

### Data Flow (Chat Request)

1. User sends message via REST (`POST /chat`) or WebSocket (`/ws/chat`)
2. Bridge passes query to RAG pipeline → retrieves top-k relevant chunks
3. Retrieved context + original query sent to LocalLLM for generation
4. If a skill matches the query, it's invoked in parallel
5. Response returned with token count, retrieved doc count, model info

### Dependencies

- **FastAPI** + **Uvicorn** — HTTP/WS server
- **Pydantic** — request validation
- **websockets** — WebSocket transport
- Python 3.10+ standard library (no ML frameworks, no vector DBs)

### Model Calls

This prototype uses a **mock LLM** (`runtime/llm.py`) that returns canned responses matched by keyword. The full Zephyr repo supports local model backends (Ollama, llama.cpp, etc.). Swapping in a real model requires changing only the `LocalLLM.generate()` method.

## Limitations

- **No real LLM inference** — this prototype uses keyword-matched mock responses. It demonstrates architecture and data flow, not model quality.
- **RAG is keyword-based** — uses a simple inverted index, not vector embeddings. Good enough to show the retrieval→augmentation flow; production would use FAISS/ChromaDB.
- **MCP client is simulated** — connects to mock servers defined in code, not real MCP server processes.
- **No React UI included** — this prototype focuses on the Python backend. The full repo has the React control room.
- **No persistence** — RAG index and conversation state live in memory only.

## Why It Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Agent factories** | Zephyr's layered architecture (UI → bridge → runtime) is a clean template for building agent products. The skills registry pattern maps directly to Claude Code's skill system. |
| **Local-first / privacy** | For industries where data can't leave the machine (legal, healthcare, finance), Zephyr's local-only design is a starting point. Swap the mock LLM for a local model and you have a private agent. |
| **MCP integration** | The MCP client pattern shows how to give agents tool access — same protocol Claude Code uses. Building MCP server wrappers around your product's API turns it into an agent-accessible tool. |
| **Self-healing workflows** | Multi-step agentic tasks (lead-gen pipelines, ad creative generation, content production) fail at individual steps. The self-healing pattern keeps workflows running without human intervention. |
| **RAG for grounding** | Any Claude product that needs to reference local documents (marketing copy, customer data, codebase) benefits from this retrieval→augmentation pattern. |
