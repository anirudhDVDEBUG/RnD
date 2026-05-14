---
name: windows_sandbox_coding_agent
description: |
  Build a secure, sandboxed execution environment for coding agents on Windows.
  Uses Windows Sandbox or Hyper-V isolation to safely run AI-generated code with
  controlled file access and network restrictions.
  Triggers: windows sandbox, secure code execution, sandboxed coding agent,
  isolated dev environment, safe code runner
---

# Windows Sandbox Coding Agent

Build a secure, isolated sandbox environment on Windows for running AI coding agents safely — with controlled file system access, network restrictions, and deterministic execution.

## When to use

- "Set up a secure sandbox for running AI-generated code on Windows"
- "Build an isolated execution environment for a coding agent"
- "Create a safe code runner with file access controls and network restrictions"
- "Implement a Windows sandbox that lets an AI agent edit code safely"
- "Design a sandboxed dev environment for automated coding tasks"

## How to use

### 1. Choose Your Isolation Strategy

Select the appropriate Windows isolation mechanism:

- **Windows Sandbox** (`WindowsSandbox.exe`): Lightweight, disposable desktop environment. Good for quick, ephemeral tasks. Requires Windows Pro/Enterprise with the Windows Sandbox feature enabled.
- **Hyper-V Containers / VMs**: Stronger isolation with kernel-level separation. Better for production-grade sandboxing.
- **AppContainers / Restricted Tokens**: Process-level isolation using Windows security primitives. Lower overhead but less isolated.

```powershell
# Enable Windows Sandbox feature
Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -Online -NoRestart
```

### 2. Configure File Access Controls

Map only the necessary project files into the sandbox using read/write or read-only folder mappings:

```xml
<!-- sandbox-config.wsb -->
<Configuration>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>C:\Projects\my-repo</HostFolder>
      <SandboxFolder>C:\Users\WDAGUtilityAccount\workspace</SandboxFolder>
      <ReadOnly>false</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>C:\Tools\approved-tools</HostFolder>
      <SandboxFolder>C:\Tools</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
</Configuration>
```

**Key principles:**
- Mount the project workspace as read-write so the agent can modify code
- Mount toolchains (compilers, interpreters, linters) as read-only
- Never mount the full host filesystem — only the minimum required directories
- Use a staging directory to review agent outputs before promoting to the host

### 3. Restrict Network Access

Disable or heavily restrict network access to prevent data exfiltration and supply chain attacks:

```xml
<Configuration>
  <Networking>Disable</Networking>
  <!-- Or use firewall rules for selective access -->
</Configuration>
```

For cases where the agent needs limited network (e.g., package installs):

```powershell
# Allow only specific endpoints via Windows Firewall inside the sandbox
New-NetFirewallRule -DisplayName "Allow PyPI" -Direction Outbound `
  -RemoteAddress 151.101.0.0/16 -Action Allow
New-NetFirewallRule -DisplayName "Block All Other" -Direction Outbound `
  -Action Block
```

**Best practice:** Pre-install all dependencies into the sandbox image so the agent runs fully offline. This eliminates network-based attack vectors entirely.

### 4. Build the Agent Execution Harness

Create a harness that receives tasks, executes them inside the sandbox, and returns results:

```python
import subprocess
import json
import os
from pathlib import Path

class SandboxedCodeAgent:
    def __init__(self, workspace_dir: str, sandbox_config: str):
        self.workspace = Path(workspace_dir)
        self.config = sandbox_config
        self.results_dir = self.workspace / ".agent-results"
        self.results_dir.mkdir(exist_ok=True)

    def execute_task(self, task: dict) -> dict:
        """Run a coding task inside the Windows Sandbox."""
        # Write the task to a file the sandbox can read
        task_file = self.workspace / ".agent-task.json"
        task_file.write_text(json.dumps(task))

        # Launch the sandbox with the task
        result = subprocess.run(
            ["WindowsSandbox.exe", self.config],
            capture_output=True, timeout=300
        )

        # Read results written by the agent inside the sandbox
        result_file = self.results_dir / "result.json"
        if result_file.exists():
            return json.loads(result_file.read_text())
        return {"status": "error", "message": "No result produced"}

    def review_changes(self) -> list[str]:
        """List files modified by the agent for human review."""
        import subprocess
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=self.workspace, capture_output=True, text=True
        )
        return result.stdout.strip().split("\n")
```

### 5. Implement Safety Guardrails

Add layers of defense to prevent the agent from causing harm:

```python
SAFETY_RULES = {
    # Restrict which file types the agent can modify
    "allowed_extensions": [".py", ".js", ".ts", ".html", ".css", ".json",
                           ".md", ".yaml", ".yml", ".toml"],
    # Block modification of sensitive files
    "blocked_paths": [".env", "secrets.*", "*.pem", "*.key", ".git/"],
    # Max file size the agent can write (bytes)
    "max_file_size": 1_000_000,
    # Time limit per task (seconds)
    "timeout": 300,
    # Max number of files changed per task
    "max_files_changed": 20,
}

def validate_changes(workspace: Path, rules: dict) -> bool:
    """Validate agent changes against safety rules before accepting."""
    import subprocess, fnmatch
    result = subprocess.run(
        ["git", "diff", "--name-only"], cwd=workspace,
        capture_output=True, text=True
    )
    changed = result.stdout.strip().split("\n")

    if len(changed) > rules["max_files_changed"]:
        return False

    for f in changed:
        if any(fnmatch.fnmatch(f, p) for p in rules["blocked_paths"]):
            return False
        ext = Path(f).suffix
        if ext and ext not in rules["allowed_extensions"]:
            return False
        full = workspace / f
        if full.exists() and full.stat().st_size > rules["max_file_size"]:
            return False
    return True
```

### 6. Programmatic Sandbox Control (Advanced)

For tighter integration, use the Windows API to create AppContainer-based sandboxes programmatically:

```python
import ctypes
from ctypes import wintypes

def create_restricted_process(exe_path: str, working_dir: str):
    """Launch a process with restricted token and no network access."""
    # Use CreateRestrictedToken + CreateProcessAsUser
    # or leverage Job Objects for resource limits
    kernel32 = ctypes.windll.kernel32

    # Create a Job Object to limit resources
    job = kernel32.CreateJobObjectW(None, None)

    # Set memory and CPU limits
    # Set UI restrictions (no clipboard, no desktop access)
    # Assign the agent process to this job
    pass  # Implementation depends on specific requirements
```

### Architecture Overview

```
┌─────────────────────────────────────────┐
│              Host System                │
│  ┌──────────┐    ┌──────────────────┐   │
│  │ Agent    │    │  Review Gate     │   │
│  │ Harness  │───>│  (validate +     │   │
│  │          │    │   approve diffs) │   │
│  └────┬─────┘    └──────────────────┘   │
│       │                                  │
│  ┌────▼──────────────────────────────┐  │
│  │     Windows Sandbox / Hyper-V     │  │
│  │  ┌──────────┐  ┌──────────────┐   │  │
│  │  │ Mapped   │  │ Agent        │   │  │
│  │  │ Workspace│  │ Runtime      │   │  │
│  │  │ (R/W)    │  │ (Python/Node)│   │  │
│  │  └──────────┘  └──────────────┘   │  │
│  │  ┌──────────┐  ┌──────────────┐   │  │
│  │  │ Tools    │  │ No Network   │   │  │
│  │  │ (R/O)    │  │ (or filtered)│   │  │
│  │  └──────────┘  └──────────────┘   │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### Key Design Principles

1. **Least privilege**: The agent gets only the permissions it needs — specific folders, no network, no system access
2. **Ephemeral environments**: Each task runs in a fresh sandbox; no state leaks between tasks
3. **Human-in-the-loop**: All code changes pass through a review gate before being applied to the host
4. **Offline-first**: Pre-install dependencies to eliminate network dependency and supply chain risk
5. **Defense in depth**: Combine OS-level isolation (sandbox) with application-level guardrails (file type restrictions, size limits, change limits)

## References

- [Building a safe, effective sandbox to enable Codex on Windows – OpenAI](https://openai.com/index/building-codex-windows-sandbox)
- [Windows Sandbox documentation – Microsoft](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-overview)
- [Windows Sandbox configuration (.wsb files)](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file)
