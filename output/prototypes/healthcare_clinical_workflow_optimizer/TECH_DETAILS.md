# Technical Details

## What It Does

This prototype demonstrates an AI-powered clinical documentation pipeline modeled after enterprise healthcare deployments like AdventHealth's partnership with OpenAI. It generates draft clinical documents (progress notes, discharge summaries, patient messages, referral letters, care plans, after-visit summaries) from structured encounter data, enforces role-based access control, requires human-in-the-loop review for every output, maintains a HIPAA-aware audit trail, and reports impact metrics.

The demo uses template-based mock generation to run without API keys. In production, the `MockAIClient` class is replaced with a real LLM client (e.g., Claude API with a Business Associate Agreement) to produce contextually rich clinical text.

## Architecture

```
mock_data.py          6 fictional clinical encounters + access-denial scenario
       |
       v
workflow_engine.py    Core engine
  - ClinicalWorkflowOptimizer   Orchestrator: generate, approve, reject drafts
  - MockAIClient                Template-based text generation (swap for Claude API)
  - AuditLogger                 HIPAA-aware event log (no PHI stored)
       |
       v
demo.py               End-to-end demo script (called by run.sh)
```

### Key files

| File | Purpose |
|---|---|
| `workflow_engine.py` | Core classes: optimizer, mock AI client, audit logger |
| `mock_data.py` | 6 realistic clinical scenarios with fictional patient data |
| `demo.py` | Runnable demo showing all 5 pipeline stages |
| `run.sh` | One-command entry point |

### Data flow

1. Encounter data (structured dict) enters `generate_draft()`
2. Role-based access check against `ROLE_PERMISSIONS` matrix
3. `MockAIClient.generate()` fills a clinical template with encounter fields
4. Draft returned with `status: pending_clinician_approval`
5. Clinician calls `approve_draft()` (optionally with edits) or `reject_draft()`
6. Every action logged to `AuditLogger` (timestamps + action metadata, no PHI)
7. `get_metrics()` computes adoption, edit rate, and time-saved estimates

### Dependencies

- **Python 3.10+** (stdlib only — `json`, `datetime`, `re`, `sys`)
- No external packages for the demo
- Production would add: `anthropic` (Claude API), `pydantic` (validation), `sqlalchemy` (audit persistence)

## Limitations

- **Mock generation only**: Templates produce realistic-looking but formulaic text. Real LLM integration needed for production-quality drafts.
- **No EHR integration**: Encounter data is hardcoded. A real system would pull from FHIR/HL7 APIs or EHR adapters (Epic, Cerner).
- **No persistent storage**: Audit log and drafts live in memory. Production needs a database.
- **No encryption/auth**: Demo skips TLS, token auth, and encryption-at-rest that HIPAA requires.
- **Simplified metrics**: Time-saved estimates use a flat 3-min-per-draft heuristic. Real measurement requires before/after time studies.
- **No bias monitoring**: Production systems need demographic fairness auditing on AI outputs.

## Why This Matters for Claude-Driven Products

1. **Agent factories / workflow automation**: The `ClinicalWorkflowOptimizer` pattern (structured input -> LLM draft -> human review -> audit) generalizes to any domain where AI assists knowledge workers. Swap clinical templates for legal, financial, or marketing templates.

2. **Skill architecture**: This is packaged as a Claude Code Skill — drop `SKILL.md` into `~/.claude/skills/` and Claude gains healthcare workflow expertise. The same pattern works for any vertical skill.

3. **Compliance-first design**: The role-based access, audit trail, and human-in-the-loop patterns shown here are transferable to any regulated industry (fintech, legal, government).

4. **Metrics-driven adoption**: The built-in metrics dashboard (edit rate, time saved, adoption) provides the feedback loop needed to justify scaling AI tools inside organizations — directly applicable to enterprise sales and lead generation.
