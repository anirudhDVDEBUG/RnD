"""Layered memory system: working, episodic, and semantic tiers."""

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryEntry:
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)
    vision_anchor: str | None = None  # path to screenshot that grounded this memory


class WorkingMemory:
    """Short-term buffer of recent context (sliding window)."""

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self._buffer: list[MemoryEntry] = []

    def add(self, entry: MemoryEntry):
        self._buffer.append(entry)
        if len(self._buffer) > self.capacity:
            self._buffer.pop(0)

    @property
    def entries(self) -> list[MemoryEntry]:
        return list(self._buffer)

    def __len__(self):
        return len(self._buffer)


class EpisodicMemory:
    """Long-term store of past interaction episodes."""

    def __init__(self, store_path: str = "./memory/episodes"):
        self.store_path = store_path
        os.makedirs(store_path, exist_ok=True)
        self._episodes: list[dict] = []

    def record_episode(self, actions: list[str], outcome: str, vision_frames: list[str] | None = None):
        episode = {
            "actions": actions,
            "outcome": outcome,
            "vision_frames": vision_frames or [],
            "timestamp": time.time(),
        }
        self._episodes.append(episode)
        ep_file = os.path.join(self.store_path, f"episode_{len(self._episodes):04d}.json")
        with open(ep_file, "w") as f:
            json.dump(episode, f, indent=2)
        return episode

    def recall(self, query: str, top_k: int = 3) -> list[dict]:
        """Simple keyword recall (production would use embeddings)."""
        scored = []
        for ep in self._episodes:
            score = sum(1 for a in ep["actions"] if query.lower() in a.lower())
            if query.lower() in ep["outcome"].lower():
                score += 2
            if score > 0:
                scored.append((score, ep))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored[:top_k]]

    @property
    def count(self) -> int:
        return len(self._episodes)


class SemanticMemory:
    """Persistent knowledge store (facts, learned patterns)."""

    def __init__(self, store_path: str = "./memory/knowledge"):
        self.store_path = store_path
        os.makedirs(store_path, exist_ok=True)
        self._facts: dict[str, Any] = {}
        self._load()

    def _load(self):
        facts_file = os.path.join(self.store_path, "facts.json")
        if os.path.exists(facts_file):
            with open(facts_file) as f:
                self._facts = json.load(f)

    def store(self, key: str, value: Any):
        self._facts[key] = {"value": value, "timestamp": time.time()}
        self._save()

    def retrieve(self, key: str) -> Any | None:
        entry = self._facts.get(key)
        return entry["value"] if entry else None

    def _save(self):
        facts_file = os.path.join(self.store_path, "facts.json")
        with open(facts_file, "w") as f:
            json.dump(self._facts, f, indent=2)

    @property
    def count(self) -> int:
        return len(self._facts)


class MemoryLayer:
    """Unified interface to the three-tier memory system."""

    def __init__(
        self,
        working_memory_size: int = 10,
        episodic_store: str = "./memory/episodes",
        semantic_store: str = "./memory/knowledge",
    ):
        self.working = WorkingMemory(capacity=working_memory_size)
        self.episodic = EpisodicMemory(store_path=episodic_store)
        self.semantic = SemanticMemory(store_path=semantic_store)

    def remember(self, content: str, vision_anchor: str | None = None):
        """Add to working memory with optional vision grounding."""
        entry = MemoryEntry(content=content, vision_anchor=vision_anchor)
        self.working.add(entry)

    def summarize(self) -> dict:
        return {
            "working_memory_items": len(self.working),
            "episodic_memory_episodes": self.episodic.count,
            "semantic_memory_facts": self.semantic.count,
        }
