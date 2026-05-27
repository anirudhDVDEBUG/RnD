# How to Use

## Option A: As a Claude Code Skill (recommended)

### Install

```bash
mkdir -p ~/.claude/skills/oss_security_report_triage
cp SKILL.md ~/.claude/skills/oss_security_report_triage/SKILL.md
```

### Trigger phrases

Once installed, Claude Code activates this skill when you say any of:

- "Help me triage this security vulnerability report"
- "Assess the severity of this bug report"
- "Draft a response to this security disclosure"
- "Prioritize these incoming CVE candidates"
- "Help me manage the flood of AI-generated security reports"
- Any mention of "security report triage", "bug bounty triage", "CVE assessment"

### Example interaction

```
You:   Help me triage this vulnerability report:
       "A heap buffer overflow in parse_idn_host() allows RCE via crafted IDN..."

Claude: [Runs the 5-step triage process from the skill]
        - Classifies the report
        - Estimates CVSS severity
        - Checks for AI-generation signals
        - Assesses reproducibility
        - Drafts a response
```

## Option B: As a standalone CLI tool

### Install

```bash
git clone <this-repo>
cd oss_security_report_triage
# No dependencies beyond Python 3.10+
```

### Run the full demo queue

```bash
bash run.sh
```

### Triage a specific report

```bash
python3 triage.py SR-2026-0042
```

### Use your own reports

Edit `mock_reports.json` to add your reports in this format:

```json
{
  "id": "SR-YYYY-NNNN",
  "title": "Short description",
  "reporter": "email@example.com",
  "submitted": "2026-05-25T14:22:00Z",
  "component": "lib/file.c",
  "function": "vulnerable_func()",
  "claimed_impact": "Remote Code Execution",
  "attack_vector": "Network",
  "description": "Full report text...",
  "poc": "Proof of concept command or description",
  "ai_indicators": []
}
```

## First 60 seconds

```
$ bash run.sh

==============================================================================
  OSS SECURITY REPORT TRIAGE ENGINE
  Helping maintainers survive the AI-generated report flood
==============================================================================

TRIAGE QUEUE SUMMARY
------------------------------------------------------------------------------

  CONFIRMED (2)
    [       MEDIUM] SR-2026-0042 Integer overflow in Content-Length parsing...
    [       MEDIUM] SR-2026-0044 CRLF injection in custom header passthrou...

  ANALYZING (1)
    [       MEDIUM] SR-2026-0045 Null pointer dereference in SOCKS5 proxy... [AI?]

  REJECTED (2)
    [         HIGH] SR-2026-0041 Heap buffer overflow in URL parser via cr... [AI?]
    [         HIGH] SR-2026-0043 Use-after-free in connection pool during... [AI?]

  Total: 5  |  Confirmed: 2  |  Rejected: 2  |  AI-flagged: 3

  [Detailed results and draft responses for each report follow...]
```

The two AI-generated reports with no PoC are auto-rejected with professional response drafts. The two human-written reports with evidence are confirmed. One borderline report is held for analysis.
