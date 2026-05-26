# Technical Details

## What It Actually Does

This skill injects Yang Tao's cognitive frameworks into Claude's system context when triggered. It doesn't call external APIs or run separate models — it's a structured prompt that guides Claude to analyze business scenarios through Yang Tao's specific mental models: accumulation thinking (积累思维), grassroots monetization paths (平民创业路径), personal IP construction principles, and content-to-trust pipelines.

The Python demo (`yangtao_engine.py`) is a standalone template engine that applies these same frameworks offline using pattern matching and structured output — useful for batch analysis or integration into pipelines without LLM calls.

## Architecture

```
~/.claude/skills/yangtao-perspective/
└── SKILL.md              # Prompt injection point — loaded by Claude Code runtime

yangtao_engine.py         # Standalone framework engine (no LLM needed)
├── FrameworkEngine       # Core class — maps input to applicable frameworks
├── FRAMEWORKS dict       # 5 cognitive lenses with scoring rubrics
├── analyze()             # Entry point — returns structured analysis
└── format_output()       # Terminal-friendly formatted display

run.sh                    # Demo runner — 3 sample scenarios
requirements.txt          # Zero external deps (stdlib only)
```

### Data Flow

1. User input (business scenario text) enters `analyze()`
2. Keyword extraction identifies relevant frameworks (e.g., "community" triggers Trust Currency + Content Pipeline)
3. Each matched framework generates structured assessment with scores and recommendations
4. Output formatted as: Sharp Insight → Framework Scores → Action Steps

### Dependencies

- Python 3.8+ (stdlib only — no pip packages required)
- For the Claude skill: Claude Code with skills directory support

### Model Calls

- **Skill mode (in Claude Code):** Zero additional API calls — the skill modifies Claude's reasoning via prompt context
- **Standalone engine:** Zero model calls — pure template/rule-based analysis

## Limitations

- **Not a fine-tuned model:** The skill guides Claude's reasoning but doesn't contain Yang Tao's actual 9.7M characters of writing. It distills patterns, not data.
- **Chinese business context:** Frameworks are rooted in Chinese internet entrepreneurship (WeChat ecosystems, Xiaohongshu, Douyin). May need adaptation for Western markets.
- **No real-time data:** Cannot pull current market prices, trending topics, or competitor analysis.
- **Template engine is simplified:** The Python demo uses keyword matching, not semantic understanding. It demonstrates structure, not depth.
- **Authorization scope:** Authorized for educational/analytical use of Yang Tao's thinking patterns, not reproduction of his original content.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|----------|-----------|
| **Lead-gen** | Yang Tao's trust-first framework maps directly to lead nurturing sequences — the skill can generate acquisition strategies grounded in "accumulation thinking" |
| **Marketing** | Content-to-business pipeline framework is immediately applicable to content marketing strategy for any Claude-powered product |
| **Agent factories** | The cognitive OS pattern (structured thinking frameworks as prompts) is a reusable architecture for building domain-expert agents |
| **Ad creatives** | "Sharp contrarian insight" opening pattern is a proven hook format for ad copy — the skill generates these structurally |
| **Personal IP / Creator economy** | Direct application — the entire skill is built for this domain |

The broader pattern here: **distilling a real expert's cognitive framework into a reusable prompt skill** is a template for building vertical AI agents. If you can do this for Yang Tao, you can do it for any domain expert with sufficient public output.
