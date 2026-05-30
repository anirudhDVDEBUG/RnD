# How to Use

## Install

```bash
git clone <this-repo>
cd customer_request_to_code_pipeline
# No pip install needed — pure Python 3.10+ stdlib
```

## Run

```bash
bash run.sh
```

Or directly:

```bash
python3 pipeline.py sample_requests.json
```

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/customer_request_to_code_pipeline
cp SKILL.md ~/.claude/skills/customer_request_to_code_pipeline/SKILL.md
```

**Trigger phrases that activate it:**

- "Turn this customer request into a code change"
- "Build a pipeline that converts support tickets into PRs"
- "Triage these feature requests and generate implementation plans"
- "Automate turning user feedback into engineering tasks with code"
- "Set up a workflow from customer input to code output"

Claude will follow the 5-step process (Parse → Map → Plan → Implement → Summarize) defined in the skill.

## First 60 Seconds

**Input** — `sample_requests.json` contains 5 realistic customer requests:

```json
{
  "id": "REQ-001",
  "source": "support_ticket",
  "customer": "Acme Corp",
  "title": "Add CSV export to dashboard analytics",
  "body": "We need to export our analytics dashboard data as CSV files...",
  "priority_signals": { "requesters": 12, "revenue_impact": "$240k ARR", "urgency": "high" }
}
```

**Output** — The pipeline produces:

1. **Terminal:** Color-coded triage summary table + detailed plans with generated code
2. **File:** `output_plans.md` — Markdown report ready for Slack/GitHub/Notion

Sample triage output:

```
 ID         PRI  TYPE           COMPLEXITY CUSTOMER         TITLE
 ──────────────────────────────────────────────────────────────────────
 REQ-004   95.0  new_feature    large      MegaRetail       Add role-based access control
 REQ-001   82.5  new_feature    medium     Acme Corp        Add CSV export to dashboard
 REQ-005   70.0  bug_fix        medium     HealthTech Pro   Rate limiting returns 500
 REQ-002   62.5  new_feature    small      DataFlow Inc     Support webhook retries
 REQ-003   41.3  bug_fix        medium     StartupXYZ       Search returns stale results
```

Each request gets a full plan: affected files, implementation steps, test strategy, risks, and generated code patches.

## Custom Input

Create your own JSON file following the schema:

```json
[
  {
    "id": "string",
    "source": "support_ticket | feature_request | bug_report",
    "customer": "string",
    "title": "string",
    "body": "string",
    "priority_signals": {
      "requesters": 0,
      "revenue_impact": "$0",
      "urgency": "low | medium | high"
    },
    "submitted_at": "ISO-8601"
  }
]
```

Then run:

```bash
python3 pipeline.py my_requests.json
```
