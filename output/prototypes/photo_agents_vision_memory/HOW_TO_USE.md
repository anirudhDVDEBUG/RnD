# How to Use

## Install

```bash
# This demo (no API keys needed)
cd photo_agents_vision_memory
bash run.sh

# Full Photo-agents (requires API key for LLM backing)
git clone https://github.com/jmerelnyc/Photo-agents.git
cd Photo-agents
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."  # or OPENAI_API_KEY
```

## As a Claude Skill

Drop the skill file:

```bash
mkdir -p ~/.claude/skills/photo_agents_vision_memory
cp SKILL.md ~/.claude/skills/photo_agents_vision_memory/SKILL.md
```

**Trigger phrases** that activate it:
- "Build an autonomous agent with photographic memory"
- "Create a self-evolving agent that operates my computer"
- "Implement vision-grounded layered memory for an LLM agent"
- "Set up agents that write their own skills"
- "Build a computer-use agent with persistent memory"

## First 60 Seconds

```bash
$ bash run.sh

# Output shows:
# 1. Agent initializes 3-tier memory (working/episodic/semantic)
# 2. Vision grounding captures "screenshots" on each action
# 3. Agent runs a multi-step task with think→act loop
# 4. Repeated action patterns auto-extract into reusable skills
# 5. Final summary shows memory state + learned skills
```

**Input**: A task string (e.g., "Open browser, navigate to example.com, extract page title")

**Output**: Step-by-step execution log showing:
- Each think/act cycle with vision grounding
- Memory accumulation across tiers
- Auto-skill extraction when patterns repeat
- Final memory + skill inventory

## SDK Usage (Programmatic)

```python
from photo_agents import Agent, MemoryLayer, VisionGrounding

memory = MemoryLayer(working_memory_size=10)
vision = VisionGrounding(capture_interval="on_action")

agent = Agent(
    memory=memory,
    vision=vision,
    skill_dir="./skills",
    auto_skill_extraction=True,
)

result = agent.run(task="Your task here", steps=5)
# result["skills_available"] → list of learned skills
# result["memory"] → {working: N, episodic: N, semantic: N}
```

## Key Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `working_memory_size` | 10 | Sliding window of recent context |
| `capture_interval` | `"on_action"` | When to take screenshots |
| `embedding_model` | `"clip"` | Visual embedding model |
| `auto_skill_extraction` | `True` | Auto-learn from repeated patterns |
| `skill_dir` | `"./skills"` | Where skills are persisted |
