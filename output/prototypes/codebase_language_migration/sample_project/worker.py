"""Worker that processes tasks from the queue."""

from typing import Callable, Any
from .models import Task, Status
from .queue import TaskQueue


HandlerFn = Callable[[dict[str, Any]], Any]


class Worker:
    def __init__(self, queue: TaskQueue, handlers: dict[str, HandlerFn] | None = None):
        self.queue = queue
        self._handlers: dict[str, HandlerFn] = handlers or {}
        self._processed = 0

    def register(self, task_name: str, handler: HandlerFn) -> None:
        self._handlers[task_name] = handler

    def process_one(self) -> bool:
        task = self.queue.dequeue()
        if task is None:
            return False
        self._execute(task)
        return True

    def process_all(self) -> int:
        count = 0
        while self.process_one():
            count += 1
        return count

    def _execute(self, task: Task) -> None:
        handler = self._handlers.get(task.name)
        if handler is None:
            task.status = Status.FAILED
            task.error = f"No handler registered for '{task.name}'"
            return
        try:
            task.result = handler(task.payload)
            task.status = Status.COMPLETED
            self._processed += 1
        except Exception as exc:
            task.status = Status.FAILED
            task.error = str(exc)

    @property
    def processed_count(self) -> int:
        return self._processed
