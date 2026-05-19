# Dell Codex On-Prem Enterprise Deploy

**TL;DR:** A Claude Code skill that generates complete deployment plans for running OpenAI Codex AI coding agents on Dell on-premise and hybrid infrastructure. Input your team size, compliance needs, and topology preference -- get back infrastructure sizing, security checklists, YAML configs, and a phased rollout plan.

**Headline result:** Plans a 75-developer hybrid deployment in under 1 second -- outputs GPU server counts, Dell PowerEdge model selection, storage sizing, cost estimates ($61K-$315K range), and an 11-item security hardening checklist tailored to SOC 2 + HIPAA.

- [HOW_TO_USE.md](HOW_TO_USE.md) -- Installation and first-run instructions
- [TECH_DETAILS.md](TECH_DETAILS.md) -- Architecture, data flow, limitations

## Quick start

```bash
bash run.sh
```

## Source

Based on: [OpenAI and Dell partner to bring Codex to hybrid and on-premise enterprise environments](https://openai.com/index/dell-codex-enterprise-partnership)
