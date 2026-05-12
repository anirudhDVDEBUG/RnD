"""Persistent memory with keyword-based retrieval."""
import json
import time
from pathlib import Path


class MemoryManager:
    def __init__(self, memory_file: str):
        self.memory_file = Path(memory_file)
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
        self.memories = self._load()
        self.session_memories = []  # short-term

    def _load(self) -> list:
        if self.memory_file.exists():
            try:
                return json.loads(self.memory_file.read_text())
            except json.JSONDecodeError:
                return []
        return []

    def store(self, query: str, response: str):
        entry = {
            "query": query,
            "response": response,
            "timestamp": time.time(),
        }
        self.memories.append(entry)
        self.session_memories.append(entry)
        self._save()

    def _save(self):
        self.memory_file.write_text(json.dumps(self.memories, indent=2))

    def get_relevant_context(self, query: str, k: int = 5) -> str:
        if not self.memories:
            return "(no prior context)"
        query_words = set(query.lower().split())
        scored = []
        for m in self.memories:
            overlap = len(query_words & set(m["query"].lower().split()))
            scored.append((overlap, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = [m for _, m in scored[:k] if _ > 0]
        if not top:
            return "(no relevant context)"
        return "\n".join(
            f"  Q: {m['query']}\n  A: {m['response']}" for m in top
        )

    def get_stats(self) -> dict:
        return {
            "total_memories": len(self.memories),
            "session_memories": len(self.session_memories),
            "file": str(self.memory_file),
        }
