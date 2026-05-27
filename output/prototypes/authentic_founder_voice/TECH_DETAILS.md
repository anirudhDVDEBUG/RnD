# Tech Details: Authentic Founder Voice

## What it does

This is a Claude Code **skill** — a structured prompt (SKILL.md) that shapes Claude's behavior when triggered by specific user requests. It teaches Claude to detect AI-generated patterns in founder communications and rewrite them using principles from Paul Graham's advice on authentic writing.

The standalone demo (`rewrite.py`) implements a subset of the same logic as pure Python: regex-based red flag detection, scoring, and rule-based rewriting heuristics. It doesn't call any LLM API — it uses pattern matching to identify AI voice markers and applies mechanical transformations to demonstrate the concept.

## Architecture

```
SKILL.md              — Prompt engineering: red flag taxonomy + rewrite rules
rewrite.py            — Standalone demo: regex scanner + rewrite engine
samples.py            — 4 sample founder emails (AI-polished originals)
run.sh                — Entry point: runs rewrite.py on all samples
requirements.txt      — No external deps (stdlib only)
```

### Data flow (skill mode, inside Claude Code)

```
User pastes draft email
  -> Claude loads SKILL.md instructions
  -> Step 1: Scan for AI-voice red flags (superlatives, filler, structure)
  -> Step 2: Rewrite applying 6 authentic-voice principles
  -> Step 3: Apply Paul Graham test (would reader suspect AI?)
  -> Output: flagged issues + rewritten email
```

### Data flow (standalone demo)

```
samples.py provides 4 AI-polished emails
  -> rewrite.py scans each with regex patterns (30+ patterns)
  -> Flags matched patterns with line-level detail
  -> Applies mechanical rewrites (strip filler, shorten, de-buzzword)
  -> Prints before/after comparison with score
```

## Key patterns detected

| Category | Examples |
|---|---|
| Corporate filler | "I hope this finds you well", "I wanted to reach out", "Thank you for your time" |
| Superlatives | "revolutionary", "groundbreaking", "game-changing", "unprecedented" |
| AI cliches | "at the intersection of", "leveraging", "synergies", "cutting-edge" |
| Structural tells | Perfectly parallel lists, balanced paragraph lengths, em-dash rhetorical flourish |
| Empty rhetoric | "poised to disrupt", "reimagining the future", "unlocking value" |

## Dependencies

- Python 3.8+ (stdlib only — `re`, `textwrap`, `json`)
- No API keys required for the demo
- Claude Code required to use the skill itself

## Limitations

- **The skill is a prompt, not a model.** Quality depends on Claude's underlying ability. The SKILL.md provides structure and principles but doesn't guarantee output quality.
- **The standalone demo uses regex, not NLP.** It catches obvious patterns but misses subtle AI voice (e.g., overly smooth transitions, suspiciously balanced arguments).
- **No personalization.** The skill doesn't learn a specific founder's voice — it applies generic "authentic" heuristics. A founder who naturally writes formally might get bad rewrites.
- **English only.** Red flag patterns are English-specific.

## Why it matters for Claude-driven products

- **Lead-gen / outreach automation**: Any tool generating cold emails needs an AI-detection pass. This skill's red flag taxonomy is directly reusable.
- **Marketing copy**: Same AI-smell problem applies to landing pages, ad copy, social posts. The detection patterns generalize.
- **Agent factories**: If you're building agents that write on behalf of humans, the Paul Graham test ("would the reader suspect AI?") is a quality gate worth automating.
- **Brand voice**: The skill's rewrite principles (be direct, be specific, be imperfect) are a minimal style guide that any text-generating agent could adopt.

## References

- [Quoting Paul Graham — Simon Willison](https://simonwillison.net/2026/May/26/paul-graham/#atom-everything)
