# How to Use Fork-a-Slicer

## What This Is

A Claude Code **skill** that provides step-by-step AI-agent guidance for forking OrcaSlicer and adding Bambu Lab printer support via a process isolation bridge (FULU-Foundation architecture).

This prototype repo also includes a runnable demo of the bridge architecture itself.

---

## Install the Skill

### 1. Clone the source plans

```bash
git clone https://github.com/danielcherubini/fork-a-slicer.git
cd fork-a-slicer
```

### 2. Install as a Claude Code skill

Copy or symlink the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/fork_a_slicer
cp SKILL.md ~/.claude/skills/fork_a_slicer/SKILL.md
```

Or if you prefer a symlink:

```bash
ln -s "$(pwd)" ~/.claude/skills/fork_a_slicer
```

### 3. Trigger Phrases

Once the skill is installed, Claude Code activates it when you say things like:

- "Help me fork OrcaSlicer and add Bambu printer support"
- "Set up a process isolation bridge for 3D printer communication"
- "Guide me through the FULU-Foundation architecture for slicer development"
- "I want to build a Bambu Connect bridge for OrcaSlicer"
- "Create a slicer fork with JSON-RPC printer networking"

---

## Run the Demo (No Skill Required)

### Prerequisites

- Python 3.8+ (uses only stdlib — no pip install needed)
- Linux or macOS (uses Unix domain sockets)

### Run

```bash
bash run.sh
```

### First 60 Seconds

**Input:** Run `bash run.sh` — no arguments, no config, no API keys.

**Output:** You will see:

```
--- Fork-a-Slicer: Process Isolation Bridge Demo ---

[main] Starting Bambu Connect Bridge (separate process)...
[bridge] Bambu Connect Bridge started (PID 12345)
[bridge] Listening on /tmp/bambu_bridge.sock
[bridge] Architecture: FULU-Foundation / Process Isolation
[main] Bridge is ready. Slicer PID=12340, Bridge PID=12345
[main] Two separate processes communicating via /tmp/bambu_bridge.sock

============================================================
  STEP 1: Query Bridge Info
============================================================
  Bridge Version : 0.1.0
  Architecture   : FULU-Foundation
  Protocol       : JSON-RPC 2.0
  ...

============================================================
  STEP 2: Discover Bambu Lab Printers
============================================================
  Found 3 printer(s):
    [X1 Carbon   ] BambuLab X1C - Workshop
    [P1S         ] BambuLab P1S - Office
    [A1          ] BambuLab A1 - Prototyping

============================================================
  STEP 3: Printer Status Details
============================================================
  (detailed status for each printer including temps, filament, progress)

============================================================
  STEP 4: Submit Print Job
============================================================
  Job ID  : JOB-38201
  Status  : queued
  Message : Print job submitted to BambuLab X1C - Workshop

============================================================
  STEP 5: Error Handling — Submit to Busy Printer
============================================================
  Expected error : Printer is busy
  Error code     : -32002

============================================================
  DEMO COMPLETE
============================================================
  The FULU-Foundation process isolation bridge works as follows:
  1. Bridge runs as a SEPARATE PROCESS
  2. Slicer communicates via JSON-RPC over Unix domain socket
  3. No proprietary Bambu code inside the slicer process
  ...
```

The whole run takes under 2 seconds. Two real OS processes start, communicate over a socket, and shut down cleanly.

---

## File Overview

| File | Purpose |
|---|---|
| `demo.py` | Orchestrator — starts bridge subprocess, runs slicer client |
| `bambu_bridge.py` | Bridge process — JSON-RPC server over Unix socket |
| `slicer_client.py` | Slicer side — discovers printers, submits jobs via RPC |
| `run.sh` | Entry point — validates Python, runs demo |
| `requirements.txt` | Dependencies (stdlib only) |
