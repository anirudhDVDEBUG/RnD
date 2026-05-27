"""Core dreaming engine: analyzes interaction logs and proposes self-improvement updates."""

from typing import List, Optional

from .models import (
    Proposal, ProposalType, ProposalAction, ProposalStatus,
    MemoryEntry, SkillEntry, FactEntry,
)
from . import store


def dream(interaction_log: Optional[List[dict]] = None, data_dir: str = store.DEFAULT_DIR) -> List[Proposal]:
    """Analyze interactions and generate staged proposals.

    In production this would call an LLM to analyze patterns.
    This implementation uses rule-based heuristics on the interaction log
    to demonstrate the staged proposal pipeline.
    """
    if interaction_log is None:
        interaction_log = _default_interaction_log()

    proposals: List[Proposal] = []
    existing_memory = {m.key for m in store.load_memory(data_dir)}
    existing_skills = {s.name for s in store.load_skills(data_dir)}
    existing_facts = {f.key for f in store.load_facts(data_dir)}

    # Analyze interaction patterns
    topic_counts: dict[str, int] = {}
    tool_counts: dict[str, int] = {}
    corrections: list[dict] = []

    for entry in interaction_log:
        # Count topic mentions
        for topic in entry.get("topics", []):
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        # Count tool/skill usage
        for tool in entry.get("tools_used", []):
            tool_counts[tool] = tool_counts.get(tool, 0) + 1

        # Track corrections
        if entry.get("correction"):
            corrections.append(entry)

    # Propose memory updates for frequently discussed topics
    for topic, count in topic_counts.items():
        if count >= 2:
            key = f"user_interest_{topic.lower().replace(' ', '_')}"
            if key not in existing_memory:
                proposals.append(Proposal(
                    type=ProposalType.MEMORY_UPDATE,
                    action=ProposalAction.ADD,
                    title=f"Remember user interest: {topic}",
                    description=f"User discussed '{topic}' in {count} interactions. "
                                f"Storing as a known interest for better context.",
                    after=f"{key} = frequently discussed topic ({count} mentions)",
                    confidence=min(0.5 + count * 0.1, 0.95),
                    reason=f"Observed {count} mentions across interactions",
                ))

    # Propose skill updates for frequently used tools
    for tool, count in tool_counts.items():
        if count >= 2 and tool not in existing_skills:
            proposals.append(Proposal(
                type=ProposalType.SKILL_UPDATE,
                action=ProposalAction.ADD,
                title=f"Add skill: {tool}",
                description=f"Tool '{tool}' was used {count} times. "
                            f"Proposing to register it as a known skill.",
                after=f"Skill: {tool} (usage count: {count})",
                confidence=min(0.4 + count * 0.15, 0.9),
                reason=f"Used {count} times in recent interactions",
            ))

    # Propose fact corrections
    for entry in corrections:
        old_val = entry.get("old_value", "unknown")
        new_val = entry["correction"]
        fact_key = entry.get("fact_key", entry.get("topics", ["unknown"])[0])
        if fact_key not in existing_facts:
            proposals.append(Proposal(
                type=ProposalType.FACT_UPDATE,
                action=ProposalAction.CORRECT,
                title=f"Correct fact: {fact_key}",
                description=f"A correction was observed: '{old_val}' -> '{new_val}'.",
                before=old_val,
                after=new_val,
                confidence=0.85,
                reason="Explicit user correction observed",
            ))

    # Propose pruning stale memories
    memory = store.load_memory(data_dir)
    active_topics = set(topic_counts.keys())
    for mem in memory:
        topic_part = mem.key.replace("user_interest_", "").replace("_", " ")
        if topic_part not in {t.lower() for t in active_topics} and mem.source == "dreaming":
            proposals.append(Proposal(
                type=ProposalType.MEMORY_UPDATE,
                action=ProposalAction.PRUNE,
                title=f"Prune stale memory: {mem.key}",
                description=f"Memory '{mem.key}' was added by a previous dreaming cycle "
                            f"but the topic is no longer active.",
                before=mem.value,
                after="(removed)",
                confidence=0.6,
                reason="Topic not observed in recent interactions",
            ))

    # Save proposals
    all_proposals = store.load_proposals(data_dir) + proposals
    store.save_proposals(all_proposals, data_dir)

    return proposals


def review(data_dir: str = store.DEFAULT_DIR) -> List[Proposal]:
    """Return all staged proposals for review."""
    return store.staged_proposals(data_dir)


def approve(proposal_ids: List[str], data_dir: str = store.DEFAULT_DIR) -> int:
    """Mark proposals as approved."""
    proposals = store.load_proposals(data_dir)
    count = 0
    for p in proposals:
        if p.id in proposal_ids and p.status == ProposalStatus.STAGED:
            p.status = ProposalStatus.APPROVED
            count += 1
    store.save_proposals(proposals, data_dir)
    return count


def discard(proposal_ids: List[str], data_dir: str = store.DEFAULT_DIR) -> int:
    """Mark proposals as discarded."""
    proposals = store.load_proposals(data_dir)
    count = 0
    for p in proposals:
        if p.id in proposal_ids and p.status == ProposalStatus.STAGED:
            p.status = ProposalStatus.DISCARDED
            count += 1
    store.save_proposals(proposals, data_dir)
    return count


def apply(data_dir: str = store.DEFAULT_DIR) -> int:
    """Apply all approved proposals to memory/skills/facts."""
    proposals = store.load_proposals(data_dir)
    memory = store.load_memory(data_dir)
    skills = store.load_skills(data_dir)
    facts = store.load_facts(data_dir)

    applied = 0
    for p in proposals:
        if p.status != ProposalStatus.APPROVED:
            continue

        if p.type == ProposalType.MEMORY_UPDATE:
            if p.action == ProposalAction.PRUNE:
                memory = [m for m in memory if m.key not in p.before]
            else:
                key = p.title.split(": ", 1)[-1].lower().replace(" ", "_")
                memory.append(MemoryEntry(key=key, value=p.after, source="dreaming"))
        elif p.type == ProposalType.SKILL_UPDATE:
            name = p.title.split(": ", 1)[-1]
            skills.append(SkillEntry(name=name, description=p.description))
        elif p.type == ProposalType.FACT_UPDATE:
            key = p.title.split(": ", 1)[-1]
            # Remove old fact if correcting
            facts = [f for f in facts if f.key != key]
            facts.append(FactEntry(key=key, value=p.after, source="dreaming"))

        p.status = ProposalStatus.APPLIED
        applied += 1

    store.save_proposals(proposals, data_dir)
    store.save_memory(memory, data_dir)
    store.save_skills(skills, data_dir)
    store.save_facts(facts, data_dir)

    return applied


def _default_interaction_log() -> List[dict]:
    """Mock interaction log for demo purposes."""
    return [
        {
            "session": "s1",
            "topics": ["Python", "Testing", "CI/CD"],
            "tools_used": ["pytest", "git"],
            "summary": "User set up pytest for a new project with CI pipeline.",
        },
        {
            "session": "s2",
            "topics": ["Python", "Docker", "Testing"],
            "tools_used": ["pytest", "docker-compose"],
            "summary": "User containerized test suite and debugged port conflicts.",
        },
        {
            "session": "s3",
            "topics": ["Python", "API Design"],
            "tools_used": ["FastAPI", "pytest", "httpx"],
            "summary": "User built a REST API with integration tests.",
        },
        {
            "session": "s4",
            "topics": ["Docker", "Deployment"],
            "tools_used": ["docker-compose", "git"],
            "summary": "User deployed multi-container app to staging.",
            "correction": "Default port is 8080, not 3000",
            "old_value": "Default app port: 3000",
            "fact_key": "default_app_port",
        },
        {
            "session": "s5",
            "topics": ["CI/CD", "GitHub Actions"],
            "tools_used": ["git", "pytest"],
            "summary": "User configured GitHub Actions for automated testing.",
        },
    ]
