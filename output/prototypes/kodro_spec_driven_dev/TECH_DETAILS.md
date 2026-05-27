# Technical Details

## What It Does

Kodro is a spec-driven development (SDD) framework that enforces a 6-phase pipeline: Specification, Architecture, Planning, Code Generation, Verification, and Integration Review. Instead of letting an LLM generate code in a single unstructured pass ("vibe coding"), Kodro forces each phase to complete and validate before proceeding to the next. The spec is the single source of truth — every generated file traces back to specific requirement IDs.

The core claim is that this structured approach reduces token costs by ~84% compared to iterative vibe coding, because the upfront spec eliminates rework cycles, redundant context, and the back-and-forth that typically inflates token usage.

## Architecture

```
spec.json
    |
    v
[Phase 1: spec.py]       Parse + validate structured spec
    |
    v
[Phase 2: architect.py]  Decompose into components, assign reqs
    |
    v
[Phase 3: planner.py]    Topological sort -> ordered task list
    |
    v
[Phase 4: codegen.py]    Generate code stubs per component
    |
    v
[Phase 5: verify.py]     Requirement coverage analysis
    |
    v
[Phase 6: pipeline.py]   Integration summary
```

### Key Files

| File | Role |
|------|------|
| `kodro/spec.py` | Spec parsing, validation, Requirement/DataModel/APIEndpoint dataclasses |
| `kodro/architect.py` | Heuristic decomposition into components, dependency graph, coverage check |
| `kodro/planner.py` | Topological sort of components into ordered implementation tasks |
| `kodro/codegen.py` | Template-based code generation (models, services, tests, validators) |
| `kodro/verify.py` | Requirement-to-file traceability and coverage reporting |
| `kodro/pipeline.py` | Orchestrates all 6 phases, produces `PipelineResult` |
| `demo.py` | End-to-end demo with sample JWT auth spec |

### Data Flow

1. **Input**: JSON dict with `name`, `purpose`, `requirements[]`, `data_models[]`, `api_endpoints[]`, `constraints[]`
2. **Spec validation**: Checks for unique REQ-NNN IDs, non-empty fields
3. **Architecture**: Creates one component per data model + a service + validator + tests component; assigns requirement coverage
4. **Planning**: Topological sort ensures models are built before services, services before tests
5. **Code generation**: Template-based — produces Python dataclasses for models, function stubs for services, BDD-style test stubs
6. **Verification**: Cross-references generated files against requirement IDs, reports coverage percentage
7. **Output**: `PipelineResult` with full summary, all generated files, and coverage report

### Dependencies

- **Python 3.8+** standard library only (dataclasses, json, re, typing)
- Zero external packages
- No LLM API calls in the demo — the pipeline itself is deterministic

## Limitations

- **Code generation is template-based**: The local demo produces stubs/skeletons, not production-ready implementations. In the real Kodro workflow, Claude fills in the implementation guided by the spec.
- **No YAML support**: Specs must be JSON dicts (trivially convertible from YAML).
- **Architecture heuristics are simple**: The auto-decomposition creates one component per model + one service. Complex domain logic requires manual architecture input.
- **No incremental re-runs**: Changing one requirement re-runs the entire pipeline. There's no diff-based regeneration.
- **The 84% savings claim** is based on the original repo's benchmarks comparing SDD to unstructured multi-turn conversations. Your mileage will vary by task complexity.

## Why It Matters for Claude-Driven Products

**Agent factories / multi-agent pipelines**: Kodro's 6-phase structure maps directly to a multi-agent pipeline where each agent handles one phase. You can wire Phase 1 to a spec-writing agent, Phase 4 to a coding agent, Phase 5 to a testing agent — each with a narrow, well-defined context window.

**Token cost management**: For teams building products on Claude's API (lead-gen tools, marketing automation, ad creative generators), token costs are a real line item. A spec-first approach that cuts 80%+ of wasted tokens translates directly to lower API bills.

**Quality gates**: The verification phase provides a programmatic check that every requirement has code. This is useful for regulated domains or anywhere you need an audit trail from requirement to implementation.

**Skill composability**: As a Claude Code skill, Kodro can be combined with other skills (e.g., a testing skill, a deployment skill) to create a full end-to-end development pipeline triggered by natural language.
