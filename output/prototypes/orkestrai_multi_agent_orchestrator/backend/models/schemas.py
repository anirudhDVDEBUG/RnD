"""Pydantic request/response models."""

from pydantic import BaseModel, Field


class OrchestrationRequest(BaseModel):
    task: str = Field(..., description="The high-level task to orchestrate")
    provider: str = Field(default="anthropic", description="LLM provider to use")
    model: str | None = Field(default=None, description="Specific model override")


class AgentOutput(BaseModel):
    agent_name: str
    output: str
    metadata: dict = Field(default_factory=dict)


class OrchestrationResponse(BaseModel):
    status: str
    task: str
    agents_used: int
    results: list[AgentOutput]
