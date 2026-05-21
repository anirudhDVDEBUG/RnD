# How to Use

## This is a Claude Code Skill

No pip install or npm install required. You drop the skill folder into your Claude Code skills directory.

### Install

```bash
# Copy the skill into your Claude Code skills directory
mkdir -p ~/.claude/skills/google_io_gemini_spark_tracker
cp SKILL.md ~/.claude/skills/google_io_gemini_spark_tracker/SKILL.md
```

That's it. Claude Code will auto-detect the skill on the next session.

### Trigger phrases

Say any of these to Claude Code and the skill activates:

- "What was announced at Google I/O 2026?"
- "What is Gemini Spark?"
- "Tell me about the Antigravity SDK"
- "How does Google handle prompt injection in Gemini Spark?"
- "Compare Gemini Spark to OpenClaw"
- "What model does Gemini Spark use?"

The skill will **not** trigger for older Google I/O events, general Gemini API usage, or unrelated Google products.

### Run the standalone tracker (no Claude Code needed)

```bash
# Requires Python 3.10+ (stdlib only, no dependencies)
python3 tracker.py
```

Or simply:

```bash
bash run.sh
```

## First 60 seconds

**Input:**

```bash
bash run.sh
```

**Output (truncated):**

```
========================================================================
  Google I/O 2026 -- Gemini Spark & Antigravity Tracker
========================================================================
  Report date: 2026-05-21
  Source: Simon Willison's Weblog (2026-05-20)

--- Availability Summary ---

  Generally Available............ 3 item(s)
  Preview / Coming Soon.......... 4 item(s)
  Announced Only................. 0 item(s)

--- All Announcements ---

  STATUS       NAME                         CATEGORY
  ------------------------------------------------------------
  [PREVIEW]    Gemini Spark                 Personal AI Agent
  [GA]         Gemini 3.5 Flash             Foundation Model
  ...

--- Competitive Landscape (Snapshot) ---

  Feature                  Gemini Spark                    OpenClaw          Claude Code
  -------------------------------------------------------------------------------------------
  Model                    Gemini 3.5 Flash                GPT-5o            Claude Opus 4.6
  CLI tool                 Antigravity CLI (Go)            OpenClaw CLI      claude (JS)
  ...

--- JSON Export ---

  Exported 7 items to google_io_2026_tracker.json
```

The JSON export (`google_io_2026_tracker.json`) is machine-readable for downstream pipelines.

## Updating the data

Edit `tracker.py` and modify the `ANNOUNCEMENTS` list to add new items or change availability status as Google ships features to GA.
