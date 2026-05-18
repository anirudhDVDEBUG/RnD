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

Build an autonomous multi-agent orchestration system. The platform coordinates multiple LLM-powered agents to collaboratively solve tasks — ideal for hackathon workflows, research pipelines, and agentic automation.

## When to use

- "Build a multi-agent orchestration system with FastAPI and Next.js"
- "Create an autonomous agent pipeline that coordinates multiple LLMs"
- "Set up a hackathon platform where AI agents collaborate on tasks"
- "Orchestrate multiple AI agents to break down and solve complex problems"
- "Scaffold a full-stack app with a FastAPI agent backend and React frontend"

## Architecture

```
Orchestrator
  ├── PlannerAgent     — decomposes task into subtasks
  ├── ResearcherAgent  — gathers context and patterns
  ├── CoderAgent       — generates code/content
  └── ReviewerAgent    — scores quality, suggests improvements
```

## Implementation pattern

1. Create `LLMProvider` class abstracting Anthropic + OpenAI APIs
2. Create specialist agent functions with role-specific system prompts
3. Create `Orchestrator` that registers agents and runs them in sequence
4. Wrap in FastAPI with `/orchestrate` POST endpoint
5. Each agent receives accumulated context from prior agents

## Key code

```python
from services.llm_provider import LLMProvider
from agents.orchestrator import Orchestrator
from agents.planner import run as planner_run
from agents.researcher import run as researcher_run
from agents.coder import run as coder_run
from agents.reviewer import run as reviewer_run

llm = LLMProvider(mock_mode=False)
orch = Orchestrator(llm)
orch.register("Planner", planner_run)
orch.register("Researcher", researcher_run)
orch.register("Coder", coder_run)
orch.register("Reviewer", reviewer_run)

results = await orch.run("Build a landing page for a SaaS product")
```
