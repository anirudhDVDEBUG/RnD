"""Parse and normalize raw requirements from YAML into internal format."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import yaml


@dataclass
class Requirement:
    id: str
    source: str
    text: str
    domain: str  # functional, non-functional, technical
    priority: str  # critical, high, medium, low

    @property
    def priority_rank(self) -> int:
        return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(self.priority, 4)


@dataclass
class ProjectIntake:
    project_name: str
    description: str
    requirements: List[Requirement] = field(default_factory=list)


def parse_requirements(path: str) -> ProjectIntake:
    data = yaml.safe_load(Path(path).read_text())

    intake = ProjectIntake(
        project_name=data.get("project", "Unnamed Project"),
        description=data.get("description", ""),
    )

    req_id = 1
    for stakeholder in data.get("stakeholders", []):
        source = stakeholder["name"]
        for req in stakeholder.get("requirements", []):
            if isinstance(req, str):
                text, domain, priority = req, "functional", "medium"
            else:
                text = req["text"]
                domain = req.get("domain", "functional")
                priority = req.get("priority", "medium")

            intake.requirements.append(
                Requirement(
                    id=f"REQ-{req_id:03d}",
                    source=source,
                    text=text,
                    domain=domain,
                    priority=priority,
                )
            )
            req_id += 1

    return intake
