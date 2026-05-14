# Technical Details

## What It Does

This prototype implements the safety and configuration layer for running AI coding agents inside Windows Sandbox. It provides: (1) a declarative config system that generates `.wsb` sandbox definition files with folder mappings and network restrictions, (2) a file-change validator that enforces extension allowlists, blocked-path patterns, size limits, and file-count caps, (3) a task executor that runs write and command operations with path-traversal guards and dangerous-command blocking.

The design follows the approach described in OpenAI's "Building a safe, effective sandbox to enable Codex on Windows" — using Windows Sandbox's disposable VM isolation to let AI agents edit code without risk to the host system, while layering application-level guardrails on top for defense-in-depth.

## Architecture

```
                  ┌─────────────────────┐
                  │   Task (JSON)       │
                  │  type: write_file   │
                  │  path: app.py       │
                  │  content: ...       │
                  └────────┬────────────┘
                           │
                  ┌────────▼────────────┐
                  │   SandboxExecutor   │
                  │                     │
                  │  ┌───────────────┐  │
                  │  │  Validator    │  │  ← extension, pattern, size, count checks
                  │  └───────┬───────┘  │
                  │          │ pass?    │
                  │  ┌───────▼───────┐  │
                  │  │ Path Traversal│  │  ← resolve + relative_to guard
                  │  └───────┬───────┘  │
                  │          │ pass?    │
                  │  ┌───────▼───────┐  │
                  │  │ Execute       │  │  ← write file / run command
                  │  └───────────────┘  │
                  └─────────────────────┘
                           │
                  ┌────────▼────────────┐
                  │   TaskResult        │
                  │  status, output,    │
                  │  files_changed,     │
                  │  validation         │
                  └─────────────────────┘
```

### Key Files

| File | Purpose |
|------|---------|
| `sandbox_agent/config.py` | `SandboxConfig`, `SafetyRules`, `NetworkPolicy`, `FolderMapping` dataclasses; `.wsb` XML generation |
| `sandbox_agent/validator.py` | `validate_changes()` — checks file lists against rules, returns `ValidationResult` |
| `sandbox_agent/executor.py` | `SandboxExecutor` — orchestrates task execution with pre-validation, path guards, command blocking |
| `demo.py` | End-to-end demonstration: config, execution, rejection scenarios |

### Data Flow

1. **Config** defines what the sandbox allows (extensions, paths, network, timeouts)
2. **Task** arrives as a JSON dict (`write_file`, `run_command`, or `multi_step`)
3. **Validator** checks proposed changes against safety rules before execution
4. **Executor** enforces path-traversal guards and command blocklists
5. **Result** includes status, changed files, output, and validation details
6. On Windows, `generate_wsb_file()` produces a `.wsb` XML config for real sandbox launch

### Dependencies

- **Python 3.10+** (stdlib only — `json`, `subprocess`, `xml.etree`, `pathlib`, `dataclasses`, `fnmatch`, `tempfile`)
- No external packages required
- On Windows: Windows Sandbox feature (Pro/Enterprise) for actual VM isolation

## Limitations

- **Simulation only on non-Windows**: The executor runs commands directly in a temp directory, not in true VM isolation. Real isolation requires Windows Sandbox or Hyper-V.
- **No actual Windows Sandbox launch**: `WindowsSandbox.exe` integration is config-generation only; launching requires Windows with the feature enabled.
- **Command blocklist is pattern-based**: A determined attacker could bypass the simple string-matching blocklist. In production, use OS-level restrictions (AppContainers, seccomp, etc.).
- **No persistent sandbox state**: Each task starts fresh. There's no mechanism for multi-turn sandbox sessions with accumulated state.
- **No LLM integration**: This is the sandbox harness, not the AI agent itself. It's designed to be called by an agent (Claude, GPT, etc.) as an execution backend.

## Why It Matters

For teams building Claude-driven products:

- **Agent factories**: Any system that spawns coding agents needs a safety boundary. This provides the template — config-driven isolation with defense-in-depth validation. Plug your agent's output into `SandboxExecutor.execute_task()` and get safety guarantees without building from scratch.
- **Enterprise deployment**: Windows is the dominant enterprise desktop. Running AI coding agents on Windows requires Windows-native sandboxing (not just Docker). The `.wsb` config generation bridges that gap.
- **Compliance / security audits**: The validator produces structured `ValidationResult` objects with explicit violation lists — useful for audit trails when AI agents modify production codebases.
- **Ad-creative and marketing automation**: Agents generating HTML/CSS/JS for ad creatives can run in sandboxes to prevent injection attacks or accidental data access, while still producing reviewable output.
