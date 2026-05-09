# How to Use

## Install

```bash
git clone <this-repo>
cd safe_coding_agent_sandbox
# No pip install needed -- stdlib only
```

Requires Python 3.10+.

## Run the Demo

```bash
bash run.sh
```

Produces a full security audit of a simulated coding agent session: sandbox config, network policies, approval decisions, secret scan results, policy violations, and telemetry.

## Use as a Claude Skill

Drop the skill file into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/safe_coding_agent_sandbox
cp SKILL.md ~/.claude/skills/safe_coding_agent_sandbox/SKILL.md
```

### Trigger Phrases

- "Set up a sandbox for a coding agent"
- "How do I run a coding agent safely in production?"
- "Design network policies and isolation for an AI code assistant"
- "Add approval workflows before an agent can execute code"
- "Implement telemetry and audit logging for agent actions"

## Use as a Library

Import the modules directly in your own agent framework:

```python
from sandbox import (
    AgentTelemetry,
    ApprovalGate,
    scan_for_secrets,
    enforce_policies,
    generate_docker_compose,
    generate_k8s_network_policy,
    generate_seccomp_profile,
)

# 1. Set up telemetry
telemetry = AgentTelemetry()

# 2. Create approval gate
gate = ApprovalGate(telemetry, auto_approve_medium=True)

# 3. Check an action before executing
result = gate.check("git_push", {"branch": "main", "commits": 1})
if result.decision.value in ("approved", "auto_approved"):
    # proceed with push
    pass

# 4. Scan agent-generated code
secrets = scan_for_secrets(agent_output)
violations = enforce_policies(agent_output)

if secrets or violations:
    # block the output
    pass

# 5. Generate infra configs
docker_cfg = generate_docker_compose(cpus="4.0", memory="8G")
k8s_policy = generate_k8s_network_policy(allowed_cidrs=["10.0.0.0/8"])
seccomp = generate_seccomp_profile()
```

## First 60 Seconds

```
$ bash run.sh

  ╔═══════════════════════════════════════════════════════════╗
  ║       SAFE CODING AGENT SANDBOX - Security Demo          ║
  ╚═══════════════════════════════════════════════════════════╝

================================================================
  1. SANDBOX ISOLATION CONFIG
================================================================

  [PASS] Read-only filesystem
  [PASS] No new privileges
  [PASS] Seccomp profile
  ...

================================================================
  3. APPROVAL WORKFLOW
================================================================

  [AUTO] low       read_file          {"path": "src/main.py"}
  [DENY] critical  modify_ci          {"file": ".github/workflows/deploy.yml"}
  [WARN] Anomaly: sensitive_path_access - /etc/shadow
  ...

================================================================
  5. POLICY ENFORCEMENT
================================================================

  [FAIL] Found 7 policy violation(s)!
    [high  ] Line 11 | no_subprocess_shell   | subprocess with shell=True
    [high  ] Line 14 | no_eval               | eval() detected
  ...

All security layers operational.
```

No API keys needed. Everything runs locally with mock data.
