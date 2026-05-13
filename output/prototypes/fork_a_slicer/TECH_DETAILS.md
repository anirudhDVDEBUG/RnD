# Technical Details: Fork-a-Slicer

## What It Does

Fork-a-Slicer is an AI-agent-driven workflow repository that provides phased, step-by-step plans for forking OrcaSlicer (an open-source 3D printing slicer descended from BambuStudio/PrusaSlicer) and re-adding Bambu Lab printer support through a process isolation bridge. The plans are designed to be fed to AI coding agents (Claude Code, Gemini CLI) who then execute each step interactively with the developer.

The core architectural idea is the **FULU-Foundation pattern**: instead of embedding Bambu Lab's proprietary communication protocol directly into the slicer binary, a separate bridge process handles all Bambu Connect protocol interactions. The slicer and bridge communicate over JSON-RPC 2.0 via a Unix domain socket. This provides legal separation (no proprietary code in the GPL-licensed slicer), stability (bridge crashes don't take down the slicer), and maintainability (bridge can be updated independently).

## Architecture

### Data Flow

```
┌─────────────────────┐    JSON-RPC 2.0     ┌─────────────────────┐
│                     │   Unix Domain Sock   │                     │
│   OrcaSlicer Fork   │ ◄─────────────────► │  Bambu Connect      │
│   (slicer_client)   │                      │  Bridge             │
│                     │  discover_printers   │  (bambu_bridge)     │
│   - Slicing engine  │  get_printer_status  │                     │
│   - UI / Preview    │  submit_print_job    │  - mDNS/SSDP disc.  │
│   - G-code gen      │  get_bridge_info     │  - Bambu protocol   │
│                     │                      │  - Auth / TLS       │
└─────────────────────┘                      └─────────────────────┘
      Process A (PID X)                           Process B (PID Y)
```

### Key Files

| File | Role |
|---|---|
| `bambu_bridge.py` | Standalone JSON-RPC server. Binds to `/tmp/bambu_bridge.sock`, handles 4 RPC methods. Simulates 3 Bambu printers with realistic state (temps, firmware, filament, print progress). |
| `slicer_client.py` | Slicer-side client. Connects to the bridge socket and walks through discovery, status, job submission, and error handling. |
| `demo.py` | Orchestrator. Spawns bridge as `subprocess.Popen`, waits for socket readiness, runs client, then cleans up. Proves true process isolation (different PIDs). |

### Dependencies

**Zero external dependencies.** Uses only Python 3.8+ stdlib:
- `socket` — Unix domain socket IPC
- `json` — JSON-RPC serialization
- `subprocess` — process isolation
- `os`, `sys`, `time`, `random`, `signal`, `threading`

### Protocol

Standard JSON-RPC 2.0 over Unix domain sockets. Four methods:

| Method | Params | Returns |
|---|---|---|
| `discover_printers` | none | List of printers with id, name, model, IP |
| `get_printer_status` | `printer_id` | Full status: temps, filament, print progress |
| `submit_print_job` | `printer_id`, `gcode_file` | Job ID, status, estimated time |
| `get_bridge_info` | none | Version, architecture, supported methods |

## Limitations

- **Mock data only** — no actual Bambu Connect protocol implementation. Real Bambu printers are not contacted.
- **Linux/macOS only** — uses Unix domain sockets (`AF_UNIX`), which are not natively available on older Windows versions.
- **Single-threaded bridge** — the demo bridge handles one RPC call at a time. A production bridge would need async I/O or threading.
- **No authentication** — the real Bambu Connect protocol requires TLS and device-level authentication. Not implemented here.
- **No actual slicer integration** — this demonstrates the bridge pattern, not a working OrcaSlicer fork. Building the actual fork requires the full plan set from the source repo.
- **Plans are Linux/ARM64 focused** — the source repo targets ARM64 Linux builds specifically.

## Why This Matters for Claude-Driven Products

**Agent Factories / AI-Agent Workflows:** Fork-a-Slicer is a reference example of "plans as code" — structured step-by-step instructions designed for AI agents to execute. This pattern is directly applicable to building agent factories that can follow complex multi-step engineering plans. If you're building systems where Claude agents execute build/deploy/configure workflows, this shows how to structure those plans.

**Process Isolation as an Architecture Pattern:** The bridge pattern demonstrated here — separate processes communicating via JSON-RPC — is the same pattern used in MCP servers, Claude tool servers, and sandboxed code execution. Understanding this architecture helps when building Claude-driven products that need to isolate untrusted code, third-party APIs, or stateful services behind clean RPC boundaries.

**Hardware/IoT Integration:** For anyone building Claude-driven products that interact with physical devices (3D printers, CNC machines, IoT devices), this demonstrates a clean architecture for bridging AI-generated commands to hardware protocols without tight coupling.

## References

- Source: [danielcherubini/fork-a-slicer](https://github.com/danielcherubini/fork-a-slicer)
- Topics: 3d-printing, ai-agent, arm64, bambu-connect, bambu-lab, bridge, claude-code, gemini-cli, interoperability, json-rpc, linux, open-source, orcaslicer, printer-networking, process-isolation, reverse-engineering
