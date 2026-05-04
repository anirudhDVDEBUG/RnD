# How to Use — Unslop Text

## Option A: Claude Code Skill (recommended)

### Install

```bash
mkdir -p ~/.claude/skills/unslop_text
# Copy the SKILL.md into the skill folder:
cp SKILL.md ~/.claude/skills/unslop_text/SKILL.md
```

### Trigger phrases

Say any of these to Claude Code and it will apply the unslop skill:

- "unslop this" / "remove slop" / "de-slop"
- "make it sound less AI" / "remove AI-isms"
- "less robotic" / "too flowery" / "sounds like ChatGPT"
- "remove filler" / "tighten prose"
- "humanize this text" / "natural writing" / "clean up AI writing"

### Example

```
You: Here's my draft, can you unslop it?

"Great question! In today's rapidly evolving landscape, leveraging
cutting-edge AI tools has become fundamentally essential..."

Claude: [applies skill, returns cleaned text with slop report]
```

---

## Option B: Python CLI / Library

### Install

```bash
# No dependencies — just Python 3.10+
git clone <this-repo> && cd unslop_text
```

### CLI usage

```bash
# From file
python3 unslop.py my_draft.txt

# From stdin
echo "Let's dive deep into this groundbreaking solution" | python3 unslop.py

# Quiet mode (cleaned text only)
python3 unslop.py -q my_draft.txt

# JSON output (for pipelines)
python3 unslop.py --json my_draft.txt

# Write to file
python3 unslop.py my_draft.txt -o cleaned.txt
```

### Library usage

```python
from unslop import unslop

result = unslop("Let's dive deep into this groundbreaking, innovative solution.")
print(result.cleaned)       # "This solution."
print(result.slop_count)    # 4
print(result.reduction_pct) # 62.3
```

---

## First 60 seconds

```bash
bash run.sh
```

This feeds `sample_sloppy.txt` (a worst-case AI-generated paragraph) through the cleaner and prints:

1. The original sloppy text
2. A categorized slop report (what was found, per category)
3. The cleaned text
4. JSON output for pipeline integration

Expected output: ~38 slop instances removed, text shortened by ~40%.
