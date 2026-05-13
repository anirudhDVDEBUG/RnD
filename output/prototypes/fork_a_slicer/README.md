# Fork-a-Slicer: Process Isolation Bridge Demo

**TL;DR** — Demonstrates the FULU-Foundation architecture for forking OrcaSlicer and adding Bambu Lab printer support through a process-isolated JSON-RPC bridge. The bridge runs as a separate process, keeping proprietary protocol handling cleanly separated from the slicer.

## Headline Result

```
Found 3 Bambu Lab printers via network discovery
  [X1 Carbon   ] BambuLab X1C - Workshop     192.168.1.42
  [P1S         ] BambuLab P1S - Office        192.168.1.87
  [A1          ] BambuLab A1 - Prototyping    192.168.1.103   (printing 47%)

Print job JOB-38201 submitted to BambuLab X1C - Workshop
```

Two separate OS processes (slicer + bridge) communicate over a Unix socket using JSON-RPC 2.0 — no proprietary code inside the slicer.

## Quick Start

```bash
bash run.sh
```

No API keys or external dependencies required (Python 3.8+ stdlib only).

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Installation, skill setup, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, relevance to Claude-driven products

## Source

[danielcherubini/fork-a-slicer](https://github.com/danielcherubini/fork-a-slicer) — AI-agent-driven plans for forking OrcaSlicer with Bambu Lab support via process isolation.
