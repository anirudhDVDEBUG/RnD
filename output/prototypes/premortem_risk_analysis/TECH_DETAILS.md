# Technical Details — Premortem Risk Analysis

## What it does

This is a **prompt-engineering skill** for Claude Code, not a standalone application. The `SKILL.md` file contains structured instructions that Claude follows when triggered. It implements Gary Klein's premortem technique (2007) — "imagine the project has failed, then work backwards to explain why" — combined with Kahneman's outside view (reference class forecasting) to surface risks that in-group optimism typically hides.

The skill orchestrates Claude through a 6-step pipeline: (1) frame the plan from codebase context, (2) prospective hindsight across 5 failure dimensions, (3) multi-agent silent scan using 5 reviewer personas, (4) ranked mitigation triplets, (5) reverse-premortem for hidden assumptions, and (6) a structured markdown snapshot for the project record.

## Architecture

```
SKILL.md (prompt instructions)
  |
  v
Claude Code (LLM execution)
  |
  ├── Step 1: Plan framing (reads codebase/conversation)
  ├── Step 2: Prospective hindsight (5 dimensions)
  │     Technical | Integration | Operational | Human/Process | External/Market
  ├── Step 3: Multi-agent scan (5 personas)
  │     Devil's Advocate | Pessimist | Security Auditor | Ops Engineer | End User
  ├── Step 4: Mitigation triplets (ranked by likelihood x impact)
  ├── Step 5: Reverse-premortem (lucky breaks, scaling assumptions)
  └── Step 6: Markdown snapshot (saveable to docs/)
```

### Key files

| File | Purpose |
|---|---|
| `SKILL.md` | The skill definition — drop into `~/.claude/skills/premortem_risk_analysis/` |
| `premortem_demo.py` | Standalone demo showing the pipeline with mock data (stdlib only) |
| `run.sh` | One-command demo runner |

### Dependencies

- **Skill itself**: Zero dependencies. It's a markdown file that instructs Claude.
- **Demo script**: Python 3.10+ (uses `dataclasses`, `json`, `textwrap` — all stdlib).
- **Model calls**: The skill uses whatever Claude model is running in Claude Code. No additional API calls.

### Data flow

When triggered in Claude Code:
1. Claude reads the skill instructions from `~/.claude/skills/premortem_risk_analysis/SKILL.md`
2. Claude gathers context from the current codebase, open files, and conversation
3. Claude generates the analysis entirely in-context (no external tools or APIs)
4. Output is rendered in the chat and optionally saved to a file

## Limitations

- **No persistent state**: Each premortem is generated fresh. There's no diff between runs or trend tracking across premortems.
- **No external data**: The skill doesn't query incident databases, historical failure rates, or CVE databases. All risk assessment comes from Claude's training data + current context.
- **Quality depends on context**: The more detail you provide about the plan (architecture docs, code, constraints), the more specific the risks. Vague plans get vague risks.
- **Not a replacement for formal risk management**: This is a fast, structured brainstorming tool. It doesn't produce probability distributions, Monte Carlo simulations, or FMEA-grade analysis.
- **Single-model personas**: The "multi-agent scan" uses prompt-based persona switching within a single Claude instance, not actual separate model calls. The diversity of perspectives is simulated, not architecturally enforced.

## Why it matters for Claude-driven products

| Use case | Relevance |
|---|---|
| **Agent factories** | Run premortem before deploying a new agent pipeline — surface failure modes in tool chains, prompt injection risks, and operational gaps before they hit production |
| **Lead-gen / marketing** | Stress-test a new campaign architecture (data pipeline, CRM integration, attribution model) before committing budget |
| **Ad creatives** | Premortem on A/B test designs — find confounds, audience segment risks, and measurement blind spots |
| **Voice AI** | Identify failure modes in voice agent flows (latency spikes, ASR misrecognition cascades, fallback handling) before launch |
| **Any Claude Code project** | Built-in decision hygiene — ask "what could go wrong" before any major commit, migration, or architecture change |

The core value: **structured pessimism before commitment**. Teams using premortems surface 30% more risks than traditional prospective risk assessment (Klein 2007). As a Claude Code skill, it's zero-friction — just say "premortem" and get a ranked risk report in seconds.
