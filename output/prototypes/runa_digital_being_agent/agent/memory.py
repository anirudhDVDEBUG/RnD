"""Persistent memory system for the digital being."""
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


class PersistentMemory:
    """File-backed memory that persists across agent sessions."""

    def __init__(self, storage_path: str = "logs/memory.json"):
        self.storage_path = storage_path
        self.memories: List[Dict[str, Any]] = []
        self.context_window: List[Dict[str, str]] = []
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                data = json.load(f)
                self.memories = data.get("memories", [])
        else:
            self.memories = []

    def save(self):
        os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({"memories": self.memories}, f, indent=2)

    def store(self, content: str, category: str = "observation", importance: int = 5):
        """Store a new memory with timestamp and metadata."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "category": category,
            "importance": importance,
        }
        self.memories.append(entry)
        self.save()
        return entry

    def recall(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Retrieve relevant memories (simple keyword match for demo)."""
        query_lower = query.lower()
        scored = []
        for mem in self.memories:
            content_lower = mem["content"].lower()
            score = sum(1 for word in query_lower.split() if word in content_lower)
            if score > 0:
                scored.append((score + mem.get("importance", 5), mem))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:limit]]

    def add_to_context(self, role: str, content: str):
        """Add a message to the current conversation context."""
        self.context_window.append({"role": role, "content": content})

    def get_context(self, max_messages: int = 20) -> List[Dict[str, str]]:
        return self.context_window[-max_messages:]

    def summary(self) -> str:
        return f"Memory bank: {len(self.memories)} entries stored."
