# How to Use

## Install

```bash
# No dependencies needed — runs on Python 3.10+ stdlib only
git clone <this-repo>
cd cnc_manufacturability_multi_agent
bash run.sh
```

For production use with real STEP files and LLM agents, install optional deps:

```bash
pip install cadquery langchain langchain-community fastapi uvicorn
```

## Claude Skill Setup

This is a **Claude Code Skill**. To install:

1. Copy the skill folder to your skills directory:
   ```bash
   mkdir -p ~/.claude/skills/cnc-manufacturability/
   cp SKILL.md ~/.claude/skills/cnc-manufacturability/SKILL.md
   ```

2. Trigger phrases that activate the skill:
   - "Build a system that checks if a part is manufacturable on our CNC machines"
   - "Create a multi-agent pipeline to analyze STEP files for manufacturing feasibility"
   - "Automate DFM checks against our shop's tool inventory"
   - "Build a manufacturability report generator for machine shop quoting"
   - "I need an AI system that extracts features from CAD files and determines required tooling"

## First 60 Seconds

Run the pipeline with default settings (steel bracket):

```bash
$ python3 pipeline.py
[Stage 1/5] Extracting features from STEP file...
  -> 3 hole groups, 2 thread specs, 1 pockets  (0.00s)
[Stage 2/5] Classifying required CNC operations...
  -> 7 operations identified  (0.00s)
[Stage 3/5] Matching against shop tool inventory...
  -> 6 matched, 1 missing  (86% match)  (0.00s)
[Stage 4/5] Making feasibility decision...
  -> CONDITIONAL (confidence: HIGH)  (0.00s)
[Stage 5/5] Generating manufacturability report...
  -> Report ready  (0.00s)

--- Structured JSON Output ---
{
  "decision": "CONDITIONAL",
  "confidence": "HIGH",
  "missing_tools": 1,
  "procurement_cost_usd": 15,
  "risk_flags": ["Verify spindle speed range for Steel 304 ..."]
}

======================================================================
  CNC MANUFACTURABILITY REPORT
======================================================================
  VERDICT: [COND] CONDITIONAL
  ...
```

Try different scenarios:

```bash
# Simple aluminum plate — likely full PASS
python3 pipeline.py --part simple_plate --material "Aluminum 6061"

# Titanium with tight tolerance — more risk flags
python3 pipeline.py --part sample_bracket --material "Titanium Grade 5" --tolerance 0.01
```

## CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--part` | `sample_bracket` | Mock part (`sample_bracket` or `simple_plate`) |
| `--material` | `Steel 304` | Material (`Steel 304`, `Aluminum 6061`, `Titanium Grade 5`) |
| `--tolerance` | `0.05` | Required tolerance in mm |

## Production Mode

To use with real STEP files and an LLM backend:

1. Start vLLM with an OpenAI-compatible endpoint:
   ```bash
   python -m vllm.entrypoints.openai.api_server \
     --model Qwen/Qwen2.5-7B-Instruct \
     --host 0.0.0.0 --port 8000
   ```

2. Replace the rule-based agents in `agents.py` with LangChain LLM calls pointed at `http://localhost:8000/v1`.

3. Use `step_parser.try_real_parser("path/to/file.step")` for actual CAD geometry extraction (requires cadquery + OpenCASCADE).
