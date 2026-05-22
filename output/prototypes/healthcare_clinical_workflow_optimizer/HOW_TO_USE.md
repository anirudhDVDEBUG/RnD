# How to Use

## Install

```bash
git clone <this-repo>
cd healthcare_clinical_workflow_optimizer
# No pip install needed — pure Python 3.10+ stdlib
```

## Run the demo

```bash
bash run.sh
```

This runs 6 clinical scenarios, demonstrates role-based access control, simulates clinician review (approve/edit/reject), prints an audit trail, and shows impact metrics. No API keys required.

## Using as a Claude Skill

This is a **Claude Code Skill**. To install:

1. Copy the skill folder:
   ```
   ~/.claude/skills/healthcare_clinical_workflow_optimizer/
   ```
   Place the `SKILL.md` file inside that folder.

2. **Trigger phrases** that activate the skill:
   - "Build an AI assistant that helps clinicians with documentation"
   - "Create a healthcare workflow tool that reduces paperwork"
   - "Design a patient communication system powered by AI"
   - "Automate repetitive healthcare administrative workflows"
   - "Help me build a clinical decision-support tool"

   Keywords: `healthcare workflow`, `clinical documentation AI`, `patient care automation`, `reduce administrative burden`, `EHR workflow`, `physician burnout reduction`

3. When triggered, Claude will use the skill's templates and architecture patterns to scaffold a clinical workflow optimizer tailored to your use case.

## First 60 Seconds

**Input:** Run `bash run.sh`

**Output** (abbreviated):

```
  Healthcare Clinical Workflow Optimizer
  ======================================

STEP 1  Generate AI Drafts Across 6 Clinical Workflows

  Scenario 1: Progress Note
  Clinician: DR-CHEN-4421 (physician)
  Patient:   Jane Doe
  Status:    pending_clinician_approval
  Word count: 112

  --- Draft Preview (first 6 lines) ---
  PROGRESS NOTE - 2026-05-22
  Patient: Jane Doe | MRN: MRN-00112233
  Provider: Dr. Lisa Chen
  ...

STEP 2  Role-Based Access Control
  Access correctly denied: Role 'admin' cannot generate 'discharge_summary'

STEP 3  Clinician Review (Approve / Edit / Reject)
  Draft #1 - Approved as-is
  Draft #3 - Approved with edits
  Draft #2 - Rejected (Missing key medication reconciliation details)

STEP 4  HIPAA-Compliant Audit Trail
  Total audit events: 17

STEP 5  Impact Metrics Dashboard
  Total drafts generated: 6
  Approved:              2
  Edit rate:             50%
  Est. hours saved/month: 2.0
```

## Programmatic Usage

```python
from workflow_engine import ClinicalWorkflowOptimizer

optimizer = ClinicalWorkflowOptimizer()

# Generate a draft
result = optimizer.generate_draft(
    workflow_type="progress_note",
    context={"patient_name": "Jane Doe", "chief_complaint": "headache", ...},
    clinician_id="DR-SMITH-1234",
    role="physician",
)

print(result["draft"])        # The generated text
print(result["status"])       # "pending_clinician_approval"

# Clinician approves
optimizer.approve_draft(result["id"], "DR-SMITH-1234")

# Check metrics
print(optimizer.get_metrics())
```
