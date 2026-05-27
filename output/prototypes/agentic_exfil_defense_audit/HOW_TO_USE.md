# How to Use

## Option A: Claude Code Skill (recommended)

### Install

```bash
mkdir -p ~/.claude/skills/agentic_exfil_defense_audit
cp SKILL.md ~/.claude/skills/agentic_exfil_defense_audit/SKILL.md
```

### Trigger Phrases

Say any of these to Claude Code:

- "Audit my agentic system for data exfiltration risks"
- "Check if my AI agent could leak files via prompt injection"
- "Review my copilot integration for the lethal trifecta pattern"
- "Security review my AI agent's output rendering pipeline"
- "copilot security audit"

Claude will walk through the 6-step audit process from the skill: map attack surface, check for lethal trifecta, audit output rendering, audit auto-actions, apply mitigations, and test with a proof-of-concept canary.

## Option B: Standalone Scanner

### Install

```bash
git clone <this-repo>
cd agentic_exfil_defense_audit
# No pip install needed — stdlib only, Python 3.7+
```

### Run

```bash
# Scan a directory of agent code
python3 audit.py /path/to/your/agent/

# Scan a single config file
python3 audit.py agent_config.json

# JSON output (for CI/CD integration)
python3 audit.py /path/to/agent/ --json

# Write report to file
python3 audit.py /path/to/agent/ -o report.txt
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No critical findings |
| 1 | Critical findings but no lethal trifecta |
| 2 | Lethal trifecta detected — exfiltration possible |

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Exfiltration audit
  run: python3 audit.py ./src/agent/ --json -o audit-report.json
  # Fails the build if lethal trifecta is found (exit code 2)
```

## First 60 Seconds

```bash
$ bash run.sh

========================================
 Agentic Exfiltration Defense Audit
 Demo: scanning sample vulnerable agent
========================================

--- [1/3] Scanning VULNERABLE agent config + handler ---

======================================================================
  AGENTIC EXFILTRATION DEFENSE AUDIT REPORT
======================================================================
  Target: samples/vulnerable_agent.json
  Findings: 18
  Critical: 4  |  High: 5

----------------------------------------------------------------------
  !! LETHAL TRIFECTA DETECTED !!

  [X] Untrusted Input:      Email processing
  [X] Sensitive Data:       Cloud storage access, Pre-authenticated URL generation
  [X] Exfiltration Channel: Email sending, HTML/Markdown rendering

  [CRITICAL]
  * Dangerous agent permission: Email sending permission
  * Approval explicitly disabled
  ...
```

The scanner finds the same vulnerability class as the Copilot Cowork disclosure — then you compare with the hardened handler to see which mitigations break the chain.
