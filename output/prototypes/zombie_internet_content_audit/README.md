# Zombie Internet Content Audit

**Detect AI-generated "slop" and zombie internet patterns in any text, file, or feed.**

Scans content for 50+ lexical tells, structural fingerprints, and zombie internet patterns — then scores it on a low/medium/high confidence scale and classifies it as pure bot output, human-edited AI draft, AI-augmented human writing, or authentic human writing.

## Headline result

```
Source: samples/ai_slop.txt    -> HIGH confidence AI-generated (score: 95+)
Source: samples/human_auth.txt -> LOW  confidence AI-generated (score: <5)
Source: samples/zombie_hybrid   -> MEDIUM-HIGH confidence zombie pattern
```

Zero dependencies. Pure Python 3.8+ stdlib. No API keys needed.

## Quick links

- [HOW_TO_USE.md](HOW_TO_USE.md) — install, configure as a Claude skill, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) — architecture, signal dictionary, limitations

## Origin

Based on Jason Koebler's "Your AI Use Is Breaking My Brain" (404 Media) and Simon Willison's [commentary](https://simonwillison.net/2026/May/11/zombie-internet/#atom-everything) on the zombie internet phenomenon.
