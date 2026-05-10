# How to Use: DeepSeek Loop Agent

## Install (original Rust CLI)

```bash
# Requires Rust toolchain (rustup.rs)
cargo install --git https://github.com/v9ai/deepseek-loop

# Or clone + build
git clone https://github.com/v9ai/deepseek-loop.git
cd deepseek-loop
cargo build --release
# Binary at ./target/release/deepseek-loop
```

## Install (this Python prototype)

```bash
# No dependencies beyond Python 3.10+
git clone <this-repo>
cd deepseek_loop_agent
python3 cli.py --help
```

## Configure

```bash
# Set your DeepSeek API key (skip for mock/offline mode)
export DEEPSEEK_API_KEY="sk-..."
```

## As a Claude Skill

Drop the skill definition into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/deepseek_loop_agent
cp SKILL.md ~/.claude/skills/deepseek_loop_agent/SKILL.md
```

**Trigger phrases that activate this skill:**
- "Set up a DeepSeek agent loop with tool use"
- "Run a cron-scheduled agent using DeepSeek models"
- "I want a Claude-Code-like CLI but with DeepSeek as the backend"
- "Configure deepseek-loop with permission modes and built-in tools"
- "Stream agent events from a DeepSeek-powered loop"

## First 60 Seconds

### 1. Run the offline demo (no API key)

```
$ bash run.sh

==============================================
  DeepSeek Loop Agent — Demo Run
==============================================

--- Part 1: Agent Loop (mock DeepSeek backend) ---

Running agent with prompt: 'Analyze this codebase and summarize its structure.'

>> Tool: glob
   Result: ./deepseek_loop.py ./tools.py ./mock_deepseek.py ...
>> Tool: file_read
   Result:    1 | """    2 | Built-in tools for the DeepSeek agent loop. ...
>> Tool: bash
   Result: Python 3.12.0 Environment OK

--- Agent Analysis Complete ---
## Codebase Summary
This project implements a Claude-Code-shaped agent loop over the DeepSeek API.
...
```

### 2. Run with a real DeepSeek API key

```bash
export DEEPSEEK_API_KEY="sk-..."
python3 cli.py --allow-all "List all TODO comments in this project"
```

### 3. Schedule a recurring agent task

```bash
# Run every 5 minutes
python3 cli.py --interval 5m --allow-read "Check for new log errors in /var/log/app.log"

# Cron expression: weekdays at 9am
python3 cli.py --cron "0 9 * * 1-5" --allow-all "Generate morning status report"
```

### 4. Permission modes

```bash
python3 cli.py --allow-all "..."    # No prompts, full autonomy
python3 cli.py --allow-read "..."   # Auto-allow file reads, prompt for writes/bash
python3 cli.py --allow-bash "..."   # Auto-allow bash + reads
python3 cli.py "..."                # Prompt before every tool call (default)
```

### 5. Capture SdkMessage events programmatically

```python
from deepseek_loop import AgentLoop, PermissionMode

events = []
agent = AgentLoop(
    permission_mode=PermissionMode.ALLOW_ALL,
    event_callback=lambda e: events.append(e),
)
agent.run("Summarize this repo")

for e in events:
    print(e.type, e.tool_name, str(e.content)[:80])
```
