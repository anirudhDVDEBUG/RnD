# How to Use — Token Cost Lint

## Install

No dependencies beyond Python 3.10+ stdlib.

```bash
git clone https://github.com/epoko77-ai/tokensave.git
cd tokensave
```

Or use this prototype directly:

```bash
cd output/prototypes/token_cost_lint
python3 audit.py --target /path/to/your/project
```

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/token_cost_lint
cp SKILL.md ~/.claude/skills/token_cost_lint/SKILL.md
```

**Trigger phrases that activate it:**
- "Audit my project for token waste"
- "Find token bloat in my codebase"
- "Reduce Claude API costs"
- "Lint my prompts for unnecessary token spend"
- "Optimize context window usage"
- "How can I cut LLM token costs?"

Once installed, Claude Code will automatically use the skill when you mention token savings, context bloat, or prompt optimization.

## First 60 Seconds

```bash
# 1. Run on the included sample project
bash run.sh

# 2. Run on your own project
python3 audit.py --target ~/my-agent-project --format report

# 3. Get JSON output for CI integration
python3 audit.py --target ~/my-agent-project --format json --output results.json

# 4. Compare against a baseline
python3 audit.py --target ~/my-agent-project --compare results.json
```

**Example output** (from `bash run.sh`):

```
====================================================================
  TOKEN COST LINT — AUDIT REPORT
====================================================================

  Target:           ./sample_project
  Files scanned:    2
  Total lines:      98
  Est. tokens:      612
  Waste tokens:     3,190
  Waste %:          21.4%

--------------------------------------------------------------------
  FINDINGS BY CATEGORY
--------------------------------------------------------------------

  [Unbounded History]
    Findings: 1  |  Est. waste: ~600 tokens

  [Retry Amplification]
    Findings: 1  |  Est. waste: ~500 tokens

  [Redundant Context]
    Findings: 1  |  Est. waste: ~500 tokens
  ...

====================================================================
  TOP RECOMMENDATIONS
====================================================================
  1. Add conversation history windowing — truncate or summarize beyond N turns.
  2. Cache file contents and share between agents instead of re-reading.
  3. Trim system prompts — remove boilerplate and duplicate role definitions.
  ...
```

## CLI Reference

```
python3 audit.py --target PATH   # Required: directory to audit
                 --format report  # Human-readable (default)
                 --format json    # Machine-readable JSON
                 --compare FILE   # Compare against baseline JSON
                 --output FILE    # Write to file instead of stdout
```
