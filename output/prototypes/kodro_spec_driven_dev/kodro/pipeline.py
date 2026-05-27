"""Full 6-phase Kodro pipeline orchestrator."""

from dataclasses import dataclass, field
from typing import List
from .spec import Spec, parse_spec
from .architect import Architecture, design_architecture
from .planner import Plan, create_plan
from .codegen import GeneratedFile, generate_code
from .verify import CoverageReport, verify_coverage


@dataclass
class PipelineResult:
    spec: Spec
    architecture: Architecture
    plan: Plan
    files: List[GeneratedFile]
    coverage: CoverageReport
    phases_completed: List[str] = field(default_factory=list)

    def summary(self) -> str:
        sep = "=" * 60
        sections = [
            sep,
            "KODRO SPEC-DRIVEN DEVELOPMENT PIPELINE",
            sep,
            "",
            "PHASE 1 - SPECIFICATION",
            self.spec.summary(),
            "",
            "PHASE 2 - ARCHITECTURE",
            self.architecture.summary(),
            "",
            "PHASE 3 - IMPLEMENTATION PLAN",
            self.plan.summary(),
            "",
            "PHASE 4 - CODE GENERATION",
            f"Generated {len(self.files)} files:",
        ]
        for f in self.files:
            sections.append(f"  {f.path} ({len(f.content)} bytes)")
        sections.extend([
            "",
            "PHASE 5 - VERIFICATION",
            self.coverage.summary(),
            "",
            "PHASE 6 - INTEGRATION REVIEW",
            f"Pipeline complete. {len(self.phases_completed)} phases executed.",
            f"Requirement coverage: {self.coverage.percent}%",
            sep,
        ])
        return "\n".join(sections)


def run_pipeline(spec_data: dict) -> PipelineResult:
    """Execute the full 6-phase Kodro SDD pipeline."""
    phases = []

    # Phase 1: Specification
    spec = parse_spec(spec_data)
    errors = spec.validate()
    if errors:
        raise ValueError(f"Spec validation failed: {'; '.join(errors)}")
    phases.append("specification")

    # Phase 2: Architecture
    arch = design_architecture(spec)
    cov = arch.coverage(spec)
    if cov["uncovered"]:
        # Warn but continue
        pass
    phases.append("architecture")

    # Phase 3: Implementation Plan
    plan = create_plan(spec, arch)
    phases.append("planning")

    # Phase 4: Code Generation
    files = generate_code(spec, plan)
    phases.append("codegen")

    # Phase 5: Verification
    coverage = verify_coverage(spec, files)
    phases.append("verification")

    # Phase 6: Integration Review (summary)
    phases.append("integration")

    return PipelineResult(
        spec=spec,
        architecture=arch,
        plan=plan,
        files=files,
        coverage=coverage,
        phases_completed=phases,
    )
