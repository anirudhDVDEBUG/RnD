# Technical Details

## What it does

Orkestrai is a multi-agent orchestration platform that takes a single high-level task and autonomously coordinates multiple specialized LLM agents to produce a complete output. The Orchestrator agent decomposes the task into subtasks via an LLM call, then routes each subtask to the appropriate specialist agent (Planner, Researcher, Coder, Reviewer). Each agent has its own system prompt and can use a different LLM provider/model. Results flow back through the Orchestrator which assembles the final output.

The system supports multiple LLM providers (Anthropic Claude, OpenAI GPT) via a unified `LLMProvider` abstraction, making it easy to mix models — e.g., use Claude for planning and GPT-4o for code generation.

## Architecture

```
User Request
    |
    v
FastAPI /orchestrate endpoint
    |
    v
Orchestrator Agent
    |-- calls LLM to decompose task
    |-- routes subtasks to agents:
    |       |
    |       ├── PlannerAgent (task decomposition, ordering)
    |       ├── ResearcherAgent (context gathering, analysis)
    |       ├── CoderAgent (code/content generation)
    |       └── ReviewerAgent (quality scoring, suggestions)
    |
    v
Assembled AgentResult[] returned to client
```

### Key files

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app with `/orchestrate` and `/health` endpoints |
| `backend/agents/orchestrator.py` | Central coordinator, task decomposition, agent routing |
| `backend/agents/planner.py` | Breaks tasks into ordered subtask list |
| `backend/agents/researcher.py` | Gathers context and patterns for the task |
| `backend/agents/coder.py` | Generates code/content based on plan + research |
| `backend/agents/reviewer.py` | Scores output quality, suggests improvements |
| `backend/services/llm_provider.py` | Multi-provider LLM abstraction (Anthropic, OpenAI) |
| `backend/models/schemas.py` | Pydantic request/response models |
| `demo.py` | Standalone demo with mock LLM (no API keys needed) |

### Dependencies

- Python 3.10+
- `fastapi`, `uvicorn` — API server
- `httpx` — async HTTP client for LLM APIs
- `pydantic` — request/response validation
- No frontend dependencies for the demo (Next.js frontend is described in the skill but not required for evaluation)

### Model calls

Each agent makes 1 LLM call per invocation. A full orchestration run makes:
- 1 call for task decomposition (Orchestrator)
- 1 call per specialist agent invoked (typically 4)
- Total: ~5 LLM calls per task

## Limitations

- **No streaming** — agents return complete responses, no token-by-token streaming to the client
- **No memory/state** — each orchestration run is stateless; agents don't remember prior tasks
- **No parallel agent execution** — agents run sequentially (Planner -> Researcher -> Coder -> Reviewer)
- **No tool use** — agents can only generate text, they cannot browse the web, run code, or access files
- **Single-turn only** — no multi-turn conversation with the orchestrator
- **No authentication** — the FastAPI server has no auth; not production-ready as-is

## Why it matters for Claude-driven products

- **Agent factories**: This pattern is the building block for agent-factory platforms — you can dynamically register new specialist agents and have the orchestrator route to them
- **Marketing/ad creatives**: Chain a research agent (competitor analysis) -> copywriter agent -> reviewer agent to generate and QA ad copy autonomously
- **Lead-gen pipelines**: Orchestrate agents that research prospects, generate personalized outreach, and score/review before sending
- **Voice AI backends**: Use the orchestrator as the "brain" behind a voice agent, decomposing complex user requests into multi-step agent workflows
