---
name: ai_native_dev_workflow
description: |
  AI-Native development workflow methodology using the 4-Phase framework for multi-agent collaboration.
  TRIGGER: user mentions "ai-native workflow", "multi-agent development", "4-phase framework",
  "parallel agent work", "ai dev methodology", "shared contract agents", "claude code multi-agent",
  "greenfield ai project", "existing codebase ai workflow"
---

# AI-Native Development Workflow (4-Phase Framework)

A methodology for AI-Native development that enables AI agents (like Claude Code) to work in parallel under shared contracts. Supports two scenarios: greenfield (empty) projects and existing codebases.

## When to use

- "How do I set up a multi-agent AI development workflow?"
- "I want AI agents to work in parallel on my project"
- "What's the 4-phase framework for AI-native development?"
- "How do I structure a new project for AI agent collaboration?"
- "How do I onboard AI agents to an existing codebase?"

## How to use

### Overview: The 4-Phase Framework

The AI-Native workflow divides development into four sequential phases. Each phase produces artifacts (contracts) that downstream phases consume, enabling multiple AI agents to work in parallel without conflicts.

### Phase 1: Align — Define the Blueprint

Establish the project's high-level architecture and shared understanding.

1. **Define project scope** — Write a clear project brief with goals, constraints, and success criteria
2. **Create the architecture doc** — Outline system components, data flow, and technology choices
3. **Establish conventions** — Set coding standards, file/folder naming conventions, and commit message formats
4. **Output**: `ARCHITECTURE.md`, `CONVENTIONS.md`, project brief

For **greenfield projects**:
- Start from scratch: define tech stack, folder structure, and module boundaries
- Create a skeleton project with placeholder modules

For **existing codebases**:
- Audit the current codebase: identify patterns, conventions, and architecture
- Document existing implicit conventions explicitly
- Identify areas that need refactoring or standardization

### Phase 2: Design — Define Contracts

Break the system into modules with clear interfaces (contracts) so agents can work independently.

1. **Define module boundaries** — Each module should have a single responsibility
2. **Specify interfaces/contracts** — Define API contracts, data schemas, type definitions, and function signatures
3. **Create task breakdown** — Split work into independent, parallelizable tasks with clear inputs/outputs
4. **Output**: Interface definitions, API contracts, task list with dependencies mapped

Key principles:
- Contracts are the **shared source of truth** between agents
- Each task should be completable by one agent without needing another agent's in-progress work
- Define integration points and test contracts upfront

### Phase 3: Build — Parallel Execution

Multiple AI agents work in parallel, each on their assigned task, following the contracts from Phase 2.

1. **Assign tasks to agents** — Each agent gets a scoped task with clear contract references
2. **Agents work independently** — Each agent implements against the shared contracts
3. **Use branch-per-task** — Each agent works on a separate git branch to avoid conflicts
4. **Validate against contracts** — Each agent writes tests that verify contract compliance
5. **Output**: Implemented modules with tests, one branch per task

Best practices:
- Agents should NOT modify shared contracts without coordination
- Each agent's CLAUDE.md or context should reference the relevant contracts
- Keep agent scope narrow: one module, one feature, one responsibility

### Phase 4: Integrate — Merge and Verify

Bring all parallel work together and verify the system works as a whole.

1. **Merge branches** — Integrate agent branches into the main branch
2. **Run integration tests** — Verify cross-module interactions against contracts
3. **Resolve conflicts** — Fix any integration issues from parallel development
4. **End-to-end validation** — Run the full system and validate against Phase 1 goals
5. **Output**: Working integrated system, deployment-ready code

### Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | What to Do Instead |
|---|---|---|
| **Skipping Phase 2 (contracts)** | Agents make incompatible assumptions | Always define interfaces before building |
| **Shared mutable state** | Agents overwrite each other's work | Use branch-per-task, merge at integration |
| **Vague task scoping** | Agent produces wrong output or scope-creeps | Define clear inputs, outputs, and boundaries per task |
| **Modifying contracts mid-build** | Breaks other agents' in-progress work | Freeze contracts during Phase 3; iterate in a new cycle |
| **Giant monolithic tasks** | Agent loses context or makes errors | Break into small, focused, independently testable tasks |
| **No integration tests** | Modules work alone but fail together | Write contract-compliance tests in Phase 2, run in Phase 4 |
| **Skipping the Align phase** | Agents build the wrong thing | Invest time upfront to define goals and architecture |

### Setting Up Multi-Agent Collaboration

1. **Create a shared `CLAUDE.md`** at the project root with:
   - Architecture overview and module map
   - Coding conventions and standards
   - Contract file locations
   - Branch naming conventions (e.g., `agent/<task-name>`)

2. **Per-agent context**: Give each agent a scoped prompt that includes:
   - Their specific task description
   - Relevant contract/interface files to reference
   - Which files/directories they own
   - What NOT to modify

3. **Contract files**: Store shared contracts in a known location (e.g., `contracts/`, `interfaces/`, or `types/`):
   - API schemas (OpenAPI, GraphQL, protobuf)
   - Type definitions / data models
   - Integration test specifications

## References

- **Source**: [tianji-qingtian/AI-Native](https://github.com/tianji-qingtian/AI-Native) — AI-Native development workflow methodology with 4-Phase framework, dual-scenario support, and anti-pattern reference
- **Topics**: multi-agent, dev-workflow, ai-native, claude-code, methodology
