# How to Use

## Install

```bash
git clone <this-repo>
cd windows_sandbox_coding_agent
pip install -r requirements.txt   # no external deps, stdlib only
```

## Quick Run

```bash
bash run.sh
```

No API keys, no Docker, no Windows required. The demo runs a simulated sandbox on any OS with Python 3.10+.

## First 60 Seconds

**Input:** `bash run.sh`

**Output (abbreviated):**

```
=== Windows Sandbox Coding Agent Demo ===

============================================================
  1. Sandbox Configuration
============================================================
{
  "workspace_host": "/tmp/sandbox_agent_demo_...",
  "network_enabled": false,
  "safety": {
    "allowed_extensions": [".py", ".js", ".md", ".json", ".txt", ".html"],
    "blocked_patterns": [".env", "secrets.*", "*.pem", "*.key"],
    ...
  }
}

============================================================
  3. Execute: Multi-Step Coding Task (ALLOWED)
============================================================
Status: success
Files changed: ['app.py', 'tests/test_app.py']
Output:
[Step 1] success: Wrote 124 bytes to app.py
[Step 2] success: Wrote 183 bytes to tests/test_app.py
[Step 3] success: Hello, World!
[Step 4] success: All tests passed.

============================================================
  5. Rejected: Write to .env File
============================================================
Status: rejected
Reason: FAIL:
  - Blocked path pattern '.env' matched: .env

============================================================
  6. Rejected: Path Traversal Attack
============================================================
Status: rejected
Reason: Path traversal blocked: ../../etc/passwd
```

## Using as a Library

```python
from sandbox_agent.config import SandboxConfig, SafetyRules, NetworkPolicy
from sandbox_agent.executor import SandboxExecutor

config = SandboxConfig(
    workspace_host="/path/to/project",
    safety=SafetyRules(allowed_extensions=[".py", ".md"]),
    network=NetworkPolicy(enabled=False),
)

executor = SandboxExecutor(config)

result = executor.execute_task({
    "type": "write_file",
    "path": "hello.py",
    "content": "print('hello')\n",
})
print(result.status)  # "success"
```

## Generating a Real Windows Sandbox Config

```python
executor.generate_wsb_file("my-sandbox.wsb")
# Double-click the .wsb file on Windows Pro/Enterprise to launch
```

The generated `.wsb` file maps your project folder into the sandbox with networking disabled. Enable Windows Sandbox first:

```powershell
Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -Online
```

## As a Claude Code Skill

Drop the `SKILL.md` file into `~/.claude/skills/windows_sandbox_coding_agent/SKILL.md`.

**Trigger phrases:**
- "Set up a secure sandbox for running AI-generated code on Windows"
- "Build an isolated execution environment for a coding agent"
- "Create a safe code runner with file access controls"

## Project Structure

```
windows_sandbox_coding_agent/
  sandbox_agent/
    __init__.py
    config.py       # SandboxConfig, SafetyRules, NetworkPolicy
    validator.py    # File change validation engine
    executor.py     # Task execution with safety enforcement
  demo.py           # End-to-end demo script
  run.sh            # One-command runner
  requirements.txt  # (stdlib only)
```
