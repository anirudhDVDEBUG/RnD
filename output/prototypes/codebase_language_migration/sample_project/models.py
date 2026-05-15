"""Data models for TaskFlow."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
import time
import uuid


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    name: str
    payload: dict[str, Any]
    priority: Priority = Priority.MEDIUM
    status: Status = Status.PENDING
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    created_at: float = field(default_factory=time.time)
    result: Optional[Any] = None
    error: Optional[str] = None

    def is_terminal(self) -> bool:
        return self.status in (Status.COMPLETED, Status.FAILED)

    def elapsed(self) -> float:
        return time.time() - self.created_at
