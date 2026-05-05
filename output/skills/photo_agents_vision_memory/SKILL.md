---
name: photo_agents_vision_memory
description: |
  Set up autonomous self-evolving agents with vision-grounded layered memory and self-written skills using Photo-agents.
  Triggers: building vision-based autonomous agents, implementing photographic memory for LLM agents, creating self-evolving agent systems with computer-use capabilities, adding layered memory with screenshot grounding, designing agents that write their own skills.
---

# Photo-agents: Vision-Grounded Autonomous Agents

Set up autonomous self-evolving agents that use vision-grounded layered memory and self-written skills to operate your computer.

## When to use

- "Build an autonomous agent with photographic/visual memory"
- "Create a self-evolving agent that can operate my computer"
- "Implement vision-grounded layered memory for an LLM agent"
- "Set up agents that write and learn their own skills over time"
- "Build a computer-use agent with persistent memory across sessions"

## How to use

### 1. Clone and install Photo-agents

```bash
git clone https://github.com/jmerelnyc/Photo-agents.git
cd Photo-agents
pip install -r requirements.txt
```

### 2. Core architecture concepts

Photo-agents implements three key patterns:

- **Vision-grounded memory**: Agents capture screenshots and ground their understanding in visual context, creating a "photographic memory" layer that persists across sessions.
- **Layered memory system**: Multiple memory tiers (working, episodic, semantic) that allow agents to recall past interactions, learn from experience, and build long-term knowledge.
- **Self-written skills**: Agents observe their own successful action sequences and codify them as reusable skills, enabling autonomous self-improvement.

### 3. Building an agent with photographic memory

```python
# Example: Initialize a Photo-agent with vision-grounded memory
from photo_agents import Agent, MemoryLayer, VisionGrounding

# Set up layered memory
memory = MemoryLayer(
    working_memory_size=10,    # Recent context window
    episodic_store="./memory/episodes",  # Past interaction logs
    semantic_store="./memory/knowledge"   # Learned facts & skills
)

# Enable vision grounding (screenshots as memory anchors)
vision = VisionGrounding(
    capture_interval="on_action",  # Screenshot on each action
    embedding_model="clip"          # Visual embedding for retrieval
)

# Create the self-evolving agent
agent = Agent(
    memory=memory,
    vision=vision,
    skill_dir="./skills",  # Where agent writes learned skills
    auto_skill_extraction=True  # Agent codifies repeated patterns
)

agent.run(task="Your task description here")
```

### 4. Self-evolving skill system

Agents autonomously create skill files when they detect repeated successful patterns:

```python
# Skills are stored as executable modules the agent can invoke
# Example auto-generated skill structure:
# ./skills/
#   open_browser_and_navigate.py
#   fill_form_fields.py
#   extract_table_data.py

# You can also manually add skills:
from photo_agents.skills import SkillRegistry

registry = SkillRegistry(skill_dir="./skills")
registry.list_skills()  # See what the agent has learned
```

### 5. Computer-use integration

Photo-agents can operate your computer through vision-guided actions:

```python
# The agent uses screenshots to understand UI state
# and executes mouse/keyboard actions accordingly
agent.run(
    task="Open the spreadsheet and summarize column B",
    computer_use=True,
    safety_mode=True  # Requires confirmation for destructive actions
)
```

### Key configuration

- Set `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` environment variable for the backing LLM
- Configure memory persistence paths for cross-session learning
- Adjust vision capture frequency based on task complexity
- Review and curate the `./skills` directory to prune low-quality auto-generated skills

## References

- Source repository: https://github.com/jmerelnyc/Photo-agents
- Topics: agent-memory, ai-agents, autonomous-agents, computer-use, self-evolving-agents, vision-agents
- Language: Python
