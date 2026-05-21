# How to Use

## Option A: Claude Code Skill (recommended)

This is a Claude Code skill — a structured prompt methodology, not a server.

### Install the skill

```bash
# Clone the source repo
git clone https://github.com/jnMetaCode/ai-shortfilm-prompts.git

# Copy the SKILL.md into Claude Code's skill directory
mkdir -p ~/.claude/skills/ai_shortfilm_prompts
cp ai-shortfilm-prompts/SKILL.md ~/.claude/skills/ai_shortfilm_prompts/SKILL.md
```

### Trigger phrases

Once installed, Claude Code activates this skill when you say things like:

- "Help me plan and write prompts for an AI short film"
- "Generate cinematic video prompts for Sora / Kling / Veo"
- "Write scene-by-scene video generation prompts for my story concept"
- "I want to create an AI-generated short film with a coherent narrative"

Claude will then walk you through the 4-phase methodology: Story development, Visual direction, Prompt engineering, and Production assembly.

## Option B: Standalone CLI tool (this prototype)

### Install

```bash
# No external dependencies — pure Python 3.8+ stdlib
pip install -r requirements.txt   # empty, but present for consistency
```

### First 60 seconds

**1. Generate full Markdown prompt doc (default):**

```bash
python3 generate_prompts.py
```

Output: A complete prompt document for "Last Light" (demo film) with style guide, character references, and 10 shot prompts optimized for Veo.

**2. Re-target to a different model:**

```bash
python3 generate_prompts.py --model sora
python3 generate_prompts.py --model kling
```

Each model gets tailored style hints (e.g., Sora emphasizes photorealism; Kling emphasizes motion dynamics).

**3. Export raw prompts only (paste directly into a video model):**

```bash
python3 generate_prompts.py --format prompts --model sora
```

**4. Export as JSON (for pipeline integration):**

```bash
python3 generate_prompts.py --format json > last_light.json
```

**5. View a single scene:**

```bash
python3 generate_prompts.py --scene 4
```

**6. List supported models:**

```bash
python3 generate_prompts.py --list-models
```

### Run the full demo

```bash
bash run.sh
```

This runs all output formats and models, showing the complete workflow end-to-end.
