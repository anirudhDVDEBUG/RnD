"""Skill registry for discovering and managing available skills."""

from skills.base import BaseSkill


class SkillRegistry:
    """Central registry for discovering, registering, and invoking skills."""

    def __init__(self):
        self._skills: dict[str, type[BaseSkill]] = {}

    def register(self, skill_class: type[BaseSkill]) -> type[BaseSkill]:
        """Register a skill class. Can be used as a decorator."""
        self._skills[skill_class.name] = skill_class
        return skill_class

    def get(self, name: str) -> type[BaseSkill] | None:
        return self._skills.get(name)

    def list_skills(self) -> list[dict]:
        """List all registered skills with metadata."""
        return [
            {
                "name": cls.name,
                "description": cls.description,
                "version": cls.version,
            }
            for cls in self._skills.values()
        ]

    def invoke(self, name: str, input_data: dict, config: dict | None = None):
        """Instantiate and run a skill by name."""
        skill_class = self._skills.get(name)
        if not skill_class:
            raise KeyError(f"Skill '{name}' not found. Available: {list(self._skills.keys())}")
        skill = skill_class(config=config)
        return skill.run(input_data)


# Global registry instance
registry = SkillRegistry()
