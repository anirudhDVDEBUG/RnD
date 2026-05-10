"""
opensquilla_agent.py — Token-Efficient AI Agent Framework (standalone demo)

Demonstrates core OpenSquilla concepts:
  - Token budget management & prompt compression
  - Skill-based architecture with decorator registration
  - Agent memory (cross-session persistence)
  - MCP server configuration (declarative)
  - Intelligence density metrics

This file is a self-contained simulation that works WITHOUT an API key.
"""

from __future__ import annotations
import json
import hashlib
import os
import textwrap
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# Token estimation (tiktoken-free approximation)
# ---------------------------------------------------------------------------

def estimate_tokens(text: str) -> int:
    """Rough token count: ~4 chars per token for English text."""
    return max(1, len(text) // 4)


# ---------------------------------------------------------------------------
# Prompt compressor — the heart of token efficiency
# ---------------------------------------------------------------------------

class PromptCompressor:
    """Reduces prompt size while preserving semantic content."""

    FILLER_PHRASES = [
        "please ", "could you ", "i would like you to ", "can you ",
        "i want you to ", "it would be great if you ", "kindly ",
    ]

    @staticmethod
    def compress(text: str, budget: int) -> str:
        original_tokens = estimate_tokens(text)
        if original_tokens <= budget:
            return text

        # Phase 1: strip filler
        compressed = text.lower()
        for filler in PromptCompressor.FILLER_PHRASES:
            compressed = compressed.replace(filler, "")

        # Phase 2: collapse whitespace
        compressed = " ".join(compressed.split())

        # Phase 3: truncate to budget if still over
        while estimate_tokens(compressed) > budget and len(compressed) > 10:
            compressed = compressed[: int(len(compressed) * 0.9)]

        return compressed.strip()

    @staticmethod
    def stats(original: str, compressed: str) -> dict:
        orig_tok = estimate_tokens(original)
        comp_tok = estimate_tokens(compressed)
        return {
            "original_tokens": orig_tok,
            "compressed_tokens": comp_tok,
            "savings_pct": round((1 - comp_tok / max(orig_tok, 1)) * 100, 1),
            "intelligence_density": round(comp_tok / max(orig_tok, 1), 3),
        }


# ---------------------------------------------------------------------------
# Skill decorator & registry
# ---------------------------------------------------------------------------

@dataclass
class SkillDef:
    name: str
    description: str
    fn: Callable


_SKILL_REGISTRY: Dict[str, SkillDef] = {}


def Skill(name: str, description: str = ""):
    """Decorator to register a function as an agent skill."""
    def decorator(fn: Callable):
        _SKILL_REGISTRY[name] = SkillDef(name=name, description=description, fn=fn)
        fn._skill_name = name
        return fn
    return decorator


# ---------------------------------------------------------------------------
# MCP configuration (declarative, no runtime dependency)
# ---------------------------------------------------------------------------

@dataclass
class MCPConfig:
    name: str
    command: str
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)

    def to_claude_json(self) -> dict:
        entry = {"command": self.command, "args": self.args}
        if self.env:
            entry["env"] = self.env
        return {self.name: entry}


# ---------------------------------------------------------------------------
# Agent Memory
# ---------------------------------------------------------------------------

class AgentMemory:
    """Simple JSON-file-backed memory for cross-session persistence."""

    def __init__(self, path: str = "./agent_memory"):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)
        self._file = self.path / "memory.json"
        self._data: Dict[str, str] = {}
        self._load()

    def _load(self):
        if self._file.exists():
            self._data = json.loads(self._file.read_text())

    def save(self):
        self._file.write_text(json.dumps(self._data, indent=2))

    def remember(self, key: str, value: str):
        self._data[key] = value
        self.save()

    def recall(self, key: str) -> Optional[str]:
        return self._data.get(key)

    def list_keys(self) -> List[str]:
        return list(self._data.keys())

    def forget(self, key: str):
        self._data.pop(key, None)
        self.save()


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class Agent:
    """Token-efficient AI agent with skills, memory, and MCP support."""

    def __init__(
        self,
        name: str = "agent",
        token_budget: int = 4096,
        mcp_servers: Optional[List[MCPConfig]] = None,
        memory_enabled: bool = False,
        memory_path: str = "./agent_memory",
        skills: Optional[List[Callable]] = None,
    ):
        self.name = name
        self.token_budget = token_budget
        self.mcp_servers = mcp_servers or []
        self.memory = AgentMemory(memory_path) if memory_enabled else None
        self.skills: Dict[str, SkillDef] = {}
        self._history: List[dict] = []

        # Register skills passed explicitly
        if skills:
            for fn in skills:
                skill_name = getattr(fn, "_skill_name", fn.__name__)
                if skill_name in _SKILL_REGISTRY:
                    self.skills[skill_name] = _SKILL_REGISTRY[skill_name]

    # -- Core loop (mock — no real LLM call) --------------------------------

    def run(self, prompt: str) -> str:
        """Process a prompt through the token-efficient pipeline."""
        compressed = PromptCompressor.compress(prompt, self.token_budget)
        stats = PromptCompressor.stats(prompt, compressed)

        # Check if a skill matches
        matched_skill = self._match_skill(compressed)

        # Build context from memory
        context_items = []
        if self.memory:
            for key in self.memory.list_keys():
                context_items.append(f"[memory:{key}] {self.memory.recall(key)}")

        # Simulate response (in real OpenSquilla this calls an LLM)
        if matched_skill:
            result = matched_skill.fn(compressed)
        else:
            result = self._mock_llm(compressed, context_items)

        # Record in history
        self._history.append({
            "prompt": prompt,
            "compressed": compressed,
            "stats": stats,
            "skill": matched_skill.name if matched_skill else None,
            "response": result,
        })

        return result

    def get_last_stats(self) -> Optional[dict]:
        if self._history:
            return self._history[-1]["stats"]
        return None

    def _match_skill(self, text: str) -> Optional[SkillDef]:
        text_lower = text.lower()
        for skill in self.skills.values():
            if skill.name.lower() in text_lower:
                return skill
        return None

    def _mock_llm(self, prompt: str, context: List[str]) -> str:
        ctx_str = "; ".join(context) if context else "none"
        return (
            f"[Agent '{self.name}'] Processed prompt "
            f"({estimate_tokens(prompt)} tokens, budget {self.token_budget}). "
            f"Context: {ctx_str}. "
            f"Mock response for: {prompt[:80]}..."
        )
