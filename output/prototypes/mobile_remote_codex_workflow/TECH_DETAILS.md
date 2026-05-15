# Technical Details

## What This Does

This prototype simulates the full lifecycle of OpenAI's Codex remote coding workflow — the same flow available in the ChatGPT mobile app. It models task creation, real-time progress tracking, mid-task steering (sending instructions to the agent while it works), diff generation, and approval/rejection from any device. The implementation uses no external APIs, making it runnable anywhere for evaluation purposes.

The core insight from OpenAI's announcement: Codex tasks run asynchronously in a cloud sandbox, and the ChatGPT app on mobile becomes a monitoring/steering/approval interface. You don't need your laptop open to manage AI-generated code changes.

## Architecture

### Key Files

| File | Purpose |
|------|---------|
| `codex_workflow.py` | Core implementation — `CodexWorkflowManager` class with full lifecycle |
| `run.sh` | Entry point for demo execution |
| `requirements.txt` | Dependency declaration (stdlib only) |

### Data Flow

```
Mobile Device (ChatGPT App)
    │
    ├── create_task() ──→ Task queued in Codex cloud
    │
    ├── simulate_progress() ──→ Real-time status updates pushed to device
    │
    ├── steer_task() ──→ Mid-flight instructions sent to agent
    │
    ├── generate_mock_diffs() ──→ File-level diffs rendered for review
    │
    └── review_task() ──→ Approve/reject → PR created or revision requested
```

### Key Classes

- **`CodexWorkflowManager`** — Orchestrates the full workflow; tracks tasks, devices, and session state
- **`CodingTask`** — Represents a single Codex coding task with status, diffs, and steering history
- **`CodeDiff`** — Structured representation of file-level changes
- **`SteeringEvent`** — Records mid-task instructions with device attribution

### Dependencies

- Python 3.10+ standard library only (`dataclasses`, `json`, `enum`, `hashlib`, `datetime`)
- No external packages, no API keys

## Limitations

- **Mock only** — Does not connect to the real Codex API (which requires an OpenAI account with Codex access)
- **No real-time push** — Simulates progress synchronously; real Codex uses WebSocket/push notifications
- **No auth** — No OAuth flow; real implementation requires OpenAI account linking
- **Single-process** — Doesn't demonstrate actual cross-device sync (would need a backend)
- **No git integration** — Diffs are generated, not actually applied to a repo

## What It Does NOT Do

- Execute real code or run tests
- Connect to GitHub/GitLab for actual PR creation
- Provide a mobile UI (it's a CLI demonstration of the workflow patterns)
- Handle concurrent multi-user scenarios

## Why This Matters for Claude-Driven Products

| Domain | Relevance |
|--------|-----------|
| **Agent Factories** | Pattern for monitoring/steering any AI agent remotely — applicable to Claude Code workflows, not just Codex |
| **Lead-Gen / Marketing** | Mobile approval workflows let marketing teams approve AI-generated content (ads, copy, landing pages) on the go |
| **Voice AI** | Same steering pattern works for voice: "Hey Claude, approve the PR from task ctx_a1b2" |
| **Ad Creatives** | Creative teams can steer AI-generated ad variations from mobile, approve winning variants without opening laptops |

### Competitive Signal

OpenAI shipping mobile-first Codex access signals that **async AI agent management from mobile** is becoming table stakes. Teams building Claude-native tools should consider:

1. Mobile-friendly approval UIs for agent outputs
2. Push notification hooks when agents need human input
3. Lightweight steering interfaces (not full IDEs) for mid-task guidance
4. Cross-device session continuity as a first-class feature
