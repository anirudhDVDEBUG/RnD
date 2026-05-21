# How to Use

## Install

No install required. Clone and open:

```bash
git clone <this-repo>
cd token_speed_visualizer
open token_speed_demo.html   # macOS
xdg-open token_speed_demo.html  # Linux
# or just double-click the HTML file
```

Or run the helper script which also starts a local server:

```bash
bash run.sh
```

## As a Claude Code Skill

Drop the skill definition into your skills directory:

```bash
mkdir -p ~/.claude/skills/token_speed_visualizer
cp SKILL.md ~/.claude/skills/token_speed_visualizer/SKILL.md
```

**Trigger phrases:**
- "What does 30 tokens per second look like?"
- "Build a demo that simulates LLM output speed"
- "Compare token throughput speeds visually"
- "I want to visualize the difference between 10 and 100 tokens per second"
- "Create an interactive token speed simulator"

When triggered, Claude will generate a self-contained HTML file in your current directory.

## First 60 seconds

1. Open `token_speed_demo.html` in your browser
2. Click the **"30 t/s"** preset button
3. Click **Start** - watch text stream at a comfortable reading pace
4. Click **Stop**, then click **"200 t/s"** and **Start** again
5. Notice how text now floods in faster than you can read
6. Try **"10 t/s"** to feel what budget local inference looks like
7. The stats bar shows actual tokens emitted, elapsed time, and measured rate

**Input:** Click a speed preset + Start button
**Output:** Simulated LLM text streaming at that exact rate with live metrics
