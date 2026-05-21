"""Skill system — modular capabilities the agent can discover and invoke."""

from dataclasses import dataclass, field


@dataclass
class Skill:
    name: str
    description: str
    triggers: list[str] = field(default_factory=list)

    def matches(self, query: str) -> bool:
        q = query.lower()
        return any(t in q for t in self.triggers)

    def execute(self, query: str, context: str = "") -> dict:
        return {
            "skill": self.name,
            "input": query,
            "output": f"[{self.name}] Processed: {query[:80]}",
        }


# Built-in skills
BUILTIN_SKILLS = [
    Skill("summarizer", "Summarize text or documents", ["summarize", "summary", "tldr"]),
    Skill("code_reviewer", "Review code for quality", ["review", "code review", "lint"]),
    Skill("researcher", "Research a topic using RAG", ["research", "find", "look up"]),
    Skill("writer", "Draft content from a prompt", ["write", "draft", "compose"]),
]


class SkillRegistry:
    def __init__(self):
        self.skills: list[Skill] = list(BUILTIN_SKILLS)

    def register(self, skill: Skill) -> None:
        self.skills.append(skill)

    def match(self, query: str) -> Skill | None:
        for s in self.skills:
            if s.matches(query):
                return s
        return None

    def list_skills(self) -> list[dict]:
        return [{"name": s.name, "description": s.description, "triggers": s.triggers} for s in self.skills]
