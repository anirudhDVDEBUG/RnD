# How to Use Tokenless Context Compression

## Installation

### Option A: Global install (recommended)
```bash
npm install -g tokenless
```

### Option B: Per-project
```bash
npm install tokenless
```

### Option C: One-shot via npx
```bash
npx tokenless
```

Requires Node.js >= 16.

---

## Claude Code Skill Setup

Tokenless is also available as a **Claude Code Skill**. To install:

1. Create the skill directory:
   ```bash
   mkdir -p ~/.claude/skills/tokenless_context_compression
   ```

2. Copy the `SKILL.md` file into that directory:
   ```bash
   cp SKILL.md ~/.claude/skills/tokenless_context_compression/SKILL.md
   ```

3. **Trigger phrases** that activate the skill in Claude Code:
   - "reduce tokens"
   - "token optimization"
   - "compress context"
   - "cut token usage"
   - "tokenless"
   - "save tokens"

Once installed, saying any trigger phrase in Claude Code will invoke the skill, which runs `npx tokenless` in your project directory.

---

## First 60 Seconds

### 1. Run the demo (no install needed)
```bash
bash run.sh
```

**Input:** The bundled `sample_project/` containing a verbose Express server, a Python utility module, and a YAML config — all intentionally over-commented.

**Output:**
```
======================================================================
  TOKENLESS CONTEXT COMPRESSION — DEMO
======================================================================

Scanning: ./sample_project

----------------------------------------------------------------------
File                          Original  Compressed     Saved       %
----------------------------------------------------------------------
server.js                         648         312       336    51.9%
utils.py                          826         401       425    51.5%
config.yaml                       368         210       158    42.9%
----------------------------------------------------------------------

SUMMARY
  Files scanned:     3
  Original tokens:   1,842
  Compressed tokens: 923
  Tokens saved:      919
  Savings:           49.9%  [###############---------------]
```

### 2. Run on your own project
```bash
cd /path/to/your/project
npx tokenless
```

Tokenless scans all source files (JS, TS, Python, Go, Rust, YAML, etc.), applies 5 compression passes, and outputs a compressed context representation. The compressed output is what gets fed into Claude's context window instead of the raw source.

### 3. Verify savings
Check the summary report. Typical savings:
- **Heavily commented code:** 45-60% reduction
- **Standard production code:** 25-40% reduction
- **Already-minimal code:** 10-20% reduction

---

## What It Does NOT Do

- Does **not** modify your source files (read-only)
- Does **not** require an API key
- Does **not** send any data externally
- Does **not** change code behavior — only the context representation
