---
name: kodro_spec_driven_dev
description: |
  Spec-Driven Development Framework that prevents "vibe coding" with a disciplined 6-phase autonomous pipeline. Lowers token costs by ~84% through structured specification-first development.
  TRIGGER when: user asks for spec-driven development, wants to prevent vibe coding, needs a structured multi-phase coding pipeline, wants to reduce token costs in AI coding, or asks for disciplined autonomous code generation.
  DO NOT TRIGGER when: user wants simple one-off code snippets, is doing exploratory prototyping, or explicitly wants freeform coding.
---

# Kodro: Spec-Driven Development Framework

A production-grade, spec-driven development framework that replaces unstructured "vibe coding" with a disciplined 6-phase autonomous pipeline.

## When to use

- "Build this feature using spec-driven development"
- "I want a structured pipeline to develop this — no vibe coding"
- "Generate code from a specification with minimal token usage"
- "Use a multi-phase autonomous approach to build this module"
- "Help me implement this with a disciplined SDD workflow"

## How to use

### Phase 1: Specification
Write a clear, complete specification before any code is generated.

1. Define the **purpose** and **scope** of the feature or module.
2. List **functional requirements** as concrete, testable statements.
3. Specify **inputs, outputs, data models**, and **API contracts**.
4. Document **constraints**, **edge cases**, and **non-functional requirements** (performance, security).

```markdown
# Spec: [Feature Name]

## Purpose
[One-paragraph description of what this does and why]

## Requirements
- REQ-1: [Testable requirement]
- REQ-2: [Testable requirement]

## Data Models
[Define schemas, types, interfaces]

## API Contract
[Endpoints, function signatures, I/O formats]

## Constraints
[Performance targets, security rules, compatibility]
```

### Phase 2: Architecture
Design the solution structure before writing implementation code.

1. Break the spec into **modules/components**.
2. Define **interfaces** between components.
3. Choose **patterns** (e.g., repository, strategy, pipeline).
4. Map requirements to components.

### Phase 3: Implementation Plan
Create a step-by-step implementation checklist.

1. Order tasks by dependency.
2. Each task should be small and independently verifiable.
3. Identify which spec requirements each task fulfills.

### Phase 4: Code Generation
Generate code one component at a time, following the plan.

1. Implement each component against its spec.
2. Follow existing project conventions.
3. Keep each unit focused — one responsibility per module.
4. Reference requirement IDs in code comments where non-obvious.

### Phase 5: Verification
Verify every requirement is met.

1. Write or generate **tests** for each requirement (BDD-style preferred).
2. Run tests and fix failures.
3. Cross-check spec requirements against implementation — every REQ must be covered.

### Phase 6: Integration & Review
Integrate, review, and finalize.

1. Integrate components and run full test suite.
2. Review for spec compliance, code quality, and security.
3. Document any deviations from the original spec with rationale.

### Token Optimization Tips

- **Spec first**: A clear spec reduces back-and-forth and rework, cutting token usage dramatically.
- **Phased generation**: Generate code in focused chunks rather than all at once.
- **Requirement tracing**: Map each code unit to a requirement — avoid generating unnecessary code.
- **Reuse over rewrite**: Check for existing utilities before generating new ones.

## Example Workflow

```
User: Build a user authentication module with JWT tokens

Phase 1 → Write spec (requirements, data models, API contract)
Phase 2 → Architecture (auth service, token manager, middleware)
Phase 3 → Plan (1. token manager, 2. auth service, 3. middleware, 4. tests)
Phase 4 → Generate each component against spec
Phase 5 → Verify all requirements with tests
Phase 6 → Integrate and review
```

## References

- Source: [mharoon1578/kodro](https://github.com/mharoon1578/kodro) — Spec-Driven Development Framework for production
- Concepts: Spec-Driven Development (SDD), BDD, multi-agent pipelines, token optimization
