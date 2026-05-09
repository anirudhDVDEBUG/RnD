---
name: local_security_agent_kali
description: |
  Set up an autonomous security testing agent on Kali Linux using a local Qwen 2.5-7B model via LM Studio. Scaffolds the Python project structure, agent loop, and tool integrations for local-inference cybersecurity workflows.
  Trigger: user wants to build a local AI security agent, run autonomous pentesting with a local LLM, set up Qwen on Kali for security tasks, or create an offline cybersecurity agent.
---

# Local Security Agent on Kali Linux

Scaffold and run an autonomous security-testing agent powered by a locally-hosted Qwen 2.5-7B model served through LM Studio, designed for Kali Linux environments.

## When to use

- "Set up a local AI agent for security testing on Kali"
- "Build an autonomous pentesting agent using a local LLM"
- "Run Qwen 2.5 locally for cybersecurity automation"
- "Create an offline security agent that doesn't need cloud APIs"
- "Scaffold a Python agent loop that calls local model inference for recon and enumeration"

## How to use

### Prerequisites

1. **Kali Linux** (or a Debian-based distro with security tools installed).
2. **LM Studio** installed and running, serving **Qwen 2.5-7B** (or compatible) on a local HTTP endpoint (default `http://localhost:1234/v1`).
3. **Python 3.10+** with `pip`.

### Step 1 — Project structure

Create the following layout:

```
local-security-agent/
├── agent.py            # Main agent loop
├── tools/
│   ├── __init__.py
│   ├── recon.py        # Nmap, whois, DNS enumeration wrappers
│   ├── web.py          # Nikto, directory brute-force helpers
│   └── exploit.py      # Searchsploit / Metasploit RPC helpers
├── llm_client.py       # OpenAI-compatible client pointed at LM Studio
├── config.py           # Endpoint URL, model name, temperature, etc.
├── requirements.txt
└── README.md
```

### Step 2 — LLM client (`llm_client.py`)

Use the OpenAI-compatible API that LM Studio exposes:

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",  # LM Studio accepts any key
)

def ask(prompt: str, system: str = "You are a cybersecurity assistant.") -> str:
    response = client.chat.completions.create(
        model="qwen2.5-7b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content
```

### Step 3 — Tool wrappers (`tools/recon.py` example)

Wrap Kali tools so the agent can invoke them programmatically:

```python
import subprocess
import shlex

def nmap_scan(target: str, flags: str = "-sV -sC") -> str:
    """Run an nmap scan and return stdout."""
    cmd = f"nmap {flags} {shlex.quote(target)}"
    result = subprocess.run(
        shlex.split(cmd),
        capture_output=True, text=True, timeout=300,
    )
    return result.stdout
```

> **Authorization check**: Only run against targets you have explicit written permission to test.

### Step 4 — Agent loop (`agent.py`)

Implement a plan-act-observe cycle:

```python
from llm_client import ask
from tools import recon, web

TOOL_MAP = {
    "nmap_scan": recon.nmap_scan,
    "nikto_scan": web.nikto_scan,
}

def run_agent(objective: str, target: str):
    history = []
    for step in range(10):  # cap iterations
        prompt = build_prompt(objective, target, history)
        response = ask(prompt)
        action, args = parse_action(response)
        if action == "DONE":
            break
        if action in TOOL_MAP:
            observation = TOOL_MAP[action](**args)
            history.append({"action": action, "result": observation})
    return history
```

### Step 5 — Install and run

```bash
pip install openai
# Start LM Studio and load Qwen 2.5-7B
python agent.py --target 192.168.1.100 --objective "enumerate open services"
```

### Key considerations

- **Authorization**: Only use against systems you own or have explicit authorization to test. This is for legitimate pentesting, CTFs, and security research.
- **Resource usage**: Qwen 2.5-7B needs ~6 GB VRAM. Use quantized (Q4/Q5) GGUF for lower-end GPUs.
- **Offline capability**: Entire pipeline runs locally — no data leaves your machine.
- **Extensibility**: Add new tools by creating wrapper functions in `tools/` and registering them in `TOOL_MAP`.

## References

- Source repository: https://github.com/XenoCoreGiger31/Local-Model
- LM Studio: https://lmstudio.ai
- Qwen 2.5 models: https://huggingface.co/Qwen
