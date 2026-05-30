# CVE Triage — Should I Care?

**TL;DR**: A Claude Code skill that triages CVEs against your actual project dependencies, producing a sourced verdict (AFFECTED / NOT AFFECTED / NOT APPLICABLE) with version-level precision. Drop the skill into `~/.claude/skills/` and ask "Should I care about CVE-2024-3094?" to get an instant, structured assessment.

## Headline Result

```
## CVE Triage: CVE-2024-3094

**Verdict**: [!!] AFFECTED

**CVSS Score**: 10.0 (CRITICAL)
**Affected Product**: xz-utils (>=5.6.0, <=5.6.1)

### Applicability to This Environment
- **Software present?**: Yes (`xz` v5.6.0 in `go.mod`)
- **Version in affected range?**: Yes

### Recommended Actions
- Upgrade to 5.6.2 or downgrade to 5.4.x immediately
- Check for indicators of compromise
```

## Quick Start

```bash
bash run.sh        # runs 4 triage scenarios with mock data, no API keys needed
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install as a Claude skill, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations

## Source

[moltenbit/should-i-care](https://github.com/moltenbit/should-i-care)
