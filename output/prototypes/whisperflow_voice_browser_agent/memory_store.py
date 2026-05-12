"""Adaptive memory store for self-healing navigation."""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class MemoryEntry:
    url_pattern: str
    selector: str
    success_count: int = 0
    fail_count: int = 0
    alt_selectors: list[str] = field(default_factory=list)


class MemoryStore:
    """Tracks which selectors work on which sites and suggests alternatives."""

    def __init__(self, path: str = "memory.json"):
        self.path = Path(path)
        self.entries: dict[str, MemoryEntry] = {}
        if self.path.exists():
            self._load()

    def _load(self):
        data = json.loads(self.path.read_text())
        for key, val in data.items():
            self.entries[key] = MemoryEntry(**val)

    def save(self):
        data = {k: asdict(v) for k, v in self.entries.items()}
        self.path.write_text(json.dumps(data, indent=2))

    def _key(self, url: str, selector: str) -> str:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        return f"{domain}::{selector}"

    def record_success(self, url: str, selector: str):
        key = self._key(url, selector)
        entry = self.entries.setdefault(key, MemoryEntry(url_pattern=url, selector=selector))
        entry.success_count += 1
        self.save()

    def record_failure(self, url: str, selector: str):
        key = self._key(url, selector)
        entry = self.entries.setdefault(key, MemoryEntry(url_pattern=url, selector=selector))
        entry.fail_count += 1
        self.save()

    def suggest_alternative(self, url: str, selector: str) -> str | None:
        key = self._key(url, selector)
        entry = self.entries.get(key)
        if entry and entry.alt_selectors:
            return entry.alt_selectors[0]
        return None

    def add_alternative(self, url: str, selector: str, alt: str):
        key = self._key(url, selector)
        entry = self.entries.setdefault(key, MemoryEntry(url_pattern=url, selector=selector))
        if alt not in entry.alt_selectors:
            entry.alt_selectors.append(alt)
        self.save()

    def stats(self) -> dict:
        total = len(self.entries)
        successes = sum(e.success_count for e in self.entries.values())
        failures = sum(e.fail_count for e in self.entries.values())
        return {"entries": total, "successes": successes, "failures": failures}
