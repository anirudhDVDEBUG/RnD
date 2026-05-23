# Technical Details: Overkill

## What it actually does

Overkill is a Claude Code skill (a `SKILL.md` prompt file) that instructs Claude
to deliberately over-engineer any coding request. When triggered, Claude applies
as many design patterns, abstraction layers, and enterprise practices as possible
to the simplest tasks. The result is functional code that is intentionally bloated
-- serving as both comedy and a teaching tool for software design patterns.

The skill itself is a single Markdown file containing instructions. There is no
runtime code in the skill -- Claude generates all code on the fly based on the
SKILL.md prompt. The demo in this prototype shows what typical output looks like.

## Architecture of the demo

The demo (`overkill_demo.py`) over-engineers `a + b` into a full service:

```
User Input (2, 3)
  |
  v
EnterpriseAdditionService (Facade)
  |
  +-- CircuitBreaker.allow_request()
  +-- OperandValidator.validate()  (4-stage pipeline)
  +-- AdditionStrategyFactory.select_optimal_strategy()
  |     +-- BitManipulationAdditionStrategy  (integers)
  |     +-- KahanSummationStrategy           (large/small floats)
  |     +-- NaiveAdditionStrategy            (fallback: a + b)
  +-- strategy.add(a, b)
  +-- AdditionMetrics.record_success()
  +-- Result[AdditionResponse]
  |
  v
Output: 5.0
```

**Key files:**
- `overkill_demo.py` -- single-file implementation (~400 LOC, zero dependencies)
- `run.sh` -- runs the demo

**Dependencies:** Python 3.10+ stdlib only. No pip packages.

**Model calls:** None. The skill is a prompt-only artifact. Claude generates code
at conversation time; no API calls happen during execution of generated code.

## Design patterns demonstrated

| Pattern             | Where                                     |
|---------------------|-------------------------------------------|
| Strategy            | 3 interchangeable addition algorithms     |
| Factory             | Dynamic strategy selection by operand type|
| Facade              | `EnterpriseAdditionService` orchestrator  |
| Result Monad        | Railway-oriented error propagation        |
| Circuit Breaker     | Fault tolerance for addition failures     |
| Value Object        | Immutable `ValidatedOperand`, `AdditionRequest` |
| Pipeline            | 4-stage operand validation                |
| Feature Flags       | Runtime-toggleable behavior               |

## Limitations

- **It's a prompt, not a library.** The skill has no code of its own; it changes
  how Claude writes code. Output quality depends on the model.
- **No persistent state.** Each invocation is independent.
- **Not deterministic.** Claude may produce different over-engineered patterns on
  each run, though the spirit is consistent.
- **Language-dependent.** The skill defaults to TypeScript if no language is
  specified. Pattern applicability varies by language.

## Why it might matter

For teams building Claude-driven products:

- **Training & onboarding:** The generated code is a live catalog of design
  patterns. Ask Claude to overkill a simple task in your stack, and juniors get
  an annotated tour of Strategy, Factory, Circuit Breaker, etc.
- **Agent factory scaffolding:** When you actually DO need enterprise patterns
  (retry logic, circuit breakers, validation pipelines) in agent orchestration
  code, the overkill output is surprisingly close to production-ready -- just
  trim the jokes.
- **Content & marketing:** The absurdity is inherently shareable. "We made
  Claude write 400 lines to add two numbers" is a natural demo/blog post hook.
- **Code review training:** Use overkill output as a "spot the unnecessary
  abstraction" exercise for teams learning to balance robustness vs. simplicity.
