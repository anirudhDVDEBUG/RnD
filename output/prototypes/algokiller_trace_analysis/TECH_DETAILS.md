# Technical Details

## What it does

The algokiller plugin scans ARM64 execution traces (captured via Frida/GumTrace) and identifies which cryptographic algorithms a binary implements at runtime. It works by matching two categories of evidence against a signature database:

1. **Constant matching** — Known magic values that ciphers embed: AES S-box bytes (`0x63, 0x7C, 0x77...`), ChaCha20's "expand 32-byte k" constants (`0x61707865...`), SHA-256 round constants (`0x428A2F98...`), DES permutation tables, Blowfish P-array digits of pi.

2. **Instruction pattern matching** — Characteristic ARM64 instruction sequences: `AESE/AESMC` pairs for hardware AES, `ROR` with rotation amounts 16/12/8/7 for ChaCha20 quarter-rounds, `SHA256H/SHA256SU0` for SHA-256 crypto extensions, 6-bit masking (`AND #0x3F`) for DES S-boxes.

Confidence scoring is a weighted average: 50% constant hit ratio + 50% instruction hit ratio, with per-algorithm minimum thresholds to avoid false positives.

## Architecture

```
generate_mock_trace.py   — Creates synthetic ARM64 traces with embedded cipher evidence
ak_search.py             — Core analysis engine (CLI + importable module)
  CIPHER_SIGNATURES      — Dict of algorithm fingerprints (constants + instruction regexes)
  parse_trace_line()     — Parses GumTrace format: "0xADDR  INSTRUCTION"
  extract_immediates()   — Pulls hex/decimal values from instruction operands
  scan_trace()           — Main loop: checks each line against all signatures
  format_results()       — Text or JSON output formatter
  analyze_file()         — File I/O wrapper
run.sh                   — End-to-end demo: generate traces, analyze both, show results
```

**Data flow:** Trace file (text lines) -> line parser -> per-line constant + pattern matching -> per-algorithm score aggregation -> sorted results.

**Dependencies:** Python 3.8+ stdlib only (`re`, `json`, `dataclasses`, `argparse`). No ML models, no network calls, no external packages.

The real algokiller-plugin adds an MCP server layer (`mcp_server.py`) that wraps `ak_search` as a tool callable by Claude Desktop, plus streaming support for GB-scale trace files.

## Limitations

- **Signature-based only** — detects known algorithms by their constants and instruction patterns. Custom or obfuscated ciphers won't match. No heuristic or ML-based detection.
- **ARM64 only** — instruction patterns are written for AArch64. x86/MIPS traces won't match the instruction regexes (constants may still match).
- **No control flow analysis** — treats the trace as a flat instruction stream. Cannot distinguish crypto code from coincidental constant usage in non-crypto code (though threshold tuning reduces false positives).
- **Demo uses mock data** — the synthetic traces are representative but simplified. Real GumTrace output has additional metadata, thread IDs, and memory access annotations.
- **No Frida integration** — this demo doesn't capture live traces. The real plugin assumes you've already captured a trace file via Frida + GumTrace.

## Why it matters for Claude-driven products

- **Security agent factories** — An agent that takes an APK, instruments it with Frida, captures a trace, runs ak_search, and reports which ciphers the app uses. Useful for compliance audits, vulnerability assessments, or competitive intelligence on mobile apps.
- **Reverse engineering assistants** — Claude can invoke ak_search via MCP to answer questions like "what crypto does this binary use?" without the analyst manually inspecting millions of trace lines.
- **Automated pen-testing pipelines** — Combine with other MCP tools (disassemblers, decompilers) to build end-to-end binary analysis workflows driven by Claude.
- **Pattern for specialized search** — The architecture (signature DB + streaming match + confidence scoring) is reusable beyond crypto: detect anti-tampering, DRM schemes, protocol implementations, or any behavior identifiable by instruction/constant fingerprints.
