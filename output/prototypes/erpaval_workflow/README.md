# ERPAVal Workflow

**Structured six-phase autonomous development for Claude Code.** ERPAVal routes every task through Explore, Research, Plan, Act, Validate, and Compound — with a classifier that picks the right emphasis and a lessons store that compounds knowledge across runs.

## Headline result

```
Task: "Fix the login timeout bug"
  -> Classifier: bug_fix (confidence 25%)
  -> Emphasized phases: explore, validate
  -> 6 phases executed, lesson captured, 42/42 tests pass
```

## Quick links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install the skill, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations
- **Run the demo:** `bash run.sh` (no API keys needed)
