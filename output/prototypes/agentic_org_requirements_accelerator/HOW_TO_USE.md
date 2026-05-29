# How to Use

## Installation

```bash
git clone <this-repo>
cd agentic_org_requirements_accelerator
pip install -r requirements.txt
```

No API keys required — the demo uses built-in mock analysis engines. To connect real LLM backends, set `ANTHROPIC_API_KEY` and pass `--live` (see below).

## As a Claude Code Skill

### Install the skill

```bash
mkdir -p ~/.claude/skills/agentic_org_requirements_accelerator
cp SKILL.md ~/.claude/skills/agentic_org_requirements_accelerator/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code to activate the skill:

- "Help me speed up requirements analysis for this project"
- "Set up an agentic workflow for software delivery"
- "Analyze these requirements documents and extract actionable specs"
- "Build an agentic coding pipeline for our organization"
- "Reduce our requirements gathering timeline"

Claude will then follow the four-step pipeline (Gather, Analyze, Cross-Validate, Refine) described in the skill.

## First 60 seconds

### Input

Run with the bundled sample requirements (a mock e-commerce platform project):

```bash
bash run.sh
```

Or point it at your own requirements file:

```bash
python accelerator.py --input my_requirements.yaml
```

### Sample input (`sample_requirements.yaml`)

```yaml
project: "Enterprise E-Commerce Platform"
stakeholders:
  - name: "Product Owner"
    requirements:
      - "Users must be able to search products by keyword and category"
      - "Checkout must support multiple payment gateways"
```

### Output

The tool prints a structured report to stdout and writes `output/analysis_report.md`:

```
=== AGENTIC REQUIREMENTS ACCELERATOR ===

[Agent 1/4] Decomposition Agent ............ 12 user stories extracted
[Agent 2/4] Dependency Mapping Agent ....... 8 dependencies, 2 conflicts found
[Agent 3/4] Technical Feasibility Agent .... 12 estimates produced
[Agent 4/4] Specification Writer Agent ..... 12 specs generated

Cross-validation complete: 2 warnings, 1 gap identified

Output: output/analysis_report.md (47 items, 3 phases)
```

The markdown report contains:
- Prioritized backlog with acceptance criteria
- Dependency graph (text-based)
- Risk assessment matrix
- Phased delivery plan
