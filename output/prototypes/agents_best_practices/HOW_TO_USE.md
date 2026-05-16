# How to Use

## This is a Claude Code Skill

It installs as a local skill folder — no pip packages, no npm modules, no API keys.

## Install (30 seconds)

```bash
# Clone the source repo
git clone https://github.com/DenisSergeevitch/agents-best-practices.git

# Copy the skill into Claude Code's skill directory
mkdir -p ~/.claude/skills/agents_best_practices
cp agents-best-practices/SKILL.md ~/.claude/skills/agents_best_practices/SKILL.md
```

Or manually create `~/.claude/skills/agents_best_practices/SKILL.md` and paste the skill content from the source repo.

## Trigger Phrases

Once installed, Claude Code activates this skill when you say things like:

- "What are best practices for building AI agents?"
- "How should I structure an agentic workflow?"
- "Help me design a multi-agent system"
- "What prompt engineering patterns work best for agents?"
- "How do I integrate MCP servers into my agent architecture?"

No slash command needed — Claude Code matches intent automatically.

## First 60 Seconds

**Input** (type in Claude Code):
```
What workflow pattern should I use for a content pipeline that researches,
writes, edits, and publishes blog posts?
```

**Output** (Claude Code responds with skill-informed guidance):
```
For a content pipeline with ordered stages (research → write → edit → publish),
use the Sequential Pipeline pattern:

1. Research Agent — gathers sources, outputs structured notes
2. Writer Agent — takes notes, produces draft (structured JSON output)
3. Editor Agent — iterative refinement loop until quality threshold met
4. Publisher Agent — final formatting and deployment

Key practices to apply:
- Input validation at each agent boundary
- Structured output (JSON) between agents for reliable parsing
- Human-in-the-loop checkpoint before publish stage
- Observability: log each agent's input/output for debugging
```

## Running the Demo Locally

The included `run.sh` demonstrates the patterns programmatically:

```bash
bash run.sh
```

This runs a Python simulation of all five workflow patterns with mock agents, showing structured input/output at each stage. No API keys required.

## Verification

After installing the skill, verify it's loaded:

```bash
ls ~/.claude/skills/agents_best_practices/SKILL.md
```

Then open Claude Code and ask any trigger phrase — the response quality should noticeably improve for agent architecture questions.
