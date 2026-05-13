# algokiller_trace_analysis

**Scan ARM64 execution traces and automatically recover which cipher algorithms a binary uses — AES, DES, ChaCha20, SHA-256, Blowfish — with confidence scores and address ranges.**

The `ak_search` engine pattern-matches known cryptographic signatures (S-box constants, round constants, characteristic instruction sequences) against GumTrace/Frida trace output, producing actionable results in seconds.

## Headline result

```
  [1] AES-128/256
      Confidence: [##################..] 90.0%
      Constants matched: 8  |  Instructions matched: 4
      Address range: 0x7f8a000050 — 0x7f8a0000b8

  [2] ChaCha20
      Confidence: [####################] 100.0%
      Constants matched: 4  |  Instructions matched: 8
      Address range: 0x7f8a000140 — 0x7f8a00017c
```

## Quick start

```bash
bash run.sh
```

No API keys or external services required — runs entirely locally with mock traces.

See [HOW_TO_USE.md](HOW_TO_USE.md) for install/skill setup and [TECH_DETAILS.md](TECH_DETAILS.md) for architecture.

## Source

[icloudza/algokiller-plugin](https://github.com/icloudza/algokiller-plugin) — ARM64 trace evidence analysis & cipher algorithm recovery.
