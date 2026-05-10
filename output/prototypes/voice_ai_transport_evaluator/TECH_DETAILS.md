# Technical Details

## What it does

The Voice AI Transport Evaluator is a decision-support tool (Claude Code skill + CLI) that scores five audio transport protocols across six dimensions weighted for voice AI workloads. It encodes the key insight from Luke Curley's analysis: WebRTC's aggressive packet-dropping strategy, designed for human-to-human calls, becomes a liability when streaming audio to LLMs -- because a garbled prompt produces a garbage response, and the extra 100-200ms of reliable delivery is negligible compared to LLM inference time.

As a Claude Code skill, it provides structured reasoning when developers ask "which protocol should I use for my voice AI app?" As a CLI tool, it produces scored comparison tables and JSON output that can feed into architecture decision records.

## Architecture

### Key files

| File | Purpose |
|------|---------|
| `evaluator.py` | Core scoring engine, protocol database, CLI entry point |
| `SKILL.md` | Claude Code skill definition with trigger phrases and evaluation framework |
| `run.sh` | One-command demo runner |

### Data flow

```
User question / CLI args
        │
        ▼
┌─────────────────────┐
│  Scenario Selection  │  (voice_ai_default / browser_first / server_to_server)
│  → weight vector     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Protocol Database   │  5 protocols × 6 dimensions (hard-coded scores 0-10)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Weighted Scoring    │  score = Σ(dimension_score × weight) / Σ(weights)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Ranked Output       │  Table + detail cards (CLI) or JSON
└─────────────────────┘
```

### Scoring model

Each protocol has a score (0-10) on six dimensions:

- **Delivery Reliability** -- Does every audio packet arrive? (weight: 3.0x for voice AI)
- **Latency** -- End-to-end delay (weight: 1.5x)
- **Browser Support** -- Works in-browser without plugins? (weight: 1.0x)
- **Implementation Ease** -- Setup complexity (weight: 1.0x)
- **Bidirectional** -- Full-duplex audio support (weight: 1.2x)
- **Scalability** -- Concurrent session handling (weight: 1.0x)

The weighted score formula: `score = sum(dim_score * dim_weight) / sum(all_weights)`

Different scenarios adjust the weight vector. The `browser_first` scenario bumps browser support to 3.0x; the `server_to_server` scenario sets browser support to 0.0x.

### Dependencies

- Python 3.7+ standard library only (dataclasses, json, argparse)
- No external packages, no API keys, no network calls

## Limitations

- **Scores are editorial, not measured.** The 0-10 scores reflect the author's assessment based on Luke Curley's analysis and general industry knowledge. They are not derived from benchmarks.
- **Static protocol database.** New protocols or updated scores require editing `evaluator.py`. There is no plugin system or external data source.
- **No actual audio testing.** This tool evaluates protocols on paper -- it does not send audio packets or measure real latency/loss.
- **Five protocols only.** Does not cover every option (e.g., raw UDP, SRT, RTMP, custom QUIC implementations).
- **Weight tuning is manual.** Users can create custom scenarios by editing the code, but there is no interactive weight-tuning UI.

## Why it matters for Claude-driven products

**Voice AI builders** choosing a transport protocol is a high-stakes architectural decision that's hard to reverse. This tool (and the underlying SKILL.md) gives Claude the structured reasoning to guide that choice correctly -- steering developers away from WebRTC's hidden failure mode before they discover it in production.

Relevant domains:
- **Voice AI / Agent Factories**: Any product streaming user speech to an LLM backend needs reliable delivery. This skill prevents the most common architectural mistake.
- **Ad creative / Marketing voice-overs**: Voice generation pipelines that use LLM-driven scripts benefit from understanding transport reliability for real-time preview flows.
- **Lead-gen voice bots**: Conversational AI over phone/web where dropped words mean lost leads.

## References

- [Luke Curley -- OpenAI's WebRTC Problem](https://moq.dev/blog/webrtc-is-the-problem/)
- [Simon Willison's commentary](https://simonwillison.net/2026/May/9/luke-curley/#atom-everything)
- [OpenAI -- Delivering low-latency voice AI at scale](https://openai.com/index/delivering-low-latency-voice-ai-at-scale/)
- [MoQ (Media over QUIC)](https://moq.dev)
