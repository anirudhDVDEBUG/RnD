# LLM Shebang Scripts

**Turn plain-text prompts into executable programs.** Using Simon Willison's `llm` CLI in the shebang line (`#!/usr/bin/env -S llm -f`), any text file becomes a runnable script — no wrapper code, no boilerplate, just a prompt you can `chmod +x` and execute.

## Headline Result

```
$ cat hello.sh
#!/usr/bin/env -S llm -f
Generate an SVG of a pelican riding a bicycle

$ chmod +x hello.sh && ./hello.sh
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <circle cx="100" cy="80" r="30" fill="#f5a623" />
  ...
</svg>
```

A two-line file that produces SVG art. No Python imports, no SDK setup, no main function.

## Quick Start

```bash
bash run.sh          # full demo with mock data, no API keys needed
```

## What's Inside

| File | Purpose |
|---|---|
| `examples/` | 5 ready-to-run shebang scripts (fragment + template modes) |
| `shebang_builder.py` | CLI to create and validate shebang scripts |
| `shebang_simulator.py` | Mock runner that demos scripts without the llm CLI |
| `run.sh` | End-to-end demo |

## Next Steps

- [HOW_TO_USE.md](HOW_TO_USE.md) — install the real `llm` CLI and run these for real
- [TECH_DETAILS.md](TECH_DETAILS.md) — architecture, limitations, and why this matters
