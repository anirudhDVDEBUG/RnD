"""FastAPI entrypoint for the Orkestrai multi-agent orchestrator."""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from agents import Orchestrator
from agents.planner import run as planner_run
from agents.researcher import run as researcher_run
from agents.coder import run as coder_run
from agents.reviewer import run as reviewer_run
from models.schemas import OrchestrationRequest, OrchestrationResponse, AgentOutput
from services.llm_provider import LLMProvider

app = FastAPI(title="Orkestrai", description="Multi-Agent Orchestration Platform")


def _is_mock() -> bool:
    return os.getenv("MOCK_MODE", "true").lower() in ("true", "1", "yes")


@app.get("/health")
async def health():
    return {"status": "ok", "mock_mode": _is_mock()}


@app.post("/orchestrate", response_model=OrchestrationResponse)
async def orchestrate(req: OrchestrationRequest):
    llm = LLMProvider(mock_mode=_is_mock())
    orch = Orchestrator(llm)
    orch.register("Planner", planner_run)
    orch.register("Researcher", researcher_run)
    orch.register("Coder", coder_run)
    orch.register("Reviewer", reviewer_run)

    results = await orch.run(req.task)

    return OrchestrationResponse(
        status="COMPLETE",
        task=req.task,
        agents_used=len(results),
        results=[
            AgentOutput(agent_name=r.agent_name, output=r.output, metadata=r.metadata)
            for r in results
        ],
    )
