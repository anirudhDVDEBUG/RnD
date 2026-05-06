# Technical Details

## What It Does

The analyzer reads `git log` output from any repository and classifies each commit as AI-assisted or manual by scanning for known signatures: `Co-authored-by` trailers (Claude, Copilot, Cursor, Codex), tool-specific message patterns, and keyword markers. It then calculates productivity multipliers using two independent methods -- a top-down role-allocation model and a bottom-up LOC-per-commit comparison -- and averages them into a combined estimate.

The upstream project also includes a Jupyter notebook for visualization and an optional Claude Code subagent that reads actual diffs to classify commits with higher accuracy (requires an Anthropic API key).

## Architecture

```
analyze.py          -- CLI entry point, single-file analyzer
  |
  +-- run_git_log() -- shells out to `git log --numstat`, parses output
  +-- detect_ai_tool() -- regex matching against AI_SIGNATURES dict
  +-- calc_top_down() -- role-allocation multiplier formula
  +-- calc_bottom_up() -- LOC-per-commit ratio
  +-- format_report() -- human-readable text output
  +-- run_demo() -- generates mock data for no-repo demos
```

### Key files

| File | Purpose |
|------|---------|
| `analyze.py` | Complete analyzer (git parsing, detection, multiplier calc, reporting) |
| `run.sh` | End-to-end demo: mock data + live repo analysis |
| `requirements.txt` | Stdlib only for core; optional deps listed for upstream features |

### Data flow

1. `git log --format=... --numstat` produces commit metadata + line counts
2. Each commit message is matched against `AI_SIGNATURES` regex patterns
3. Commits are bucketed into AI-assisted vs manual
4. Two multiplier formulas are applied independently
5. Results output as text table or JSON

### Detection signatures

| Tool | Signal | Confidence |
|------|--------|------------|
| Claude Code | `Co-authored-by: *Claude*` or `Co-Authored-By: *Anthropic*` | 0.95 |
| GitHub Copilot | `Co-authored-by: *Copilot*` | 0.95 |
| Cursor | `Co-authored-by: *Cursor*` or `Generated.*Cursor` trailer | 0.80-0.95 |
| OpenAI Codex | `Co-authored-by: *Codex*` or `Co-authored-by: *OpenAI*` | 0.95 |
| Any (weak) | Conventional commit format `feat(scope):` | 0.40 |

### Dependencies

- **Python 3.10+** (stdlib only: `subprocess`, `re`, `json`, `argparse`, `dataclasses`)
- **git** on PATH
- No API keys for core analysis
- Optional: `anthropic` SDK for subagent diff classification (upstream feature)

## Limitations

- **Signature-based detection only** -- if a developer uses AI but doesn't include Co-authored-by trailers, commits are classified as manual. False negatives are common for Copilot (inline suggestions rarely add trailers).
- **Conventional commits are weak signal** -- the `feat(scope):` pattern triggers a 0.40 confidence match for Claude, but many teams use conventional commits without AI. Filter these out with `--since` to focus on the AI adoption period.
- **LOC != productivity** -- the bottom-up multiplier assumes more lines = more output. Refactoring commits that reduce LOC are not captured well.
- **No diff-level analysis** in this prototype -- the upstream repo's subagent mode reads actual diffs via Claude API for higher accuracy, but requires an API key.
- **Single-repo scope** -- does not aggregate across multiple repositories or CI/CD pipelines.

## Why It Matters for Claude-Driven Products

| Use case | Relevance |
|----------|-----------|
| **Agent factories** | Quantify the ROI of adding AI coding agents to your pipeline. Show clients a concrete multiplier. |
| **Lead-gen / marketing** | "Our team ships 2.3x faster with Claude Code" -- backed by actual git data, not vibes. |
| **Ad creatives** | Use real before/after productivity numbers in ad copy for developer tools. |
| **Voice AI / support** | Less directly relevant, but the pattern of commit-signature detection transfers to detecting AI-generated support responses. |
| **Internal tooling** | Track AI adoption across engineering teams; identify who's getting the most leverage and share their patterns. |
