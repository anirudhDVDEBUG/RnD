---
name: orkestrai_multi_agent_orchestrator
description: >
  Scaffold and run an autonomous multi-agent orchestration platform for hackathons
  using FastAPI (backend), Next.js (frontend), and multi-provider LLMs.
  TRIGGER: user wants to build a multi-agent system, orchestrate LLM agents for a
  hackathon, create an agent pipeline with FastAPI and Next.js, or coordinate
  multiple AI agents autonomously.
---

# Orkestrai — Multi-Agent Orchestration Platform

Build an autonomous multi-agent orchestration system inspired by [Orkestrai](https://github.com/grsanudeep42-cmd/Orkestrai). The platform coordinates multiple LLM-powered agents to collaboratively solve tasks — ideal for hackathon workflows, research pipelines, and agentic automation.

## When to use

- "Build a multi-agent orchestration system with FastAPI and Next.js"
- "Create an autonomous agent pipeline that coordinates multiple LLMs"
- "Set up a hackathon platform where AI agents collaborate on tasks"
- "Orchestrate multiple AI agents to break down and solve complex problems"
- "Scaffold a full-stack app with a FastAPI agent backend and React frontend"

## How to use

### 1. Scaffold the project structure

```
orkestrai/
├── backend/
│   ├── main.py              # FastAPI app entrypoint
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py  # Central orchestrator agent
│   │   ├── planner.py       # Task decomposition agent
│   │   ├── researcher.py    # Information gathering agent
│   │   ├── coder.py         # Code generation agent
│   │   └── reviewer.py      # Quality review agent
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic request/response models
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_provider.py  # Multi-provider LLM abstraction
│   ├── config.py            # Settings and env var loading
│   └── requirements.txt
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx     # Main orchestration dashboard
│   │   │   └── layout.tsx
│   │   └── components/
│   │       ├── AgentPanel.tsx
│   │       ├── TaskFlow.tsx
│   │       └── ChatInterface.tsx
│   └── next.config.js
├── .env.example
└── README.md
```

### 2. Set up the FastAPI backend

Create the multi-provider LLM service (`backend/services/llm_provider.py`):

```python
import os
from typing import Optional
import httpx

class LLMProvider:
    """Abstraction over multiple LLM providers (OpenAI, Anthropic, etc.)."""

    def __init__(self):
        self.providers = {
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "base_url": "https://api.anthropic.com/v1",
                "default_model": "claude-sonnet-4-20250514",
            },
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": "https://api.openai.com/v1",
                "default_model": "gpt-4o",
            },
        }

    async def complete(
        self, prompt: str, provider: str = "anthropic",
        model: Optional[str] = None, system: Optional[str] = None
    ) -> str:
        cfg = self.providers[provider]
        model = model or cfg["default_model"]

        if provider == "anthropic":
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{cfg['base_url']}/messages",
                    headers={
                        "x-api-key": cfg["api_key"],
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": model,
                        "max_tokens": 4096,
                        "system": system or "You are a helpful assistant.",
                        "messages": [{"role": "user", "content": prompt}],
                    },
                    timeout=120.0,
                )
                resp.raise_for_status()
                return resp.json()["content"][0]["text"]

        elif provider == "openai":
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{cfg['base_url']}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {cfg['api_key']}",
                        "Content-Type": "application/json",
                    },
                    json={"model": model, "messages": messages, "max_tokens": 4096},
                    timeout=120.0,
                )
                resp.raise_for_status()
                return resp.json()["choices"][0]["message"]["content"]
```

Create the orchestrator agent (`backend/agents/orchestrator.py`):

```python
from dataclasses import dataclass
from typing import Any
from services.llm_provider import LLMProvider

@dataclass
class AgentResult:
    agent_name: str
    output: str
    metadata: dict[str, Any] | None = None

class Orchestrator:
    """Central coordinator that decomposes tasks and delegates to specialist agents."""

    def __init__(self, llm: LLMProvider):
        self.llm = llm
        self.agents: dict[str, callable] = {}

    def register(self, name: str, agent_fn):
        self.agents[name] = agent_fn

    async def run(self, task: str) -> list[AgentResult]:
        # Step 1: Plan — decompose the task into subtasks
        plan = await self.llm.complete(
            prompt=f"Decompose this task into ordered subtasks. Return as numbered list:\n\n{task}",
            system="You are a project planner. Break complex tasks into concrete, actionable subtasks.",
        )

        # Step 2: Assign subtasks to agents
        assignment = await self.llm.complete(
            prompt=(
                f"Given these subtasks:\n{plan}\n\n"
                f"Available agents: {list(self.agents.keys())}\n\n"
                "Assign each subtask to the best agent. Format: subtask | agent_name"
            ),
            system="You are a task router. Match subtasks to the most capable agent.",
        )

        # Step 3: Execute each assigned subtask
        results = []
        for line in assignment.strip().split("\n"):
            if "|" not in line:
                continue
            subtask, agent_name = [s.strip() for s in line.split("|", 1)]
            agent_name = agent_name.lower().strip()
            if agent_name in self.agents:
                result = await self.agents[agent_name](subtask)
                results.append(AgentResult(agent_name=agent_name, output=result))

        return results
```

Create the FastAPI app (`backend/main.py`):

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.orchestrator import Orchestrator
from services.llm_provider import LLMProvider

app = FastAPI(title="Orkestrai")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

llm = LLMProvider()
orchestrator = Orchestrator(llm)

# Register specialist agents
async def researcher(task: str) -> str:
    return await llm.complete(task, system="You are a research agent. Provide thorough, factual analysis.")

async def coder(task: str) -> str:
    return await llm.complete(task, system="You are an expert programmer. Write clean, working code.")

async def reviewer(task: str) -> str:
    return await llm.complete(task, system="You are a code reviewer. Identify bugs, improvements, and security issues.")

orchestrator.register("researcher", researcher)
orchestrator.register("coder", coder)
orchestrator.register("reviewer", reviewer)

class TaskRequest(BaseModel):
    task: str

@app.post("/api/orchestrate")
async def orchestrate(req: TaskRequest):
    results = await orchestrator.run(req.task)
    return {"results": [{"agent": r.agent_name, "output": r.output} for r in results]}

@app.get("/api/health")
async def health():
    return {"status": "ok"}
```

### 3. Set up the Next.js frontend

Create a minimal orchestration dashboard (`frontend/src/app/page.tsx`):

```tsx
"use client";
import { useState } from "react";

interface AgentResult {
  agent: string;
  output: string;
}

export default function Home() {
  const [task, setTask] = useState("");
  const [results, setResults] = useState<AgentResult[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    const res = await fetch("http://localhost:8000/api/orchestrate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task }),
    });
    const data = await res.json();
    setResults(data.results);
    setLoading(false);
  }

  return (
    <main className="max-w-4xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Orkestrai</h1>
      <form onSubmit={handleSubmit} className="mb-8">
        <textarea
          value={task}
          onChange={(e) => setTask(e.target.value)}
          placeholder="Describe your task..."
          className="w-full p-4 border rounded-lg mb-4 min-h-[120px]"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg disabled:opacity-50"
        >
          {loading ? "Orchestrating..." : "Run Agents"}
        </button>
      </form>
      {results.map((r, i) => (
        <div key={i} className="border rounded-lg p-4 mb-4">
          <h3 className="font-semibold text-blue-600 mb-2">{r.agent}</h3>
          <pre className="whitespace-pre-wrap text-sm">{r.output}</pre>
        </div>
      ))}
    </main>
  );
}
```

### 4. Configure environment and run

Create `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...        # optional, for multi-provider support
```

Start the backend:
```bash
cd backend
pip install fastapi uvicorn httpx python-dotenv
uvicorn main:app --reload --port 8000
```

Start the frontend:
```bash
cd frontend
npx create-next-app@latest . --typescript --tailwind --app
npm run dev
```

### 5. Extend with custom agents

Register new specialist agents by adding async functions to the orchestrator:

```python
async def designer(task: str) -> str:
    return await llm.complete(task, system="You are a UI/UX designer. Describe layouts and user flows.")

orchestrator.register("designer", designer)
```

## Key concepts

- **Orchestrator pattern**: A central agent decomposes tasks, assigns subtasks to specialists, and aggregates results
- **Multi-provider LLM**: Abstract over Anthropic, OpenAI, or other providers — swap models per agent
- **Agent registration**: Plug in new specialist agents without changing orchestration logic
- **Hackathon-ready**: Designed for rapid prototyping with minimal boilerplate

## References

- Source repository: [grsanudeep42-cmd/Orkestrai](https://github.com/grsanudeep42-cmd/Orkestrai)
- Topics: ai-agents, fastapi, hackathon, llm, nextjs, orchestration
