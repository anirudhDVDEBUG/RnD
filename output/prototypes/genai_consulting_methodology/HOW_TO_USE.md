# How to Use

## What this is

A **Claude Code skill** that teaches Claude how to run enterprise GenAI maturity assessments using a structured L1-L5 model and an eight-stage consulting framework. It also ships as a standalone Python CLI.

---

## Option A: Install as a Claude Code Skill

### 1. Copy the skill folder

```bash
mkdir -p ~/.claude/skills/genai_consulting_methodology
cp SKILL.md ~/.claude/skills/genai_consulting_methodology/SKILL.md
```

Or if you cloned the source repo:

```bash
cp -r path/to/GenAI-Consulting-Methodology-Toolkit/.claude/skills/genai_consulting_methodology \
      ~/.claude/skills/
```

### 2. Trigger phrases

Once installed, Claude Code activates this skill when you say things like:

- "Assess our organization's AI maturity level"
- "Create a GenAI transformation roadmap for the enterprise"
- "What stage of AI adoption is this company at?"
- "Design an AI governance framework"
- "Help me run a consulting engagement for enterprise AI"

Claude will walk through the L1-L5 diagnosis, ask about each dimension, and produce a scorecard + roadmap.

---

## Option B: Run the standalone CLI

### 1. Prerequisites

- Python 3.8+
- No external packages (stdlib only)

### 2. Install

```bash
git clone https://github.com/MorrisLu-Taipei/GenAI-Consulting-Methodology-Toolkit.git
cd GenAI-Consulting-Methodology-Toolkit
```

Or just use this prototype directory directly — the `assess.py` tool is self-contained.

### 3. Run with mock data

```bash
bash run.sh
```

### 4. Run with your own company profile

Create a JSON file following this schema:

```json
{
  "company_name": "Your Corp",
  "industry": "FinTech",
  "dimensions": [
    {
      "dimension": "Strategy & Vision",
      "current_level": 3,
      "target_level": 5,
      "evidence": "Board-approved AI strategy; dedicated budget"
    },
    {
      "dimension": "Data & Infrastructure",
      "current_level": 2,
      "target_level": 4,
      "evidence": "Cloud data warehouse; no ML pipelines yet"
    },
    {
      "dimension": "Talent & Culture",
      "current_level": 2,
      "target_level": 4,
      "evidence": "3 data scientists; no prompt engineering skills"
    },
    {
      "dimension": "Governance & Ethics",
      "current_level": 1,
      "target_level": 3,
      "evidence": "No AI policy in place"
    },
    {
      "dimension": "Use Cases & Value",
      "current_level": 3,
      "target_level": 5,
      "evidence": "2 production ML models; 1 GenAI chatbot in pilot"
    }
  ],
  "use_cases": [
    {"name": "Customer support chatbot", "impact": 4, "feasibility": 5, "strategic_fit": 4},
    {"name": "Fraud detection enhancement", "impact": 5, "feasibility": 3, "strategic_fit": 5}
  ]
}
```

Then run:

```bash
python3 assess.py your_company.json
```

---

## First 60 seconds

```
$ bash run.sh

╔══════════════════════════════════════════════════════════════════════╗
║  GenAI Consulting Methodology Toolkit — Demo Run                   ║
╚══════════════════════════════════════════════════════════════════════╝

Running L1-L5 maturity assessment on mock company: Acme Manufacturing Co.

========================================================================
  GenAI MATURITY ASSESSMENT — ACME MANUFACTURING CO.
  Industry: Industrial Manufacturing
========================================================================

┌─ MATURITY SCORECARD ─────────────────────────────────────────────┐
│  Strategy & Vision         ██░░░  L2 (Exploring)
│  Data & Infrastructure     ██░░░  L2 (Exploring)
│  Talent & Culture          █░░░░  L1 (Initial/Ad-hoc)
│  Governance & Ethics       █░░░░  L1 (Initial/Ad-hoc)
│  Use Cases & Value         ██░░░  L2 (Exploring)
│──────────────────────────────────────────────────────────────────│
│  OVERALL                   ██░░░  L1.6 (Exploring)
└──────────────────────────────────────────────────────────────────┘

┌─ USE CASE PRIORITIZATION MATRIX ─────────────────────────────────┐
│  GenAI Knowledge Base for SOPs     4    5    4   4.35 ★
│  Predictive Maintenance (IoT+AI)   5    3    5   4.30 ★
│  Supplier Email Auto-Drafting      3    5    3   3.70
│  ...
└──────────────────────────────────────────────────────────────────┘

→ JSON summary written to assessment_output.json
```

**Input:** `mock_company.json` (company profile with dimension scores + use cases)
**Output:** Terminal report + `assessment_output.json` machine-readable summary
