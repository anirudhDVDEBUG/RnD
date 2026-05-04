# Anthropic Grade Optimizer

**Audit any Claude-directing artifact (CLAUDE.md, SKILL.md, subagent prompts, hooks, MCP configs) against 189 cited Anthropic rules across 11 dimensions.**

Every finding cites a specific rule or stays silent. Voice drift trumps score.

## Headline Result

```
$ bash run.sh
Auditing: sample_claude.md

  Overall Grade: B-
  Dimensions Passing: 7/11
  Critical Findings: 3
  Voice Drift Detected: Yes

  Top fix: Lines 12-14 mix imperative and conversational tone — Rule §4.2 (Voice Consistency)
```

## Quick Links

- [HOW_TO_USE.md](HOW_TO_USE.md) — Install, activate the skill, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — Architecture, rule engine, limitations
