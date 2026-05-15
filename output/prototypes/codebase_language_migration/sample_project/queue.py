"""Priority queue for tasks."""

from typing import Optional
from .models import Task, Status, Priority


class TaskQueue:
    def __init__(self, max_size: int = 100):
        self._tasks: list[Task] = []
        self._max_size = max_size

    def enqueue(self, task: Task) -> bool:
        if len(self._tasks) >= self._max_size:
            return False
        self._tasks.append(task)
        self._tasks.sort(key=lambda t: t.priority.value, reverse=True)
        return True

    def dequeue(self) -> Optional[Task]:
        for i, task in enumerate(self._tasks):
            if task.status == Status.PENDING:
                task.status = Status.RUNNING
                return task
        return None

    def peek(self) -> Optional[Task]:
        for task in self._tasks:
            if task.status == Status.PENDING:
                return task
        return None

    @property
    def size(self) -> int:
        return len(self._tasks)

    @property
    def pending_count(self) -> int:
        return sum(1 for t in self._tasks if t.status == Status.PENDING)

    def get_by_id(self, task_id: str) -> Optional[Task]:
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def stats(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for task in self._tasks:
            key = task.status.value
            counts[key] = counts.get(key, 0) + 1
        return counts
