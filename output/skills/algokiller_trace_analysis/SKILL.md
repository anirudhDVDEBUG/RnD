---
name: algokiller_trace_analysis
description: |
  ARM64 trace evidence analysis and cipher algorithm recovery using the algokiller plugin.
  TRIGGER when: user mentions ARM64 trace analysis, cipher recovery from binary traces, algokiller, ak_search, GumTrace analysis, recovering crypto algorithms from execution traces, or analyzing GB-scale trace files for cipher identification.
  DO NOT TRIGGER when: general reverse engineering without trace analysis, static binary analysis without traces, or non-ARM64 architectures.
---

# AlgoKiller Trace Analysis

Analyze ARM64 execution traces and recover cipher algorithm implementations using the algokiller plugin with its local MCP server and ak_search engine.

## When to use

- "Analyze this ARM64 trace file to find crypto algorithms"
- "Recover the cipher implementation from this GumTrace dump"
- "Search this trace for AES/DES/ChaCha patterns"
- "Identify cryptographic operations in this Frida trace output"
- "Run algokiller on this binary trace to find algorithm evidence"

## How to use

### 1. Setup

Clone and install the algokiller plugin:

```bash
git clone https://github.com/icloudza/algokiller-plugin.git
cd algokiller-plugin
pip install -r requirements.txt
```

Ensure the MCP server is configured in your Claude Desktop settings or Claude Code MCP config to expose the `ak_search` tool.

### 2. Capture a trace (if needed)

Use Frida with GumTrace to capture ARM64 execution traces:

```bash
# Example: attach to a running process and capture trace
frida -U -n <target_app> -l gumtrace.js -o trace_output.log
```

### 3. Analyze traces with ak_search

Once the MCP server is running, use the `ak_search` tool to scan trace files for cipher algorithm evidence:

- **Load a trace file** — Point ak_search at your GB-scale trace file
- **Search for algorithm patterns** — The engine matches known cipher operation sequences (S-box lookups, round constants, key schedule patterns) against the traced instruction flow
- **Review matched algorithms** — Results include confidence scores, matched instruction ranges, and identified algorithm names (AES, DES, Blowfish, ChaCha20, etc.)

### 4. Interpret results

The plugin returns:
- **Algorithm identification** — Which cipher was detected and the confidence level
- **Trace evidence** — Specific instruction sequences and memory access patterns that match known algorithms
- **Address ranges** — Where in the binary the cipher implementation lives
- **Round/key schedule details** — Recovered structural information about the cipher usage

### 5. Tips

- For large trace files (GB-scale), the ak_search engine is optimized for streaming analysis — avoid loading entire files into memory
- Combine with static analysis to cross-reference recovered algorithm addresses with binary symbols
- Use Frida's selective tracing to reduce trace size by focusing on suspected crypto modules

## References

- **Source repository**: https://github.com/icloudza/algokiller-plugin
- **Topics**: ARM64, binary analysis, cryptanalysis, Frida, GumTrace, MCP, reverse engineering, trace analysis
