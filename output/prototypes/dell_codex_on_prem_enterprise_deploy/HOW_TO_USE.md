# How to Use

## This is a Claude Code SKILL

### Install the skill

Copy the `SKILL.md` file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/dell-codex-on-prem-deploy
cp SKILL.md ~/.claude/skills/dell-codex-on-prem-deploy/SKILL.md
```

### Trigger phrases

Once installed, these prompts will activate the skill in Claude Code:

- "Help me plan an on-premise Codex deployment for our enterprise"
- "Set up a hybrid AI coding agent environment with Dell infrastructure"
- "What do I need to deploy Codex securely on-prem?"
- "Design an architecture for enterprise Codex with data residency requirements"
- "Evaluate whether hybrid or fully on-premise Codex fits our compliance needs"

### What the skill does inside Claude Code

When triggered, Claude will walk you through:
1. Assessing data residency, security, scale, and compliance requirements
2. Selecting a deployment topology (fully on-prem, hybrid, or edge+cloud)
3. Recommending Dell PowerEdge server models and storage systems
4. Generating a `codex-enterprise-config.yaml`
5. Producing a security hardening checklist
6. Creating a phased rollout plan

---

## Standalone demo (no Claude Code needed)

### Prerequisites

- Python 3.8+
- No external packages required (stdlib only)

### Install

```bash
git clone <this-repo>
cd dell_codex_on_prem_enterprise_deploy
```

### Run

```bash
bash run.sh
```

### First 60 seconds

**Input:** `bash run.sh` (no arguments needed -- uses a realistic 75-developer hybrid scenario)

**Output (abbreviated):**

```
========================================================================
  DELL CODEX ON-PREM ENTERPRISE DEPLOYMENT PLAN
========================================================================

>> ENTERPRISE REQUIREMENTS
   Developers:           75
   Topology:             hybrid
   Compliance:           SOC 2, HIPAA

>> INFRASTRUCTURE SIZING
   Concurrent sessions:  27
   Total GPUs needed:    4
   GPU servers:          1x Dell PowerEdge R760xa (4x NVIDIA H100 each)
   Management nodes:     2x Dell PowerEdge R760
   Code storage:         30 TB (Dell PowerScale)
   Model/artifact store: 50 TB (Dell ECS)
   Est. cost range:      $61,000 - $315,000
   Notes:
     - Hybrid mode: configure cloud fallback for inference overflow

>> SECURITY HARDENING CHECKLIST
   [ ] [CRITICAL] TLS everywhere: Enable TLS for all inter-service communication
   [ ] [CRITICAL] SSO integration: Configure SAML SSO with enterprise identity provider
   [ ] [CRITICAL] Code egress policy: Set code egress policies to DENY ...
   ...11 total checks including SOC 2 + HIPAA compliance items

>> GENERATED CONFIG (codex-enterprise-config.yaml)
   deployment:
     mode: hybrid
     inference:
       primary: on-prem
       fallback: cloud
   ...

>> PHASED ROLLOUT PLAN
   Phase 1: Pilot (2-3 weeks)
   Phase 2: Department Rollout (4-6 weeks)
   Phase 3: Enterprise-Wide (Ongoing)

========================================================================
  SCENARIO COMPARISON
========================================================================

  Scenario                                       Devs  GPUs  Sessions  Cost Range
  Mid-size hybrid (50 devs, SOC 2)                 50     4        15  $61,000 - $315,000
  Large air-gapped (200 devs, FedRAMP + ITAR)     200     8        60  $106,000 - $630,000
  Small edge+cloud (15 devs, GDPR)                 15     4         5  $61,000 - $315,000
```

### Save config files

```bash
python3 codex_deploy_planner.py --save
# Creates: codex-enterprise-config.yaml, deployment-report.json
```
