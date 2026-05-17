# Chinese Technical Writing Agent Skill — Postmortem

A Claude Code skill that enforces Chinese internal technical writing conventions
for postmortem/incident-review documents: objective tone, short sentences,
quantified impact, 5-Whys root cause chains, and actionable improvement items.

## Headline Result

```
❌ [no-blame] L4: 避免带有情绪色彩的形容词
❌ [required-sections] 全局: 缺少必要章节：影响范围, 根因分析, 改进项, 经验教训
⚡ [sentence-length] L4: 句子过长（87 字），建议拆分为短句（≤30 字/句）
```

Drop the skill into Claude Code and it will rewrite sloppy incident reports into
structured, blameless, data-driven postmortems — in Chinese.

## Quick Links

- [HOW_TO_USE.md](./HOW_TO_USE.md) — Installation & first 60 seconds
- [TECH_DETAILS.md](./TECH_DETAILS.md) — Architecture & limitations
