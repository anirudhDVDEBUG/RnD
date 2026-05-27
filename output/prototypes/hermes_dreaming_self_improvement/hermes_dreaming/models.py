"""Data models for proposals, memory entries, skills, and facts."""

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional


class ProposalType(Enum):
    MEMORY_UPDATE = "memory_update"
    SKILL_UPDATE = "skill_update"
    FACT_UPDATE = "fact_update"


class ProposalAction(Enum):
    ADD = "add"
    MERGE = "merge"
    PRUNE = "prune"
    CORRECT = "correct"
    REFINE = "refine"


class ProposalStatus(Enum):
    STAGED = "staged"
    APPROVED = "approved"
    DISCARDED = "discarded"
    APPLIED = "applied"


@dataclass
class Proposal:
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    type: ProposalType = ProposalType.MEMORY_UPDATE
    action: ProposalAction = ProposalAction.ADD
    status: ProposalStatus = ProposalStatus.STAGED
    title: str = ""
    description: str = ""
    before: Optional[str] = None
    after: str = ""
    confidence: float = 0.0
    reason: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        d = asdict(self)
        d["type"] = self.type.value
        d["action"] = self.action.value
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, d):
        d = dict(d)
        d["type"] = ProposalType(d["type"])
        d["action"] = ProposalAction(d["action"])
        d["status"] = ProposalStatus(d["status"])
        return cls(**d)

    def summary_line(self):
        icon = {
            ProposalAction.ADD: "+",
            ProposalAction.MERGE: "~",
            ProposalAction.PRUNE: "-",
            ProposalAction.CORRECT: "!",
            ProposalAction.REFINE: "^",
        }[self.action]
        return f"[{icon}] {self.id}  {self.type.value:<15} {self.title}  (conf: {self.confidence:.0%})"


@dataclass
class MemoryEntry:
    key: str
    value: str
    source: str = "user"
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)


@dataclass
class SkillEntry:
    name: str
    description: str
    trigger_phrases: list = field(default_factory=list)
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)


@dataclass
class FactEntry:
    key: str
    value: str
    confidence: float = 1.0
    source: str = "observed"
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)
