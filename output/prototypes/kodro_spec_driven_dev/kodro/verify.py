"""Phase 5: Verification — check requirement coverage and traceability."""

from dataclasses import dataclass, field
from typing import List, Dict
from .spec import Spec
from .codegen import GeneratedFile


@dataclass
class CoverageReport:
    total_requirements: int
    covered_requirements: int
    uncovered: List[str]
    file_coverage: Dict[str, List[str]]  # file -> [req IDs]

    @property
    def percent(self) -> float:
        if self.total_requirements == 0:
            return 100.0
        return round(100 * self.covered_requirements / self.total_requirements, 1)

    def summary(self) -> str:
        lines = [
            f"Verification: {self.percent}% requirement coverage",
            f"  {self.covered_requirements}/{self.total_requirements} requirements traced to code",
        ]
        if self.uncovered:
            lines.append(f"  UNCOVERED: {', '.join(self.uncovered)}")
        for fpath, reqs in self.file_coverage.items():
            lines.append(f"  {fpath}: {', '.join(reqs)}")
        return "\n".join(lines)


def verify_coverage(spec: Spec, files: List[GeneratedFile]) -> CoverageReport:
    """Check that every requirement is covered by at least one generated file."""
    all_reqs = {r.id for r in spec.requirements}
    covered = set()
    file_cov = {}

    for f in files:
        if f.requirements:
            file_cov[f.path] = f.requirements
            covered.update(f.requirements)

    return CoverageReport(
        total_requirements=len(all_reqs),
        covered_requirements=len(covered & all_reqs),
        uncovered=sorted(all_reqs - covered),
        file_coverage=file_cov,
    )
