---
description: Run TrendForge Mode B research on a topic.
---

You are running TrendForge Mode B research.

The user's topic is: $ARGUMENTS

Execute:

```bash
cd ~/trendforge && PYTHONPATH=. python3 -m trendforge.research \
  --topic "$ARGUMENTS" \
  --depth standard
```

Stream the output. When the dossier completes, summarize what was
produced (slides count, key findings, recommended demo concept) and
offer to open `slides.pptx` or run the working demo in a fresh terminal.

To install: copy this file to `~/.claude/commands/research.md`.
