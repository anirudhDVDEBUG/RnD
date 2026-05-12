# How to Use

## Install

```bash
git clone <this-repo>
cd zombie_internet_content_audit
# No pip install needed — stdlib only, Python 3.8+
```

## Run the demo

```bash
bash run.sh
```

## CLI usage

```bash
# Audit a single file
python3 audit_content.py article.txt

# Audit inline text
python3 audit_content.py "In today's fast-paced world, it's important to note..."

# Audit all .txt/.md files in a directory
python3 audit_content.py --dir ./my_content/

# Pipe from stdin
curl -s https://example.com/article | python3 audit_content.py --stdin

# JSON output
python3 audit_content.py --format json article.txt
```

## Use as a Claude Code Skill

This is a Claude Code skill. To install it:

1. Copy the `SKILL.md` file to your skills directory:

```bash
mkdir -p ~/.claude/skills/zombie_internet_content_audit
cp SKILL.md ~/.claude/skills/zombie_internet_content_audit/SKILL.md
```

2. The skill activates on trigger phrases like:
   - "Does this look AI-generated?"
   - "Check this article for LLM slop"
   - "Audit this content for authenticity"
   - "Scan this page for zombie internet patterns"
   - "Is this real human writing?"

3. When triggered, Claude will use the heuristics defined in SKILL.md to analyze content — either by running `audit_content.py` directly or by applying the same signal checks inline.

## First 60 seconds

```
$ bash run.sh

========================================
 Zombie Internet Content Audit - Demo
========================================

Scanning 3 sample texts for AI slop signals...

======================================================================
ZOMBIE INTERNET CONTENT AUDIT
Source: samples/ai_slop.txt
Words: 498
======================================================================

  Confidence:     HIGH
  Score:          97.8
  Classification: Pure bot output / unedited AI generation

----------------------------------------------------------------------
TOP SIGNALS:
  - [LEXICAL] "cutting-edge": AI-associated phrase found 3 time(s) (weight=6.0, lines [8, 16, 40])
  - [LEXICAL] "in today's fast-paced world": AI-associated phrase found 1 time(s) (weight=4.0, lines [1])
  - [LEXICAL] "whether you're a seasoned": AI-associated phrase found 1 time(s) (weight=4.0, lines [3])
  - [STRUCTURAL] Listicle padding: Numbered list with bold headings (weight=20.0)
  - [ZOMBIE] Engagement bait: Engagement-bait phrasing (weight=2.0)
----------------------------------------------------------------------

...

======================================================================
ZOMBIE INTERNET CONTENT AUDIT
Source: samples/human_authentic.txt
Words: 342
======================================================================

  Confidence:     LOW
  Score:          0.0
  Classification: Likely authentic human writing
```
