# How to Use Loushang Multi-Model Orchestration

## Install

```bash
# Clone the upstream repo
git clone https://github.com/zhnt/loushang.git
cd loushang

# Install (Python 3.10+)
pip install -e .
```

## As a Claude Code Skill

Drop the skill folder into your skills directory:

```bash
mkdir -p ~/.claude/skills/loushang_multi_model_orchestration
cp SKILL.md ~/.claude/skills/loushang_multi_model_orchestration/SKILL.md
```

**Trigger phrases:**
- "Set up a multi-model agent orchestration for my coding project"
- "Orchestrate Claude, DeepSeek, and Qwen agents in a unified workflow"
- "Configure tool governance and traceability for agentic coding"
- "Run multiple AI coding models together with session persistence"
- "I need stateful session management across different AI coding agents"

## Configuration

Set API keys for each provider you want to use:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."
export QWEN_API_KEY="sk-..."
export KIMI_API_KEY="sk-..."
export MINIMAX_API_KEY="sk-..."
```

## CLI Usage

```bash
# Interactive TUI mode
loushang

# CLI automation mode
loushang --cli

# Run a specific workflow
loushang run --workflow plan-implement-review --task "Add error handling to auth module"
```

## First 60 Seconds

**Input:** Run the local demo (no API keys needed):

```bash
bash run.sh
```

**Output:**

```
=== Loushang Multi-Model Orchestration Demo ===

[Session 8b2c] Starting workflow: plan-implement-review
  Provider: mock (demo mode)

[Step 1/3] PLAN (model: deepseek-r1)
  Task: "Add input validation to user registration endpoint"
  Result: 3 subtasks identified
    1. Validate email format
    2. Check password strength
    3. Sanitize username

[Step 2/3] IMPLEMENT (model: claude-opus)
  Generating code for 3 subtasks...
  Files written: validators.py (34 lines)

[Step 3/3] REVIEW (model: qwen-max)
  Reviewing validators.py...
  Result: APPROVED (2 suggestions, 0 blocking issues)

[Session 8b2c] DELIVERED
  Duration: 2.1s | Tool calls: 7 | Policy violations: 0
  Trace saved: ./traces/session_8b2c.json
```

## Session Management

```bash
# List sessions
loushang sessions list

# Resume a session
loushang sessions resume <session-id>

# Fork a session to explore alternatives
loushang sessions fork <session-id>

# Replay for auditing
loushang sessions replay <session-id>
```

## Tool Governance

Define policies in `loushang.yaml`:

```yaml
governance:
  policies:
    - agent: claude-opus
      allowed_tools: [read_file, write_file, run_tests]
      denied_tools: [delete_file, exec_shell]
    - agent: deepseek-r1
      allowed_tools: [read_file, search]
      denied_tools: [write_file, exec_shell]
```
