# How to Use

## Install (this demo)

```bash
# Python 3.8+ required, no pip dependencies
git clone <this-repo>
cd algokiller_trace_analysis
bash run.sh
```

## Install the real algokiller plugin

```bash
git clone https://github.com/icloudza/algokiller-plugin.git
cd algokiller-plugin
pip install -r requirements.txt
```

## As a Claude Skill

Drop the skill folder into your Claude skills directory:

```bash
mkdir -p ~/.claude/skills/algokiller_trace_analysis
cp SKILL.md ~/.claude/skills/algokiller_trace_analysis/SKILL.md
```

**Trigger phrases** that activate the skill:
- "Analyze this ARM64 trace file to find crypto algorithms"
- "Recover the cipher implementation from this GumTrace dump"
- "Search this trace for AES/DES/ChaCha patterns"
- "Identify cryptographic operations in this Frida trace output"
- "Run algokiller on this binary trace to find algorithm evidence"

## As an MCP Server

Add this to your `~/.claude.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "algokiller": {
      "command": "python3",
      "args": ["/path/to/algokiller-plugin/mcp_server.py"],
      "env": {
        "AK_TRACE_DIR": "/path/to/your/traces"
      }
    }
  }
}
```

This exposes the `ak_search` tool to Claude, which accepts a trace file path and returns algorithm matches.

## First 60 seconds

**Input:** A GumTrace log file from Frida (ARM64 instructions with addresses).

```
0x7f8a000050  MOV W0, #0x63
0x7f8a000054  MOV W1, #0x7C
0x7f8a000058  TBL V0.16B, {V1.16B}, V2.16B
0x7f8a00005c  AESE V0.16B, V1.16B
0x7f8a000060  AESMC V0.16B, V0.16B
```

**Run:**

```bash
python3 ak_search.py sample_traces/aes_chacha_trace.log
```

**Output:**

```
======================================================================
  ak_search — ARM64 Cipher Algorithm Recovery Results
======================================================================

  Detected 2 algorithm(s):

  [1] AES-128/256
      AES (Rijndael) block cipher
      Confidence: [##################..] 90.0%
      Constants matched: 8  |  Instructions matched: 4
      Address range: 0x7f8a000050 — 0x7f8a0000b8

      Evidence (top hits):
        L   17  0x7f8a000050  [CONST]  MOV W0, #0x63
        L   18  0x7f8a000054  [CONST]  MOV W1, #0x7C
        ...

  [2] ChaCha20
      ChaCha20 stream cipher (Bernstein)
      Confidence: [####################] 100.0%
      ...
```

**JSON output:**

```bash
python3 ak_search.py sample_traces/des_sha256_trace.log --format json
```

Returns structured JSON with `matches[]`, each containing `algorithm`, `confidence`, `address_range`, and `evidence_sample`.
