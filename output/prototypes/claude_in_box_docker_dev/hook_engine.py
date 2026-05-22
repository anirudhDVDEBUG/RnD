"""
hook_engine.py — Hook-driven automation engine for Claude-in-Box simulator.

Mirrors the real claude-in-box hook system: events fire callbacks that can
log, notify, or chain actions when session lifecycle events occur.
"""

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class HookExecution:
    hook_name: str
    event: str
    session_id: str
    timestamp: float
    result: str
    duration_ms: float


@dataclass
class HookRule:
    name: str
    event_pattern: str  # e.g. "session.started", "session.*", "*"
    action: str         # description of what happens
    callback: Optional[Callable] = None


class HookEngine:
    """Event-driven hook engine matching the claude-in-box hook architecture."""

    def __init__(self):
        self._rules: List[HookRule] = []
        self._history: List[HookExecution] = []
        self._install_defaults()

    def _install_defaults(self):
        """Install default hooks that mirror claude-in-box built-ins."""
        self.register(HookRule(
            name="session-logger",
            event_pattern="session.*",
            action="Log session lifecycle event to audit trail",
        ))
        self.register(HookRule(
            name="resource-monitor",
            event_pattern="session.started",
            action="Start resource monitoring for new session",
        ))
        self.register(HookRule(
            name="workspace-init",
            event_pattern="session.created",
            action="Initialize workspace directory and git repo",
        ))
        self.register(HookRule(
            name="cleanup-hook",
            event_pattern="session.stopped",
            action="Archive session output and release resources",
        ))

    def register(self, rule: HookRule):
        self._rules.append(rule)

    def _matches(self, pattern: str, event: str) -> bool:
        if pattern == "*":
            return True
        if pattern.endswith(".*"):
            return event.startswith(pattern[:-2])
        return pattern == event

    def fire(self, event: str, session_id: str, detail: str = "") -> List[HookExecution]:
        results = []
        for rule in self._rules:
            if self._matches(rule.event_pattern, event):
                start = time.time()
                result = f"[{rule.name}] {rule.action}"
                if detail:
                    result += f" | {detail}"
                if rule.callback:
                    try:
                        rule.callback(event, session_id, detail)
                    except Exception as e:
                        result += f" | ERROR: {e}"
                elapsed = (time.time() - start) * 1000
                exe = HookExecution(
                    hook_name=rule.name,
                    event=event,
                    session_id=session_id,
                    timestamp=time.time(),
                    result=result,
                    duration_ms=round(elapsed, 2),
                )
                self._history.append(exe)
                results.append(exe)
        return results

    def get_history(self, limit: int = 20) -> List[dict]:
        return [
            {
                "hook": h.hook_name,
                "event": h.event,
                "session": h.session_id,
                "result": h.result,
                "duration_ms": h.duration_ms,
            }
            for h in self._history[-limit:]
        ]

    def list_rules(self) -> List[dict]:
        return [
            {"name": r.name, "pattern": r.event_pattern, "action": r.action}
            for r in self._rules
        ]
