# How to Use

## Option A: Install as a Claude Skill (recommended)

This is a **Claude Code skill** — a markdown prompt file that teaches Claude how to humanize Chinese text on demand.

### Install

```bash
mkdir -p ~/.claude/skills/humanize_chinese
cp SKILL.md ~/.claude/skills/humanize_chinese/SKILL.md
```

### Trigger phrases

Once installed, any of these phrases will activate the skill in Claude Code:

- "Humanize this Chinese text"
- "Make this Chinese output natural"
- "Rewrite Chinese to sound human"
- "Polish Chinese writing"
- "Remove AI tone from Chinese"

Claude will then apply the humanization rules from the skill file to whatever Chinese text you provide.

### Example conversation

```
You:    Humanize this: 此外，人工智能在各个领域都有着广泛的应用。
Claude: 另外，AI在很多领域都用上了。
        Changes: '此外' → '另外'
```

## Option B: Use the Python CLI directly

### Prerequisites

- Python 3.10+
- No pip dependencies (stdlib only)

### Install

```bash
git clone https://github.com/voidborne-d/humanize-chinese.git
cd humanize-chinese
# or just copy humanize_chinese.py to your project
```

### CLI usage

```bash
# Inline text
python3 humanize_chinese.py "人工智能技术取得了显著的进展。"

# From file
python3 humanize_chinese.py -f input.txt

# Pipe from stdin
echo "需要注意的是，这很重要。" | python3 humanize_chinese.py

# Choose register: casual (default), professional, creative
python3 humanize_chinese.py -r professional "此外，该方案具有重要意义。"
```

### Use as a Python library

```python
from humanize_chinese import humanize

result = humanize("综上所述，该产品非常好。", register="casual")
print(result.humanized)   # "说到底，该产品挺好的。"
print(result.changes)     # ["'综上所述' → '说到底'", "'非常好' → '挺好的'"]
```

## First 60 seconds

```bash
$ bash run.sh

==========================================
 humanize_chinese — demo
==========================================

[Sample 1] AI-generated tech overview
--------------------------------------
============================================================
ORIGINAL:
人工智能技术在近年来取得了显著的进展。此外，它在各个领域都有着广泛的应用，
包括医疗、教育和金融等。需要注意的是，人工智能的发展也带来了一些挑战，
因此我们需要谨慎对待。

HUMANIZED:
人工智能技术在近年来发展得特别快。说实话，另外，它在各个领域都有着广泛的应用，
包括医疗、教育和金融等。不过话说回来，人工智能的发展也带来了一些挑战，
所以我们需要谨慎对待。

CHANGES (4):
  • '取得了显著的进展' → '发展得特别快'
  • '此外' → '另外'
  • '需要注意的是' → '不过话说回来'
  • '因此' → '所以'
============================================================
```

The output shows the original text, the humanized version, and a list of every change made — so you can verify meaning was preserved.
