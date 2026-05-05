"""Self-written skill system: agents detect repeated patterns and codify them as reusable skills."""

import json
import os
import time
from dataclasses import dataclass, field


@dataclass
class Skill:
    name: str
    description: str
    action_sequence: list[str]
    times_used: int = 0
    created_at: float = field(default_factory=time.time)

    def execute(self, context: dict | None = None) -> str:
        """Simulate skill execution by replaying action sequence."""
        results = []
        for i, action in enumerate(self.action_sequence):
            results.append(f"  Step {i+1}: {action} [OK]")
        self.times_used += 1
        return "\n".join(results)


class SkillRegistry:
    """Manages learned skills - stores, retrieves, and auto-extracts from action history."""

    def __init__(self, skill_dir: str = "./skills"):
        self.skill_dir = skill_dir
        os.makedirs(skill_dir, exist_ok=True)
        self._skills: dict[str, Skill] = {}
        self._action_history: list[list[str]] = []
        self._load_skills()

    def _load_skills(self):
        """Load existing skills from disk."""
        for fname in os.listdir(self.skill_dir):
            if fname.endswith(".json"):
                path = os.path.join(self.skill_dir, fname)
                with open(path) as f:
                    data = json.load(f)
                skill = Skill(
                    name=data["name"],
                    description=data["description"],
                    action_sequence=data["action_sequence"],
                    times_used=data.get("times_used", 0),
                    created_at=data.get("created_at", time.time()),
                )
                self._skills[skill.name] = skill

    def register_skill(self, name: str, description: str, action_sequence: list[str]) -> Skill:
        """Manually register a new skill."""
        skill = Skill(name=name, description=description, action_sequence=action_sequence)
        self._skills[name] = skill
        self._save_skill(skill)
        return skill

    def _save_skill(self, skill: Skill):
        path = os.path.join(self.skill_dir, f"{skill.name}.json")
        with open(path, "w") as f:
            json.dump({
                "name": skill.name,
                "description": skill.description,
                "action_sequence": skill.action_sequence,
                "times_used": skill.times_used,
                "created_at": skill.created_at,
            }, f, indent=2)

    def record_action_sequence(self, actions: list[str], success: bool = True):
        """Record a completed action sequence. If pattern repeats, auto-extract skill."""
        if success:
            self._action_history.append(actions)
            self._try_extract_skill(actions)

    def _try_extract_skill(self, actions: list[str]):
        """Detect repeated patterns and auto-generate skills."""
        # Look for identical sequences appearing 2+ times
        action_key = "|".join(actions)
        count = sum(1 for h in self._action_history if "|".join(h) == action_key)
        if count >= 2:
            skill_name = "_".join(actions[0].lower().split()[:3]) + "_auto"
            if skill_name not in self._skills:
                skill = self.register_skill(
                    name=skill_name,
                    description=f"Auto-extracted skill from repeated pattern ({count} occurrences)",
                    action_sequence=actions,
                )
                return skill

    def list_skills(self) -> list[str]:
        return list(self._skills.keys())

    def get_skill(self, name: str) -> Skill | None:
        return self._skills.get(name)

    def execute_skill(self, name: str, context: dict | None = None) -> str | None:
        skill = self._skills.get(name)
        if skill:
            result = skill.execute(context)
            self._save_skill(skill)  # persist usage count
            return result
        return None
