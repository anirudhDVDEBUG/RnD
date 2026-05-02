"""Base skill class that all production skills inherit from."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SkillResult:
    """Standard result envelope for all skill executions."""
    success: bool
    data: Any = None
    error: str | None = None
    metadata: dict = field(default_factory=dict)


class BaseSkill(ABC):
    """Production-grade base skill with logging, validation, and error handling."""

    name: str = "base_skill"
    description: str = "Base skill"
    version: str = "1.0.0"

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"skill.{self.name}")

    @abstractmethod
    def execute(self, input_data: dict) -> SkillResult:
        """Execute the skill logic. Subclasses must implement this."""
        ...

    def validate_input(self, input_data: dict) -> bool:
        """Override to add input validation."""
        return True

    def run(self, input_data: dict) -> SkillResult:
        """Public entry point with validation and error handling."""
        self.logger.info(f"Running skill: {self.name} v{self.version}")
        try:
            if not self.validate_input(input_data):
                return SkillResult(success=False, error="Input validation failed")
            result = self.execute(input_data)
            self.logger.info(f"Skill {self.name} completed successfully")
            return result
        except Exception as e:
            self.logger.error(f"Skill {self.name} failed: {e}")
            return SkillResult(success=False, error=str(e))
