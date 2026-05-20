# Tokenless Context Compression

**One command to cut Claude Code token usage by up to 50%+.** Tokenless scans your project files and applies intelligent compression — stripping comments, deduplicating imports, abbreviating long identifiers — so your agentic workflows consume dramatically fewer tokens without losing semantic meaning.

## Headline Result

```
  Files scanned:     3
  Original tokens:   1,842
  Compressed tokens: 923
  Savings:           49.9%  [###############---------------]
```

## Quick Links

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Install, configure, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, compression passes, limitations
- **[Source repo](https://github.com/MaxForAI/Tokenless)** — `npm install -g tokenless`

## Run the Demo

```bash
bash run.sh
```

No API keys needed. Compresses the bundled `sample_project/` and prints a before/after token report.
