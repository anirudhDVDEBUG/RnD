# How to Use

## Quick start (mock demo — no dependencies beyond Python)

```bash
git clone <this-repo> && cd local_security_agent_kali
bash run.sh          # runs in MOCK_MODE, no LM Studio needed
```

## Full setup (real scanning)

### Prerequisites

| Requirement | Notes |
|---|---|
| Kali Linux (or Debian + security tools) | nmap, nikto, searchsploit must be on PATH |
| LM Studio | Download from https://lmstudio.ai |
| Qwen 2.5-7B GGUF | Load in LM Studio; ~6 GB VRAM (Q4 quantized) |
| Python 3.10+ | With pip |

### Install

```bash
pip install -r requirements.txt   # installs: openai
```

### Configure LM Studio

1. Open LM Studio, download **Qwen 2.5-7B** (or any compatible model).
2. Start the local server (default: `http://localhost:1234/v1`).
3. Verify: `curl http://localhost:1234/v1/models` should return a model list.

### Run against a real target

```bash
# Unset mock mode (default is off; run.sh sets it on for demo)
export MOCK_MODE=0

python3 agent.py \
    --target 192.168.1.100 \
    --objective "enumerate open services and check for known vulnerabilities"
```

Only scan targets you have explicit written authorization to test.

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `LLM_BASE_URL` | `http://localhost:1234/v1` | LM Studio endpoint |
| `LLM_MODEL` | `qwen2.5-7b` | Model name in LM Studio |
| `LLM_TEMPERATURE` | `0.3` | Sampling temperature |
| `MAX_STEPS` | `10` | Max agent iterations |
| `MOCK_MODE` | `0` | Set to `1` for demo without LM Studio |

## Using as a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/local_security_agent_kali
cp SKILL.md ~/.claude/skills/local_security_agent_kali/SKILL.md
```

**Trigger phrases:**
- "Set up a local AI agent for security testing on Kali"
- "Build an autonomous pentesting agent using a local LLM"
- "Run Qwen 2.5 locally for cybersecurity automation"
- "Create an offline security agent that doesn't need cloud APIs"

## First 60 seconds

```
$ bash run.sh

=== Local Security Agent — Demo ===

============================================================
  LOCAL SECURITY AGENT
  Objective : enumerate open services and check for known vulnerabilities
  Target    : 192.168.1.100
  Model     : qwen2.5-7b
  Mock mode : ON
============================================================

[Step 1] Querying LLM for next action...
  -> Running: nmap_scan(target='192.168.1.100', flags='-sV -sC -T4')
  Result:
    Starting Nmap 7.94 ( https://nmap.org )
    Nmap scan report for 192.168.1.100
    PORT     STATE SERVICE  VERSION
    22/tcp   open  ssh      OpenSSH 8.9p1 Ubuntu
    80/tcp   open  http     Apache httpd 2.4.49
    3306/tcp open  mysql    MySQL 8.0.28

[Step 2] Querying LLM for next action...
  -> Running: nikto_scan(target='192.168.1.100', port='80')
  Result:
    - Nikto v2.5.0
    + Server: Apache/2.4.49 (Ubuntu)
    + /server-status: Apache server-status enabled.

[Step 3] Querying LLM for next action...
  -> Running: searchsploit(query='Apache 2.4.49')
  Result:
    Apache HTTP Server 2.4.49 - Path Traversal  | multiple/webapps/50383.sh
    Apache 2.4.49/50 - RCE (CVE-2021-41773)     | multiple/webapps/50406.py

============================================================
  AGENT COMPLETE
============================================================

Summary:
Target 192.168.1.100 has 3 open ports (22/ssh, 80/http, 3306/mysql).
Web server Apache 2.4.49 is vulnerable to CVE-2021-41773 path traversal.
Recommend patching Apache immediately and restricting MySQL bind address.
```
