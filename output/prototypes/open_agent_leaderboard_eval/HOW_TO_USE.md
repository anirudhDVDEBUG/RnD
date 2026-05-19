# How to Use

## This is a Claude Code Skill

### Install the Skill

Drop the skill file into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/open_agent_leaderboard_eval
cp SKILL.md ~/.claude/skills/open_agent_leaderboard_eval/SKILL.md
```

### Trigger Phrases

Once installed, Claude Code activates this skill when you say things like:

- "Benchmark my agent across multiple evaluation suites"
- "Compare agent architectures on SWE-Bench and AppWorld"
- "Submit my agent's results to the Open Agent Leaderboard"
- "Evaluate agent cost vs quality tradeoffs"
- "Set up Exgentic to run standardized agent evaluations"

---

## Running the Demo (no API keys needed)

### Prerequisites

- Python 3.9+
- No external packages required (stdlib only)

### Install

```bash
git clone <this-repo> open_agent_leaderboard_eval
cd open_agent_leaderboard_eval
pip install -r requirements.txt   # no-op — all stdlib
```

### Run

```bash
bash run.sh
```

### CLI Options

```bash
# Full evaluation across all 6 benchmarks
python3 evaluate.py

# Single benchmark
python3 evaluate.py --benchmark swe
python3 evaluate.py --benchmark airline

# Leaderboard comparison only
python3 evaluate.py --compare

# Export results to JSON
python3 evaluate.py --output results.json
```

Available benchmark shortcuts: `swe`, `browse`, `appworld`, `airline`, `retail`, `telecom`.

---

## First 60 Seconds

**Input:**
```bash
python3 evaluate.py --benchmark swe
```

**Output:**
```
========================================================================
  OPEN AGENT LEADERBOARD — EVALUATION RUN
========================================================================

  Agent:       MyAgent-Demo
  Model:       mock-model
  Benchmarks:  1
  Protocol:    Exgentic Unified (Task / Context / Actions)

  Running SWE-Bench Verified... done

========================================================================
  BENCHMARK RESULTS
========================================================================

  SWE-Bench Verified       ██████████░░░░░░░░░░  50.0%   $1.23/task
    ✓ django__django-16379              steps=12  cost=$0.87
    ✗ sympy__sympy-24213                steps=19  cost=$2.14
    ✓ scikit-learn__scikit-learn-25638  steps= 8  cost=$0.67
```

**What you see:** Per-task pass/fail, step count, cost in USD, and a visual progress bar. The full run adds aggregate metrics, cost analysis (failed vs successful), and your rank on the leaderboard.

---

## Using the Real Exgentic Framework

To move beyond mock data and evaluate a real agent:

### 1. Install Exgentic

```bash
git clone https://github.com/Exgentic/exgentic.git
cd exgentic
pip install -e .
```

### 2. Wrap Your Agent

Implement the three-part protocol your agent must speak:

```python
from exgentic import AgentProtocol

class MyAgent(AgentProtocol):
    def handle_task(self, task, context, actions):
        # task:    what to do
        # context: what you know (tools, rules, constraints)
        # actions: what operations are allowed
        ...
        return result
```

### 3. Run Against Real Benchmarks

```bash
exgentic run --agent my_agent.MyAgent --benchmarks swe,appworld,tau2-airline
```

### 4. Submit to the Leaderboard

1. Version your agent config (model, architecture, tools)
2. Open a PR at `huggingface.co/datasets/open-agent-leaderboard/results`
3. Include trajectories and cost reports
