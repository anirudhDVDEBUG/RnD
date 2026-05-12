# How to Use FRIDAY Cognitive AI OS

## Install

```bash
# Clone / copy this directory
cd friday_cognitive_ai_os

# No pip install needed for demo mode (stdlib only).
# For live Gemini reasoning + voice:
pip install google-generativeai speechrecognition pyttsx3
```

## As a Claude Skill

Drop the skill folder so Claude Code can trigger it:

```bash
cp -r friday_cognitive_ai_os ~/.claude/skills/friday_cognitive_ai_os/
```

The `SKILL.md` inside activates on trigger phrases like:
- "Build an autonomous AI assistant with memory and reasoning"
- "Create a local cognitive AI operating system like FRIDAY"
- "Set up a voice-controlled AI agent with cybersecurity tools"
- "Build a self-improving AI system with persistent memory"

Claude will scaffold the full FRIDAY project structure using the skill template.

## Run the Demo

```bash
bash run.sh
```

This runs in **mock mode** (no API key needed) and exercises all five subsystems: memory, reasoning, voice (text fallback), security scanning, and automation.

## Interactive Mode

```bash
python3 friday/main.py --interactive
```

Type queries at the `You >` prompt. Special commands:
- `reflect` -- FRIDAY reports on its own cognitive state
- `scan` -- scans localhost common ports
- `quit` -- exit

## Live Gemini Mode

```bash
export GEMINI_API_KEY="your-key-here"
python3 friday/main.py --interactive
```

When `GEMINI_API_KEY` is set, the cognitive engine sends prompts to Gemini Pro instead of using mock responses. Memory and context injection work identically.

## First 60 Seconds

```
$ bash run.sh

  _____ ____  ___ ____    _ __   __
 |  ___|  _ \|_ _|  _ \  / \\ \ / /
 | |_  | |_) || || | | |/ _ \\ V /
 |  _| |  _ < | || |_| / ___ \| |
 |_|   |_| \_\___|____/_/   \_\_|

  Autonomous Cognitive AI Operating System
  =========================================
  Mode: Mock (no API key)

[1/5] Initializing Memory System...
  Loaded 0 prior memories from friday/data/memory_store.json
[2/5] Starting Cognitive Engine...
[3/5] Running Reasoning Demo...

  You > How should I plan a new Python project with CI/CD?
  FRIDAY > Let me decompose this into actionable steps: 1) Define the
           objective clearly, 2) Identify required resources, 3) Execute
           in priority order, 4) Validate each milestone.

  You > What security measures should I implement for a web API?
  FRIDAY > From a defensive security perspective, I recommend: audit access
           controls, monitor for anomalies, keep systems patched, and
           maintain incident response procedures.

  You > Can you recall what we discussed about planning?
  FRIDAY > I recall our previous discussions. Drawing on prior context,
           I can provide a more informed perspective now.

[4/5] Self-Reflection...
  Self-reflection: 3 memories stored, 3 this session. Cognitive engine: mock mode.

[5/5] System Awareness & Automation...
  Platform: Linux-6.x.x
  Hostname: your-host
  Python:   3.11.x

  Localhost Port Scan:
    Port    80: closed
    Port   443: closed
    Port  8080: closed

  Session complete. 3 new memories stored.
  Memory file: friday/data/memory_store.json
```

Run it again and the memory count starts at 3 -- FRIDAY remembers across sessions.
