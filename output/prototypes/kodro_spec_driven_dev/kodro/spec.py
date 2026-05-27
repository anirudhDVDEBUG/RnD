"""Phase 1: Specification — parse and validate structured specs."""

import json
import re
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Requirement:
    id: str
    text: str
    category: str = "functional"


@dataclass
class DataModel:
    name: str
    fields: dict


@dataclass
class APIEndpoint:
    method: str
    path: str
    description: str
    request_schema: Optional[dict] = None
    response_schema: Optional[dict] = None


@dataclass
class Spec:
    name: str
    purpose: str
    requirements: List[Requirement] = field(default_factory=list)
    data_models: List[DataModel] = field(default_factory=list)
    api_endpoints: List[APIEndpoint] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        """Return list of validation errors (empty = valid)."""
        errors = []
        if not self.name.strip():
            errors.append("Spec must have a name")
        if not self.purpose.strip():
            errors.append("Spec must have a purpose")
        if not self.requirements:
            errors.append("Spec must have at least one requirement")

        # Check requirement IDs are unique
        ids = [r.id for r in self.requirements]
        if len(ids) != len(set(ids)):
            errors.append("Requirement IDs must be unique")

        # Check requirement ID format
        for r in self.requirements:
            if not re.match(r"^REQ-\d+$", r.id):
                errors.append(f"Invalid requirement ID format: {r.id} (expected REQ-NNN)")

        return errors

    def summary(self) -> str:
        lines = [
            f"Spec: {self.name}",
            f"Purpose: {self.purpose}",
            f"Requirements: {len(self.requirements)}",
            f"Data Models: {len(self.data_models)}",
            f"API Endpoints: {len(self.api_endpoints)}",
            f"Constraints: {len(self.constraints)}",
        ]
        return "\n".join(lines)


def parse_spec(data: dict) -> Spec:
    """Parse a spec from a dictionary (e.g. loaded from JSON/YAML)."""
    reqs = [
        Requirement(id=r["id"], text=r["text"], category=r.get("category", "functional"))
        for r in data.get("requirements", [])
    ]
    models = [
        DataModel(name=m["name"], fields=m["fields"])
        for m in data.get("data_models", [])
    ]
    endpoints = [
        APIEndpoint(
            method=e["method"],
            path=e["path"],
            description=e["description"],
            request_schema=e.get("request_schema"),
            response_schema=e.get("response_schema"),
        )
        for e in data.get("api_endpoints", [])
    ]
    return Spec(
        name=data["name"],
        purpose=data["purpose"],
        requirements=reqs,
        data_models=models,
        api_endpoints=endpoints,
        constraints=data.get("constraints", []),
    )
