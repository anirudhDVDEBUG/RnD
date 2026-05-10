"""
Cron scheduler for recurring agent tasks — mirrors /loop semantics.

Supports standard cron expressions (e.g. "*/5 * * * *") and simple
interval strings (e.g. "5m", "1h").
"""

import re
import sched
import time
import threading
from datetime import datetime
from typing import Callable, Optional


def parse_interval(spec: str) -> int:
    """Parse an interval string like '5m', '1h', '30s' into seconds."""
    match = re.match(r"^(\d+)\s*(s|sec|m|min|h|hr|hour)s?$", spec.strip(), re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid interval: {spec!r}. Use e.g. '5m', '1h', '30s'.")
    value = int(match.group(1))
    unit = match.group(2).lower()
    multipliers = {"s": 1, "sec": 1, "m": 60, "min": 60, "h": 3600, "hr": 3600, "hour": 3600}
    return value * multipliers[unit]


def cron_matches_now(cron_expr: str) -> bool:
    """
    Check if a 5-field cron expression matches the current minute.
    Fields: minute hour day_of_month month day_of_week
    Supports: * (any), */N (every N), N (exact), N-M (range).
    """
    fields = cron_expr.strip().split()
    if len(fields) != 5:
        raise ValueError(f"Cron expression must have 5 fields, got {len(fields)}: {cron_expr}")

    now = datetime.now()
    values = [now.minute, now.hour, now.day, now.month, now.weekday()]  # weekday: 0=Mon

    for field_str, current in zip(fields, values):
        if field_str == "*":
            continue
        if field_str.startswith("*/"):
            step = int(field_str[2:])
            if current % step != 0:
                return False
        elif "-" in field_str:
            lo, hi = field_str.split("-", 1)
            if not (int(lo) <= current <= int(hi)):
                return False
        elif "," in field_str:
            allowed = {int(x) for x in field_str.split(",")}
            if current not in allowed:
                return False
        else:
            if current != int(field_str):
                return False
    return True


class CronScheduler:
    """
    Schedule agent tasks using cron expressions or simple intervals.

    Usage:
        scheduler = CronScheduler()
        scheduler.add_interval("5m", lambda: agent.run("check status"))
        scheduler.add_cron("0 9 * * 1-5", lambda: agent.run("morning report"))
        scheduler.start()  # blocks, or use start_background()
    """

    def __init__(self):
        self.tasks: list[dict] = []
        self._running = False
        self._thread: Optional[threading.Thread] = None

    def add_interval(self, interval: str, callback: Callable, name: str = ""):
        """Add a task that runs at a fixed interval (e.g. '5m')."""
        seconds = parse_interval(interval)
        self.tasks.append({
            "type": "interval",
            "seconds": seconds,
            "callback": callback,
            "name": name or f"every-{interval}",
            "last_run": 0.0,
        })

    def add_cron(self, cron_expr: str, callback: Callable, name: str = ""):
        """Add a task that runs on a cron schedule."""
        self.tasks.append({
            "type": "cron",
            "expr": cron_expr,
            "callback": callback,
            "name": name or f"cron({cron_expr})",
            "last_run": 0.0,
        })

    def tick(self):
        """Check all tasks and run those that are due. Call once per ~30s."""
        now = time.time()
        for task in self.tasks:
            if task["type"] == "interval":
                if now - task["last_run"] >= task["seconds"]:
                    task["last_run"] = now
                    print(f"[cron] Running: {task['name']}")
                    task["callback"]()
            elif task["type"] == "cron":
                if cron_matches_now(task["expr"]) and now - task["last_run"] >= 60:
                    task["last_run"] = now
                    print(f"[cron] Running: {task['name']}")
                    task["callback"]()

    def run_loop(self, poll_interval: float = 30.0, max_iterations: int = 0):
        """Run the scheduler loop. If max_iterations > 0, stop after that many ticks."""
        self._running = True
        iteration = 0
        while self._running:
            self.tick()
            iteration += 1
            if max_iterations and iteration >= max_iterations:
                break
            time.sleep(poll_interval)

    def start_background(self):
        """Start the scheduler in a background thread."""
        self._thread = threading.Thread(target=self.run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False


# ---------------------------------------------------------------------------
# Demo: show the scheduler running a few ticks
# ---------------------------------------------------------------------------
def demo_scheduler():
    """Demonstrate the cron scheduler with a fast-ticking mock."""
    print("=== Cron Scheduler Demo ===\n")

    counter = {"n": 0}

    def mock_task():
        counter["n"] += 1
        print(f"    Task executed (run #{counter['n']})")

    scheduler = CronScheduler()
    scheduler.add_interval("1s", mock_task, name="heartbeat")

    print("Running scheduler for 3 ticks (1-second interval)...\n")
    scheduler.run_loop(poll_interval=1.0, max_iterations=3)
    print(f"\nTotal executions: {counter['n']}")


if __name__ == "__main__":
    demo_scheduler()
