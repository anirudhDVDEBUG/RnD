# Technical Details: Ta-Persona Digital Twin Distillation

## What It Does

Ta-Persona conducts a structured 5-round guided interview that extracts a
subject's "expression DNA" -- their tone, vocabulary preferences, sentence
structure, reasoning style, humor, values, and contextual adaptations. It
then synthesizes these observations into a reusable persona profile document
(Markdown + JSON) that can serve as a system prompt prefix to make any LLM
write in the subject's voice.

The original project (拓/Ta) targets Chinese-language persona distillation
with a focus on preserving cognitive "operating systems" -- the implicit
frameworks people use to reason, decide, and communicate. This prototype
demonstrates the full pipeline in English with mock data.

## Architecture

```
persona_distiller.py          # Single-file engine
  |
  +-- DIMENSIONS[]            # 5 interview dimensions with seed questions
  +-- MOCK_RESPONSES[]        # Pre-recorded responses for demo mode
  +-- MOCK_OBSERVATIONS[]     # Pattern observations per round
  |
  +-- run_mock_interview()    # Runs demo with canned data
  +-- run_interactive_interview()  # Terminal Q&A (--interactive flag)
  |
  +-- synthesize_persona()    # Aggregates observations into PersonaProfile
  +-- format_persona_markdown()  # Renders profile as Markdown
  |
  +-- output/
       +-- persona_<name>.md   # Human-readable profile
       +-- persona_<name>.json # Machine-readable profile
```

### Data Flow

1. **Interview phase**: 5 rounds x 2 questions = 10 data points collected
2. **Observation phase**: Each round produces pattern observations (in demo:
   pre-written; in live mode with Claude: LLM-generated analysis)
3. **Synthesis phase**: Observations are aggregated into a structured
   PersonaProfile dataclass covering tone, vocabulary, sentence architecture,
   reasoning style, cognitive OS, and contextual variations
4. **Output phase**: Profile rendered as both Markdown (for humans) and JSON
   (for programmatic use)

### Key Files

| File | Role |
|------|------|
| `persona_distiller.py` | Complete interview + synthesis engine |
| `SKILL.md` | Claude Code skill definition (drop into `~/.claude/skills/`) |
| `run.sh` | One-command demo runner |
| `requirements.txt` | Dependencies (none for demo) |

### Dependencies

- **Demo mode**: Python 3.10+ standard library only (no pip packages)
- **Live mode**: Would require `anthropic` SDK for LLM-powered adaptive
  questions and real-time pattern analysis

### Model Calls

The demo makes **zero API calls**. In a production version, you would call
Claude at two points:

1. **After each interview round** -- to analyze responses and generate
   adaptive follow-up questions (making the interview dynamic rather than
   static)
2. **During synthesis** -- to produce richer, more nuanced persona
   observations from raw interview data

## Limitations

- **Demo uses static synthesis**: The mock interview produces a hardcoded
  persona profile. Real distillation requires LLM analysis of responses.
- **No writing sample ingestion**: The original ta-persona project can
  analyze existing writing samples (emails, messages, posts) to accelerate
  distillation. This prototype only covers the interview path.
- **Single-session only**: No persistence of interview state across sessions.
  A production version would save partial interviews and allow resumption.
- **English only in demo**: The original project supports multilingual
  distillation (especially Chinese). This prototype's mock data is English.
- **No validation loop**: The original includes a fidelity rating step
  (subject rates accuracy 1-10) with iterative refinement. The demo skips
  this.

## Why It Matters for Claude-Driven Products

**Lead-gen / Marketing / Ad Creatives**: Persona profiles let you generate
brand-consistent copy at scale. Instead of a vague "write in a friendly
tone", you get a precise voice specification with calibration examples that
any model can follow.

**Agent Factories**: When building specialized agents, each agent needs a
distinct voice. Ta-Persona provides a repeatable process for capturing and
encoding those voices as structured data.

**Voice AI**: The persona profile's tone, vocabulary, and sentence
architecture sections map directly to voice synthesis parameters -- helping
maintain consistency between written and spoken output.

**Customer-facing digital twins**: For executives, creators, or domain
experts who want an AI that "sounds like them" in customer interactions,
this is the distillation step that captures what makes their communication
distinctive.

## Source

[n8f86p7j5b-afk/ta-persona](https://github.com/n8f86p7j5b-afk/ta-persona)
