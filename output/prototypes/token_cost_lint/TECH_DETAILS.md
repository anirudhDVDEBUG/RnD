# Technical Details — Token Cost Lint

## What It Does

Token Cost Lint is a static analysis tool that scans Python/JS/TS/YAML/MD files in a project directory and identifies patterns that cause unnecessary token consumption in LLM-based multi-agent systems. It uses regex pattern matching and heuristic rules — no LLM calls — to classify findings into a 10-category taxonomy with 31 specific sub-patterns.

The tool estimates wasted tokens per finding, aggregates waste by category and severity (critical/high/medium/low), and generates prioritized fix recommendations. It's designed for teams running multi-agent Claude Code harnesses where token spend is a real cost center.

## Architecture

```
audit.py          Main CLI + AuditEngine class (detection logic + formatters)
taxonomy.py       10-category x 31 sub-pattern definitions with regex patterns
sample_project/   Demo target with intentional waste patterns for all 10 categories
run.sh            End-to-end demo script
```

**Data flow:**
1. `collect_files()` walks the target directory, skipping `node_modules`, `.git`, etc.
2. All files are read into memory with rough token estimates (chars / 4).
3. Ten detection methods run sequentially, each scanning all file contents with regex patterns and heuristic rules.
4. Findings are collected with category, sub-pattern, file, line, message, estimated waste, and severity.
5. Output is formatted as either a terminal report or JSON.

**Dependencies:** Python 3.10+ stdlib only (`re`, `json`, `os`, `pathlib`, `collections`, `argparse`). Zero external packages.

**Model calls:** None. The entire audit is static analysis. This is the core value proposition — the linter costs zero tokens to run.

## The 10 Categories

| # | Category | Sub-patterns | Key detection method |
|---|----------|-------------|---------------------|
| 1 | Redundant Context | 3 | Track file read targets across files, flag duplicates |
| 2 | Oversized Prompts | 4 | Regex for boilerplate phrases, role re-definitions, long lines |
| 3 | Unbounded History | 3 | Find `messages.append()` without corresponding truncation |
| 4 | Duplicate Tool Results | 3 | Count `tool_call()` invocations, check for caching |
| 5 | Verbose Output | 3 | Detect input-echo patterns ("You asked", "Let me repeat") |
| 6 | Unnecessary Re-reads | 2 | Track `open()` / `read_file()` targets within single files |
| 7 | Broad File Inclusion | 3 | Flag `**/*` globs and unrestricted `node_modules` refs |
| 8 | Uncompressed Examples | 3 | Count example markers, flag when >3 |
| 9 | Idle Agent Overhead | 3 | Flag short agent delegations (likely trivial tasks) |
| 10 | Retry Amplification | 3 | Find retry loops without context reduction |

## Limitations

- **Heuristic, not precise.** Token waste estimates are rough (chars/4). Real tokenization varies by model.
- **Pattern-based.** Regex can produce false positives (e.g., "You asked" in a comment vs. actual output). It can also miss patterns that don't match the expected code style.
- **Single-file scope.** Cross-file data flow analysis is limited to file-read tracking. It doesn't trace variables or follow imports.
- **No runtime analysis.** It audits source code, not actual API call logs. A function that reads a file 10 times in a loop shows as 1 finding, not 10.
- **Python/JS focused.** Detection patterns are tuned for Python and JavaScript/TypeScript codebases. Other languages will get partial coverage.

## Why It Matters

For teams building Claude-driven products — lead-gen bots, marketing automation, ad creative pipelines, agent factories, voice AI — token cost is a scaling bottleneck. A multi-agent harness with 5 agents passing 4K context each can burn 20K+ tokens per user interaction. If 20% of that is waste (duplicate reads, bloated prompts, unbounded history), that's 4K tokens saved per interaction — which compounds to significant cost reduction at scale.

This tool gives you a zero-cost way to find that waste before it hits your API bill.
