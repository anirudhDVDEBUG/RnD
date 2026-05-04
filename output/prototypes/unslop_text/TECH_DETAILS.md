# Technical Details — Unslop Text

## What it does

Unslop is a regex-based text cleaner that identifies and removes AI-generated "slop" — the predictable filler words, hollow adjectives, and cliched phrases that LLMs (especially ChatGPT) overuse. It works in four passes over the input text, progressively stripping slop while preserving meaning. No model calls, no API keys — pure pattern matching.

Based on the slop patterns catalogued by [MohamedAbdallah-14/unslop](https://github.com/MohamedAbdallah-14/unslop) and extended with additional categories.

## Architecture

**Single file: `unslop.py`** (~230 lines, zero dependencies)

### Data flow

```
Input text
  -> Pass 1: Delete cliched phrases (25+ regex patterns)
  -> Pass 2: Remove filler adverbs (21 words)
  -> Pass 3: Strip hollow adjectives (22 words)
  -> Pass 4: Word replacements (leverage->use, utilize->use, etc.)
  -> Cleanup: collapse whitespace, fix orphan punctuation
  -> UnslopResult (cleaned text + match metadata)
```

### Key components

| Component | Description |
|-----------|-------------|
| `DELETE_PHRASES` | 30+ regex patterns for phrases to remove entirely ("It's worth noting that", "Let's dive deep", sycophantic openers, hollow conclusions) |
| `FILLER_ADVERBS` | 21 adverbs that add no meaning ("seamlessly", "fundamentally", "incredibly") |
| `HOLLOW_ADJECTIVES` | 22 adjectives that are vague praise ("groundbreaking", "cutting-edge", "robust") |
| `WORD_REPLACEMENTS` | Dict mapping inflated words to plain English ("leverage" -> "use", "empower" -> "help") |
| `unslop()` | Main function, returns `UnslopResult` with `.cleaned`, `.slop_count`, `.reduction_pct`, `.matches` |
| `format_report()` | Human-readable report with categorized findings |

### Dependencies

None. Python 3.10+ standard library only (`re`, `json`, `sys`, `argparse`, `dataclasses`).

## Limitations

- **Regex-only**: No semantic understanding. Will remove "groundbreaking" even when something is literally groundbreaking. Context-blind.
- **English only**: All patterns are English-language.
- **False positives**: Words like "robust" and "comprehensive" have legitimate uses in technical writing. The tool doesn't distinguish.
- **No sentence restructuring**: When removing a filler phrase leaves an awkward sentence, the tool doesn't rewrite — it just deletes and collapses whitespace.
- **Not a style guide**: Doesn't improve writing quality beyond slop removal. Won't fix bad structure, weak arguments, or factual issues.
- **Static word lists**: The slop vocabulary is hardcoded. New AI-isms that emerge won't be caught until the lists are updated.

## Why it matters for Claude-driven products

| Use case | Value |
|----------|-------|
| **Lead-gen / marketing** | Post-process AI-generated copy before publishing. Catches the tell-tale "AI wrote this" patterns that erode trust. |
| **Agent factories** | Add as a post-processing step in any agent pipeline that generates customer-facing text. |
| **Ad creatives** | Clean AI-drafted ad copy — removes hollow superlatives that ad platforms may penalize or audiences ignore. |
| **Content QA** | Use the JSON output to score drafts for "slop density" and flag pieces that need human editing. |
| **Claude Code skill** | Integrates directly into the developer workflow — say "unslop this" and get cleaner text without leaving the editor. |

The skill version is particularly valuable: it teaches Claude the specific patterns to watch for, making it a better editor even without running the Python code.
