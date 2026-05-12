# Technical Details

## What it does

A rule-based content auditor that scans text for patterns statistically associated with AI-generated writing. It checks three signal categories — lexical tells (specific words/phrases LLMs overuse), structural tells (formulaic document patterns), and zombie internet patterns (engagement bait, SEO stuffing, hustlebro framing) — then produces a weighted score, confidence level, and classification.

This is not a machine-learning classifier. It's a deterministic heuristic engine: fast, transparent, no API keys, no model calls. Every flagged signal points to a specific passage with a line reference, so a human reviewer can quickly verify or dismiss it.

## Architecture

```
audit_content.py          # Single-file implementation, ~350 lines
  |
  +-- Signal dictionaries  # LEXICAL_TELLS (50+ phrases with weights)
  |                        # STRUCTURAL_PATTERNS (6 regex/check rules)
  |                        # ZOMBIE_PATTERNS (4 regex/check rules)
  |
  +-- Custom checks        # paragraph_uniformity (std-dev of paragraph lengths)
  |                        # keyword_density (n-gram frequency analysis)
  |
  +-- Scoring engine       # Weighted sum, length-normalized
  |                        # Thresholds: <5 low, 5-15 medium, >15 high
  |
  +-- Reporter             # Text or JSON output with line references

samples/                   # 3 demo texts: pure slop, authentic human, zombie hybrid
SKILL.md                   # Claude Code skill definition
```

**Data flow:** File/stdin/inline text -> tokenize -> run all signal checks -> accumulate weighted findings -> length-normalize -> classify -> format report.

**Dependencies:** None. Python 3.8+ stdlib only (re, json, dataclasses, pathlib, argparse).

## Key signals detected

| Category | Signal | Weight | Example |
|----------|--------|--------|---------|
| Lexical | "delve", "landscape", "game-changer" | 2-3 | "Let's delve into the landscape..." |
| Lexical | "in today's fast-paced world" | 4 | Opening sentence of AI slop |
| Lexical | "whether you're a seasoned" | 4 | AI's favorite audience qualifier |
| Structural | Listicle with bold headings | 2/hit | `1. **Bold Title**` pattern |
| Structural | Paragraph uniformity | 2 | All paragraphs within 15% of mean length |
| Zombie | Engagement bait | 2/hit | "What do you think? Share your thoughts!" |
| Zombie | SEO keyword stuffing | 2 | Same 2-3 word phrase repeated 4+ times |
| Zombie | Hustlebro framing | 2/hit | "passive income", "6-figure", "scale your" |

## Limitations

- **Not proof.** This identifies patterns *consistent with* AI generation. A human writer who naturally uses "delve" will get flagged. A skilled editor can strip AI tells from generated text.
- **English only.** Signal dictionaries are English-specific. Other languages have different AI-tell distributions.
- **No model calls.** This won't catch well-edited AI text that avoids common tells. For higher accuracy you'd need a classifier model (GPT-Zero, Originality.ai, etc.), but those have their own false-positive problems.
- **Static signals.** As LLMs evolve, their lexical fingerprint shifts. The signal dictionary needs periodic updates.

## Why this matters for Claude-driven products

| Use case | Relevance |
|----------|-----------|
| **Lead-gen / marketing** | Audit outbound content before publishing to avoid sounding like AI slop. Prospects increasingly distrust generic AI-sounding copy. |
| **Ad creatives** | Pre-screen ad copy for AI tells that trigger reader skepticism and reduce CTR. |
| **Agent factories** | Quality gate for agent-generated content — catch slop before it ships. |
| **Content platforms** | Filter incoming submissions/comments for bot-generated noise. |
| **Voice AI** | Audit scripts and transcripts — AI tells in spoken content sound especially robotic. |

The zombie internet problem (Koebler's framing) is that humans are using AI to talk to other humans, creating an uncanny valley of semi-authentic content. Tools like this help maintain quality standards in a world where the default output is increasingly machine-generated.
