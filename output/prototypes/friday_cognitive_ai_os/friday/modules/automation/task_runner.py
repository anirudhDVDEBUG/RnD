"""Simple task runner for scheduled/triggered actions."""
import time


class TaskRunner:
    def __init__(self):
        self.tasks = []
        self.history = []

    def add_task(self, name: str, fn, args=None):
        self.tasks.append({"name": name, "fn": fn, "args": args or []})

    def run_all(self) -> list:
        results = []
        for task in self.tasks:
            start = time.time()
            try:
                result = task["fn"](*task["args"])
                elapsed = time.time() - start
                entry = {"task": task["name"], "status": "ok", "result": result, "elapsed": round(elapsed, 3)}
            except Exception as e:
                elapsed = time.time() - start
                entry = {"task": task["name"], "status": "error", "error": str(e), "elapsed": round(elapsed, 3)}
            results.append(entry)
            self.history.append(entry)
        self.tasks.clear()
        return results
