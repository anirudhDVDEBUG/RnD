"""JSON-file-based persistence for proposals, memory, skills, and facts."""

import json
import os
from pathlib import Path
from typing import List

from .models import (
    Proposal, ProposalStatus, ProposalType, ProposalAction,
    MemoryEntry, SkillEntry, FactEntry,
)

DEFAULT_DIR = os.environ.get("HERMES_DATA_DIR", ".hermes_data")


def _ensure_dir(data_dir: str = DEFAULT_DIR):
    Path(data_dir).mkdir(parents=True, exist_ok=True)


def _path(name: str, data_dir: str = DEFAULT_DIR) -> Path:
    _ensure_dir(data_dir)
    return Path(data_dir) / name


# --- Proposals ---

def save_proposals(proposals: List[Proposal], data_dir: str = DEFAULT_DIR):
    with open(_path("proposals.json", data_dir), "w") as f:
        json.dump([p.to_dict() for p in proposals], f, indent=2)


def load_proposals(data_dir: str = DEFAULT_DIR) -> List[Proposal]:
    p = _path("proposals.json", data_dir)
    if not p.exists():
        return []
    with open(p) as f:
        return [Proposal.from_dict(d) for d in json.load(f)]


def staged_proposals(data_dir: str = DEFAULT_DIR) -> List[Proposal]:
    return [p for p in load_proposals(data_dir) if p.status == ProposalStatus.STAGED]


# --- Memory ---

def load_memory(data_dir: str = DEFAULT_DIR) -> List[MemoryEntry]:
    p = _path("memory.json", data_dir)
    if not p.exists():
        return []
    with open(p) as f:
        return [MemoryEntry(**d) for d in json.load(f)]


def save_memory(entries: List[MemoryEntry], data_dir: str = DEFAULT_DIR):
    with open(_path("memory.json", data_dir), "w") as f:
        json.dump([e.to_dict() for e in entries], f, indent=2)


# --- Skills ---

def load_skills(data_dir: str = DEFAULT_DIR) -> List[SkillEntry]:
    p = _path("skills.json", data_dir)
    if not p.exists():
        return []
    with open(p) as f:
        return [SkillEntry(**d) for d in json.load(f)]


def save_skills(entries: List[SkillEntry], data_dir: str = DEFAULT_DIR):
    with open(_path("skills.json", data_dir), "w") as f:
        json.dump([e.to_dict() for e in entries], f, indent=2)


# --- Facts ---

def load_facts(data_dir: str = DEFAULT_DIR) -> List[FactEntry]:
    p = _path("facts.json", data_dir)
    if not p.exists():
        return []
    with open(p) as f:
        return [FactEntry(**d) for d in json.load(f)]


def save_facts(entries: List[FactEntry], data_dir: str = DEFAULT_DIR):
    with open(_path("facts.json", data_dir), "w") as f:
        json.dump([e.to_dict() for e in entries], f, indent=2)
