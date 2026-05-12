# How to Use LLM Shebang Scripts

## Install (real usage)

```bash
# 1. Install the llm CLI
pip install llm
# or
pipx install llm

# 2. Set up a model key (e.g., for Claude)
llm keys set anthropic
# paste your ANTHROPIC_API_KEY when prompted

# 3. (Optional) Install tool plugins
llm install llm-time
```

**Requirement:** GNU coreutils 8.30+ (for `env -S` multi-arg shebang support). Check with `env --version`. Most Linux distros from 2019+ and macOS with Homebrew coreutils have this.

## Run the demo (no API keys needed)

```bash
pip install pyyaml           # only dependency for the demo
bash run.sh                  # runs with mock data
```

## Claude Code Skill Installation

This is a Claude Code skill. To install:

```bash
# Drop the skill file into place
mkdir -p ~/.claude/skills/llm_shebang_scripts
cp SKILL.md ~/.claude/skills/llm_shebang_scripts/SKILL.md
```

### Trigger phrases that activate the skill

- "Make this prompt into an executable script"
- "Create a shebang script that calls an LLM"
- "I want to run a text file as an LLM prompt"
- "Build a CLI tool from a prompt using llm"
- "Create an LLM template script with tool use"

Once installed, Claude Code will use the skill automatically when you say things like *"turn this prompt into a runnable script"*.

## First 60 Seconds

### 1. Create a fragment script (simplest form)

```bash
cat > joke.sh << 'EOF'
#!/usr/bin/env -S llm -f
Tell me a one-liner programming joke
EOF
chmod +x joke.sh
./joke.sh
```

**Output:**
```
Why do programmers prefer dark mode? Because light attracts bugs.
```

### 2. Create a script with tool access

```bash
cat > now.sh << 'EOF'
#!/usr/bin/env -S llm -T llm_time -f
What time is it right now? Respond in exactly one sentence.
EOF
chmod +x now.sh
./now.sh
```

**Output:**
```
It is currently 2:47 PM EDT on May 12, 2026.
```

### 3. Create a YAML template with inline functions

```bash
cat > calc.yaml << 'EOF'
#!/usr/bin/env -S llm -t
model: claude-sonnet-4-6
system: Use tools to run calculations
functions: |
  def add(a: int, b: int) -> int:
      return a + b
  def multiply(a: int, b: int) -> int:
      return a * b
EOF
chmod +x calc.yaml
./calc.yaml "what is 42 * 17 + 5" --td
```

**Output (with --td tool debug):**
```
Tool call: multiply(42, 17) → 714
Tool call: add(714, 5) → 719
The answer is 719.
```

### 4. Use the builder tool (included in this repo)

```bash
python3 shebang_builder.py create review.sh \
    "Review the code on stdin for security issues" \
    --mode fragment --tools llm_time

python3 shebang_builder.py validate review.sh examples/*
```

### 5. Pipe data into a shebang script

```bash
git diff | ./examples/commit_message.sh
# → feat: add user authentication middleware for API routes
```

## Key Flags Reference

| Flag | What it does |
|---|---|
| `-f` | Fragment mode — file contents are the prompt |
| `-t` | Template mode — file is a YAML template |
| `-T plugin` | Enable a tool plugin (e.g., `llm_time`) |
| `--td` | Show tool-call debug output |
| `-m model` | Override the model (in fragment mode) |
