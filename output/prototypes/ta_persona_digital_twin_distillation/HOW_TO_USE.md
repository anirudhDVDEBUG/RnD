# How to Use Ta-Persona Digital Twin Distillation

## Option A: As a Claude Code Skill (recommended)

### Install

Copy the skill folder into your Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills/ta-persona-digital-twin-distillation
cp SKILL.md ~/.claude/skills/ta-persona-digital-twin-distillation/SKILL.md
```

### Trigger Phrases

Once installed, say any of these to Claude Code:

- "Create a digital twin of my writing voice"
- "Distill my persona through an interview"
- "Imprint my tone of voice into a reusable profile"
- "Build a persona document from a conversation"
- "Extract my cognitive style and communication patterns"

Claude will then conduct a 5-7 round guided interview, asking about your
communication style, vocabulary, reasoning patterns, emotional tone, values,
and quirks. After the interview it synthesizes a structured persona profile
you can reuse as a system prompt prefix.

---

## Option B: Standalone Python Demo

### Install

```bash
git clone <this-repo>
cd ta_persona_digital_twin_distillation
pip install -r requirements.txt   # no external deps for demo
```

### Run the Demo (mock data, no API key needed)

```bash
bash run.sh
```

### Run an Interactive Interview

```bash
python3 persona_distiller.py --interactive
```

You'll answer 10 questions across 5 dimensions. At the end, the engine
produces a persona Markdown file and JSON file in `output/`.

---

## First 60 Seconds

```
$ bash run.sh

================================================================
  Ta-Persona: Digital Twin Distillation Engine
  Mode: DEMO (mock interview data)
================================================================

Subject: Alex Chen
Interview rounds: 5

--- Round 1/5: Communication Style ---

  Q: How would you describe your default writing style...
  A: I'd say I'm casually professional. Like, I won't use slang in work emails but I'm not writing le...

  >> Observation: Casually professional register; heavy use of em dashes...

--- Round 2/5: Vocabulary & Expression ---
  ...

================================================================
  Synthesizing persona profile...
================================================================

# Persona Profile: Alex Chen

## Voice Summary
Alex Chen writes with casual professionalism -- direct, opinionated, and
precise without being stiff...

## Expression DNA
### Tone & Register
- Default Formality: Casual-professional (60/40 toward casual)
- Humor Style: Dry, self-deprecating, situational...

### Vocabulary Patterns
- Preferred Terms: use (not utilize), figure out (not determine)...
- Signature Phrases: the thing is, my read is, peak [noun]...

## Calibration Examples
> Hey -- just pushed the fix for the auth timeout. Turned out the retry
> logic was swallowing the error silently. Classic...

Persona saved to: output/persona_alex_chen.md
JSON saved to:    output/persona_alex_chen.json
```

### Output Files

| File | Purpose |
|------|---------|
| `output/persona_alex_chen.md` | Human-readable persona profile |
| `output/persona_alex_chen.json` | Machine-readable profile for programmatic use |

### Using the Persona

Paste the contents of the `.md` file as a system prompt prefix:

```
You are writing as Alex Chen. Follow this persona profile exactly:
[paste persona_alex_chen.md contents here]

Now write a response to: ...
```

Or load the JSON programmatically and inject the relevant fields into your
prompt template.
