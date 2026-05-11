# Technical Details

## What It Does

This is a multi-agent pipeline for automated CNC manufacturability analysis. Given a part's geometry (extracted from STEP/CAD files), material, and tolerances, it determines whether a machine shop can manufacture the part with its existing tool inventory. The system classifies required CNC operations (drilling, milling, tapping, chamfering), matches them against shop tooling, produces a GO/NO-GO/CONDITIONAL verdict, and generates a full report with risk flags, action items, and procurement costs.

The original MachinaCheck project ran on AMD MI300X GPUs using Qwen 2.5 7B via vLLM for the LLM-backed agents. This demo replaces the LLM calls with deterministic rule-based logic so it runs instantly without any model server or API keys.

## Architecture

```
STEP File ──> [1. Parser] ──> Features
                                  │
Material + Tolerance ─────────────┤
                                  v
                          [2. Ops Classifier]  ──> Required Operations
                                  │
                                  v
                          [3. Tool Matcher]     ──> Availability Report
                                  │
                                  v
                          [4. Feasibility]      ──> Decision JSON
                                  │
                                  v
                          [5. Report Gen]       ──> Full Report
```

### Key Files

| File | Role |
|------|------|
| `pipeline.py` | Orchestrator — runs all 5 stages sequentially, CLI entry point |
| `step_parser.py` | Stage 1 — mock STEP feature extraction (+ real cadquery path) |
| `agents.py` | Stages 2, 4, 5 — operations classifier, feasibility decision, report generator |
| `tool_database.py` | Stage 3 — shop inventory DB + deterministic tool matching |

### Data Flow

1. **Input:** Part name (mock) or STEP file path (production), material string, tolerance float
2. **Features dict:** bounding box, holes (diameter/depth/count), threads, chamfers, fillets, pockets
3. **Operations list:** each operation has a tool_type, diameter/thread, and reason
4. **Tool match results:** matched tools (with IDs), missing tools (with procurement costs), match rate %
5. **Feasibility JSON:** decision, confidence, reason, action_items, risk_flags, setup_hours
6. **Report:** formatted text block with all sections

### Dependencies

- **Demo mode:** Python 3.10+ stdlib only (zero external deps)
- **Production:** cadquery (OpenCASCADE), langchain, vLLM, FastAPI

### Design Decisions

- **LLMs only for reasoning, not data:** Geometry extraction and tool matching are pure Python — deterministic, fast, no hallucination risk. Only the operations classifier, feasibility judgment, and report prose use an LLM.
- **Structured output:** The feasibility agent returns typed JSON with a fixed schema, not free-form text.
- **On-premise inference:** vLLM runs locally — proprietary CAD data never leaves the network.

## Limitations

- **Mock geometry only in demo:** Without cadquery/OpenCASCADE installed, features come from hardcoded mock data. Real STEP parsing requires system-level OpenCASCADE libraries.
- **No LLM reasoning in demo:** The rule-based agents approximate what the LLM would do. In production, the LLM handles edge cases, material-specific reasoning, and nuanced trade-offs that rules can't capture.
- **Simplified tool matching:** The matcher does exact diameter/thread lookup. A production system would handle tolerance bands, tool substitution, and multi-setup planning.
- **No multi-axis analysis:** The current pipeline assumes 3-axis CNC. 4/5-axis feasibility, undercut detection, and fixturing analysis are not implemented.
- **Two mock parts:** Only `sample_bracket` and `simple_plate` are available without real STEP files.

## Relevance to Claude-Driven Products

**Agent factories / multi-agent orchestration:** This is a clean example of a linear multi-agent pipeline where some agents are LLM-backed and others are deterministic. The pattern — parse structured input, classify with LLM, match deterministically, decide with LLM, generate with LLM — applies broadly to:

- **Quoting / lead-gen automation:** Replace "CNC tool inventory" with "service catalog" and you have an automated quoting pipeline that checks whether you can fulfill a client request.
- **Ad creative feasibility:** Same architecture could check whether creative assets meet platform specs (image sizes, text ratios, format requirements) before submission.
- **Manufacturing-as-a-service platforms:** Embedded manufacturability checks for online CNC ordering services.

The key architectural insight is **knowing when NOT to use an LLM** — tool matching and geometry extraction are faster, cheaper, and more reliable as pure code.
