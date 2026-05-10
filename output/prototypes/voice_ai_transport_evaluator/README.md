# Voice AI Transport Evaluator

**TL;DR:** WebRTC drops audio packets to stay real-time -- great for video calls, disastrous for voice AI where a garbled prompt means a garbage LLM response. This tool scores five transport protocols (WebRTC, WebSocket+Opus, MoQ, gRPC, HTTP/3) across reliability, latency, and browser support to recommend the best fit for your voice AI stack.

## Headline Result

```
  Protocol               Score  Bar                   Verdict
  ────────────────────── ────── ████████████████████  ──────────────
  WebSocket + Opus         8.25  ████████████████░░░░  ★ RECOMMENDED
  gRPC Streaming           7.68  ███████████████░░░░░
  MoQ (Media over QUIC)    7.54  ███████████████░░░░░
  WebRTC                   7.13  ██████████████░░░░░░
  HTTP/3 Streaming         6.98  █████████████░░░░░░░
```

WebRTC ranks **4th out of 5** for voice AI workloads because delivery reliability is weighted 3x -- a dropped audio packet corrupts the entire LLM prompt.

## Quick Start

```bash
bash run.sh
```

No API keys or external dependencies required (Python 3.7+ stdlib only).

## Next Steps

- [HOW_TO_USE.md](HOW_TO_USE.md) -- installation, skill setup, CLI options
- [TECH_DETAILS.md](TECH_DETAILS.md) -- architecture, scoring model, limitations

## Source

Based on [Luke Curley's analysis](https://simonwillison.net/2026/May/9/luke-curley/#atom-everything) of why WebRTC is the wrong choice for LLM voice interfaces, and the [MoQ (Media over QUIC)](https://moq.dev) alternative.
