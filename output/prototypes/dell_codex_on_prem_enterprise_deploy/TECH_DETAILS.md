# Technical Details

## What it does

This prototype implements a deployment planning engine for the Dell-OpenAI Codex enterprise partnership. Given enterprise constraints (team size, compliance frameworks, topology preference, air-gap requirements), it calculates GPU infrastructure sizing using Dell's PowerEdge server catalog, generates a production-ready YAML configuration, produces a severity-ranked security hardening checklist, and outputs a phased rollout plan. It also supports multi-scenario comparison for side-by-side evaluation of different deployment topologies.

The tool codifies the architectural guidance from the Dell-OpenAI partnership announcement into a deterministic, repeatable planning process -- turning what would normally be weeks of solution architecture into a structured output.

## Architecture

### Key files

| File | Purpose |
|------|---------|
| `codex_deploy_planner.py` | Core engine: sizing calculator, config generator, security checklist, rollout planner |
| `SKILL.md` | Claude Code skill definition with trigger phrases and step-by-step guidance |
| `run.sh` | Entry point -- runs the planner with default scenarios |

### Data flow

```
EnterpriseRequirements (dataclass)
  |
  +---> compute_sizing() ---> InfraRecommendation
  |       - Maps developer count to concurrent sessions
  |       - Selects Dell PowerEdge model (R760xa for <60 sessions, XE9680 for larger)
  |       - Calculates GPU count at ~12 sessions/GPU
  |       - Sizes storage (PowerScale for repos, ECS for models)
  |
  +---> generate_security_checklist() ---> [{check, description, severity, status}]
  |       - 9 base checks (TLS, SSO, egress, audit, etc.)
  |       - Adds air-gap verification if air_gapped=True
  |       - Adds per-framework compliance checks
  |
  +---> generate_config_yaml() ---> YAML string
  |       - Deployment mode, inference routing, security block
  |       - Scaling parameters, monitoring endpoints
  |
  +---> generate_rollout_plan() ---> [{phase, name, duration, scope, goals}]
          - 3-phase: Pilot -> Department -> Enterprise-Wide
```

### Dependencies

- **Python 3.8+** (stdlib only: `dataclasses`, `json`, `math`, `enum`, `typing`)
- No external packages, no API keys, no network calls

### Model calls

None. This is a deterministic planning tool, not an inference engine. The SKILL.md is designed to guide Claude Code's responses when a user asks about Codex deployment -- Claude uses the skill's instructions to structure its advice, not to call any external model.

## Limitations

- **Sizing is approximate.** GPU-per-session ratios (~12 sessions/GPU) are estimates based on typical LLM inference workloads. Actual capacity depends on model size, context length, and workload patterns.
- **No real Dell API integration.** Server specs and pricing are hardcoded from public catalog data. A production tool would integrate with Dell's Configure-to-Order API.
- **No Codex API.** OpenAI's on-prem Codex product is not yet generally available. The config YAML represents the expected configuration surface based on the partnership announcement.
- **No network topology generation.** The tool recommends network segmentation but does not generate firewall rules, VLAN configs, or switch configurations.
- **Single-region only.** Multi-region or multi-site deployments require manual planning beyond what this tool provides.

## Why it matters for Claude-driven products

- **Agent factories:** Teams building agent orchestration platforms can use this pattern (requirements -> sizing -> config -> checklist -> rollout) to create deployment planners for any on-prem AI workload, not just Codex. The SKILL.md structure shows how to encode domain expertise as a Claude Code skill.
- **Enterprise sales / lead-gen:** The scenario comparison output is designed to be drop-in for enterprise sales decks -- showing prospects exactly what infrastructure they need and what it costs, personalized to their constraints.
- **Compliance automation:** The security checklist generation pattern (base checks + conditional checks per framework) is reusable for any compliance-aware deployment tool. Plug in different frameworks (HIPAA, FedRAMP, PCI-DSS) and get tailored checklists.
- **On-prem AI infrastructure:** As more enterprises demand data sovereignty for AI workloads, tools that plan Dell/NVIDIA on-prem deployments will become a recurring need across coding agents, RAG systems, and fine-tuning pipelines.
