"""
session_manager.py — Multi-session manager for Claude-in-Box simulator.

Manages isolated Claude Code sessions with lifecycle, workspace isolation,
resource tracking, and event hooks.
"""

import uuid
import time
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable
from enum import Enum


class SessionState(Enum):
    CREATED = "created"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class Session:
    id: str
    name: str
    workspace: str
    state: SessionState = SessionState.CREATED
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    pid: Optional[int] = None
    memory_mb: float = 0.0
    cpu_pct: float = 0.0
    output_lines: List[str] = field(default_factory=list)
    hooks: Dict[str, List[str]] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "workspace": self.workspace,
            "state": self.state.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "uptime_s": (time.time() - self.started_at) if self.started_at else 0,
            "memory_mb": round(self.memory_mb, 1),
            "cpu_pct": round(self.cpu_pct, 1),
            "output_line_count": len(self.output_lines),
            "hooks": {k: len(v) for k, v in self.hooks.items()},
        }


class SessionManager:
    """Manages multiple Claude Code sessions with isolated workspaces."""

    def __init__(self, on_event: Optional[Callable] = None):
        self._sessions: Dict[str, Session] = {}
        self._lock = threading.Lock()
        self._on_event = on_event

    def _emit(self, event: str, session: Session, detail: str = ""):
        if self._on_event:
            self._on_event(event, session, detail)

    def create_session(self, name: str, workspace: str = "/workspace") -> Session:
        sid = uuid.uuid4().hex[:12]
        ws = f"{workspace}/{name}_{sid[:6]}"
        session = Session(id=sid, name=name, workspace=ws)
        with self._lock:
            self._sessions[sid] = session
        self._emit("session.created", session)
        return session

    def start_session(self, sid: str) -> Session:
        with self._lock:
            s = self._sessions[sid]
            s.state = SessionState.RUNNING
            s.started_at = time.time()
            s.pid = 1000 + len(self._sessions)
            s.memory_mb = 45.0 + (hash(sid) % 30)
            s.cpu_pct = 2.0 + (hash(sid) % 8)
        self._emit("session.started", s)
        return s

    def stop_session(self, sid: str) -> Session:
        with self._lock:
            s = self._sessions[sid]
            s.state = SessionState.STOPPED
        self._emit("session.stopped", s)
        return s

    def append_output(self, sid: str, line: str):
        with self._lock:
            self._sessions[sid].output_lines.append(line)

    def get_session(self, sid: str) -> Optional[Session]:
        return self._sessions.get(sid)

    def list_sessions(self) -> List[Session]:
        return list(self._sessions.values())

    def add_hook(self, sid: str, event: str, command: str):
        with self._lock:
            s = self._sessions[sid]
            s.hooks.setdefault(event, []).append(command)
        self._emit("hook.added", s, f"{event} -> {command}")

    def get_stats(self) -> dict:
        sessions = self.list_sessions()
        running = [s for s in sessions if s.state == SessionState.RUNNING]
        return {
            "total_sessions": len(sessions),
            "running": len(running),
            "stopped": len(sessions) - len(running),
            "total_memory_mb": round(sum(s.memory_mb for s in running), 1),
            "total_cpu_pct": round(sum(s.cpu_pct for s in running), 1),
        }
