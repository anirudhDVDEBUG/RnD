"""Dispatcher: routes tasks to agents and manages the agent registry."""

from __future__ import annotations

from typing import Any

from agents.base import Agent, AgentState


class Dispatcher:
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    # -- registry -----------------------------------------------------------

    def register(self, agent: Agent) -> None:
        agent.start()
        self._agents[agent.name] = agent

    def unregister(self, name: str) -> None:
        if name in self._agents:
            self._agents[name].stop()
            del self._agents[name]

    def get(self, name: str) -> Agent | None:
        return self._agents.get(name)

    def list_agents(self) -> list[dict[str, Any]]:
        return [a.status() for a in self._agents.values()]

    # -- dispatch -----------------------------------------------------------

    def dispatch(self, task_type: str, payload: str = "") -> dict[str, Any]:
        """Find the best agent for *task_type* and execute."""
        agent = self._resolve(task_type)
        if agent is None:
            return {"error": f"No agent registered for task type '{task_type}'"}
        task = {"type": task_type, "payload": payload}
        try:
            result = agent.run(task)
            return {"agent": agent.name, "result": result}
        except Exception as exc:
            # attempt rebuild + single retry
            agent.rebuild()
            try:
                result = agent.run(task)
                return {"agent": agent.name, "result": result, "retried": True}
            except Exception:
                return {"agent": agent.name, "error": str(exc)}

    def rebuild_agent(self, name: str) -> str:
        agent = self._agents.get(name)
        if agent is None:
            return f"Agent '{name}' not found"
        agent.rebuild()
        return f"Agent '{name}' rebuilt → {agent.state.value}"

    # -- internal -----------------------------------------------------------

    def _resolve(self, task_type: str) -> Agent | None:
        for agent in self._agents.values():
            if task_type in agent.task_types:
                return agent
        # fallback: match by agent name
        return self._agents.get(task_type)
