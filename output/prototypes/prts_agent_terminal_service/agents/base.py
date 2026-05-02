"""Base agent class with lifecycle management (start/stop/rebuild)."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class AgentState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    REBUILDING = "rebuilding"
    STOPPED = "stopped"


class Agent(ABC):
    """Abstract base for all PRTS agents. Subclass and implement execute()."""

    name: str = "unnamed"
    description: str = ""
    task_types: list[str] = []

    def __init__(self) -> None:
        self.state = AgentState.IDLE
        self._start_time: float | None = None
        self._last_result: Any = None
        self._error: str | None = None
        self._execution_count = 0

    # -- lifecycle ----------------------------------------------------------

    def start(self) -> None:
        self.state = AgentState.IDLE
        self._start_time = time.time()
        self._error = None

    def stop(self) -> None:
        self.state = AgentState.STOPPED

    def rebuild(self) -> None:
        """Hot-restart: reset internal state without losing registry entry."""
        self.state = AgentState.REBUILDING
        self._error = None
        self._last_result = None
        self._execution_count = 0
        self.state = AgentState.IDLE

    # -- execution ----------------------------------------------------------

    def run(self, task: dict[str, Any]) -> Any:
        self.state = AgentState.RUNNING
        self._start_time = time.time()
        try:
            result = self.execute(task)
            self._last_result = result
            self._execution_count += 1
            self.state = AgentState.COMPLETED
            return result
        except Exception as exc:
            self._error = str(exc)
            self.state = AgentState.FAILED
            raise

    @abstractmethod
    def execute(self, task: dict[str, Any]) -> Any:
        ...

    # -- introspection ------------------------------------------------------

    def status(self) -> dict[str, Any]:
        uptime = None
        if self._start_time:
            uptime = round(time.time() - self._start_time, 2)
        return {
            "name": self.name,
            "state": self.state.value,
            "uptime_s": uptime,
            "executions": self._execution_count,
            "last_error": self._error,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r} state={self.state.value}>"
