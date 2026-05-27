# Technical Details — AI Video Production Kit

## What It Does

The AI Video Production Kit is an enterprise-oriented toolkit for AI video generation workflows. The upstream repo (`cclank/lanshu-awesome-ai-video-kit`) contains 411+ battle-tested prompts, coverage of 15 models, 7 Claude Skills, and 14 methodology articles — all born from real production work at Lanshu (蓝数) doing enterprise AI video projects.

This prototype distills the core engine: a **5-layer prompt generator** and a **scoring model selector** that takes a video brief (subject, action, style, platform, budget) and outputs an optimized prompt plus ranked model recommendations. No API keys or external services are needed for the demo.

## Architecture

```
video_prompt_engine.py          # Single-file implementation
├── VideoModel dataclass        # 12 models with metadata (strengths, cost, ratios, etc.)
├── CAMERA_MOVES                # 15 camera movement templates
├── STYLES                      # 8 style presets (cinematic, commercial, noir, etc.)
├── MOTION_INTENSITIES          # 5 intensity levels (static → extreme)
├── VideoBrief dataclass        # Input: subject, action, style, budget, platform, etc.
├── generate_prompt(brief)      # → 5-layer structured prompt + negative prompt
├── select_model(brief)         # → scored & ranked model list
├── run_demo()                  # 4 pre-built scenarios
└── interactive_mode()          # CLI prompt builder

SKILL.md                        # Claude Code skill definition (drop into ~/.claude/skills/)
run.sh                          # Entry point
```

### Data Flow

```
User brief → VideoBrief → generate_prompt() → 5-layer prompt string
                        → select_model()    → ranked [(model, score)] list
```

### Scoring Logic (select_model)

Each model is scored on a point system:
- **Duration fit** (+20 if model supports requested length, -30 if not)
- **Aspect ratio match** (+15)
- **Budget alignment** (+15 if within budget, penalty per tier over)
- **Use-case overlap** (+10 per matching category)
- **Platform bonus** (+5 for ratio/platform fit)
- **Style affinity** (+8 for cinematic/creative match)
- **Feature bonus** (+5 if negative prompts supported and requested)

## Key Dependencies

- **Python 3.10+** (for `list[str]` syntax in dataclass annotations)
- **No external packages** — uses only `json`, `random`, `sys`, `textwrap`, `dataclasses`, `typing`

## Limitations

- **No actual API calls**: This is a prompt engineering and model selection tool, not a video generation API wrapper. It produces prompts you paste into each model's interface or API.
- **Static model data**: Model capabilities, pricing, and availability change frequently. The database here is a snapshot; the upstream repo is updated more regularly.
- **English-focused prompts**: While the upstream repo has strong Chinese-language prompt coverage, this prototype generates English prompts only.
- **No image-to-video**: The prompt engine handles text-to-video only. Many models also support image-to-video (img2vid) with different prompt strategies.
- **No quality evaluation**: It recommends models and generates prompts but does not evaluate or compare output quality.

## Why This Matters for Claude-Driven Products

| Use Case | Relevance |
|---|---|
| **Ad Creatives / Lead-Gen** | Generate video ad prompts at scale — feed briefs from campaign data, get model-optimized prompts for each platform (TikTok vertical, YouTube landscape). |
| **Marketing Automation** | Batch prompt generation for content calendars. The 5-layer structure is deterministic enough to template but flexible enough for variety. |
| **Agent Factories** | The model selector is a decision engine — wrap it as a tool in an agent pipeline that automates the full script→prompt→generate→review loop. |
| **Enterprise Video Pipelines** | The production pipeline pattern (script breakdown → prompt batch → model assignment → generate → post) maps directly to orchestration agents. |
| **Claude Skills Ecosystem** | Demonstrates a well-structured Claude Skill with clear triggers, structured output, and domain expertise — a pattern for building vertical skills. |
