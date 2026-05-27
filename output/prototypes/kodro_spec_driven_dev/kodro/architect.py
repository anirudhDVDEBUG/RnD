"""Phase 2: Architecture — decompose spec into components and interfaces."""

from dataclasses import dataclass, field
from typing import List, Dict
from .spec import Spec


@dataclass
class Component:
    name: str
    responsibility: str
    requirements_covered: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    pattern: str = ""


@dataclass
class Architecture:
    components: List[Component] = field(default_factory=list)
    interfaces: Dict[str, str] = field(default_factory=dict)

    def coverage(self, spec: Spec) -> dict:
        """Check which requirements are covered by components."""
        all_reqs = {r.id for r in spec.requirements}
        covered = set()
        for c in self.components:
            covered.update(c.requirements_covered)
        return {
            "total": len(all_reqs),
            "covered": len(covered & all_reqs),
            "uncovered": sorted(all_reqs - covered),
        }

    def dependency_order(self) -> List[str]:
        """Topological sort of components by dependency."""
        name_set = {c.name for c in self.components}
        in_degree = {c.name: 0 for c in self.components}
        deps = {c.name: c.depends_on for c in self.components}

        for name, dep_list in deps.items():
            for d in dep_list:
                if d in name_set:
                    in_degree[name] += 1

        queue = [n for n, deg in in_degree.items() if deg == 0]
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for name, dep_list in deps.items():
                if node in dep_list:
                    in_degree[name] -= 1
                    if in_degree[name] == 0:
                        queue.append(name)
        return order

    def summary(self) -> str:
        lines = [f"Architecture: {len(self.components)} components"]
        for c in self.components:
            lines.append(f"  [{c.name}] {c.responsibility}")
            if c.requirements_covered:
                lines.append(f"    covers: {', '.join(c.requirements_covered)}")
            if c.depends_on:
                lines.append(f"    depends: {', '.join(c.depends_on)}")
        lines.append(f"Build order: {' -> '.join(self.dependency_order())}")
        return "\n".join(lines)


def design_architecture(spec: Spec) -> Architecture:
    """Auto-generate architecture from spec (heuristic decomposition)."""
    components = []

    # One component per data model
    for model in spec.data_models:
        components.append(Component(
            name=f"{model.name.lower()}_model",
            responsibility=f"Data layer for {model.name}",
            pattern="repository",
        ))

    # One service component per group of related endpoints
    if spec.api_endpoints:
        components.append(Component(
            name="service",
            responsibility="Business logic and endpoint handlers",
            requirements_covered=[r.id for r in spec.requirements],
            depends_on=[f"{m.name.lower()}_model" for m in spec.data_models],
            pattern="service",
        ))

    # Validation component if constraints exist
    if spec.constraints:
        components.append(Component(
            name="validator",
            responsibility="Input validation and constraint enforcement",
            pattern="strategy",
        ))

    # Test component
    components.append(Component(
        name="tests",
        responsibility="Verification of all requirements",
        requirements_covered=[r.id for r in spec.requirements],
        depends_on=[c.name for c in components],
        pattern="BDD",
    ))

    return Architecture(components=components)
