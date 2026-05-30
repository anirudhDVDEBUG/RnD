# Technical Details — Build DNA Business Ideation

## What It Does

Build DNA is a Claude Code **skill** (prompt-only, no runtime code) that implements a structured 3-phase business ideation framework. Phase 1 conducts an adaptive interview to extract the user's unique "founder DNA" — skills, experience, unfair advantages, constraints, and goals. Phase 2 uses that profile to generate 3-5 personalized business ideas across multiple business types (SaaS, services, creator, e-commerce, cross-border arbitrage). Phase 3 lets the user select one idea and produces a full execution package: market sizing, competitive analysis, GTM strategy, MVP roadmap, and a 72-hour action plan to first revenue.

The skill works entirely through Claude's reasoning — no external APIs, databases, or model calls beyond the Claude session itself. The quality of output depends on the depth of the user's intake answers and Claude's ability to synthesize them into actionable plans.

## Architecture

```
~/.claude/skills/build_dna_business_ideation/
  SKILL.md          <- The entire skill (prompt template)

demo.py             <- Standalone demo with mock data (this repo)
output.json         <- Structured output from demo run
```

### Key Components

| Component | Role |
|-----------|------|
| `SKILL.md` | Prompt template loaded by Claude Code; defines the 3-phase workflow, output format, and trigger phrases |
| `demo.py` | Python script simulating the full workflow with a hardcoded founder profile; produces both terminal output and `output.json` |

### Data Flow

```
User trigger phrase
  -> Claude loads SKILL.md
  -> Phase 1: Claude asks intake questions (5 categories, adaptive follow-ups)
  -> User provides answers
  -> Phase 2: Claude generates 3-5 ideas with difficulty ratings
  -> User selects one idea
  -> Phase 3: Claude produces market analysis, GTM, MVP roadmap, 72-hour plan
```

### Dependencies

- **Skill itself**: None. Pure prompt — runs in any Claude Code session.
- **Demo script**: Python 3.7+ stdlib only (json, dataclasses, textwrap).

## Limitations

- **No real market data.** TAM estimates, competitor lists, and pricing benchmarks come from Claude's training data, not live research. They should be validated with actual market research.
- **No web search.** The skill doesn't call external APIs or scrape competitors. Adding an MCP web-search tool would improve accuracy.
- **Quality depends on intake depth.** Shallow answers produce generic ideas. The skill prompts for depth but can't force it.
- **Single-session.** The skill doesn't persist founder profiles across sessions. Running it again requires re-answering intake questions (unless the user saves their profile).
- **No financial modeling.** Revenue projections and pricing are heuristic, not modeled from unit economics.

## Why This Matters

For teams building Claude-driven products:

- **Lead-gen / marketing**: The intake framework is a reusable pattern for any "personalized recommendation" skill — swap business ideas for ad creatives, content strategies, or product recommendations.
- **Agent factories**: The 3-phase structure (intake → generation → deep dive) is a solid template for building multi-step agentic workflows that adapt based on user input.
- **Creator / solopreneur tools**: Demonstrates how Claude can serve as a "co-founder advisor" — a product category with clear willingness to pay.
- **Cross-border / LATAM**: The skill explicitly handles multilingual and cross-border arbitrage scenarios, relevant for global go-to-market planning.

## Source

[Sudiddii/build-DNA](https://github.com/Sudiddii/build-DNA)
