# Technical Details

## What It Does

This skill runs a shell pipeline that walks the git log for a specific file, extracts the first line of that file at each commit where it was added or modified, and deduplicates consecutive identical values. The result is a chronological timeline showing every change to the file's first line — effectively a "rename history" for projects that encode their name in README headers.

The approach uses `git log --follow` to track the file even through renames, `git show <hash>:<path>` to retrieve historical content without checking out, and `tac` to reverse the output into chronological order.

## Architecture

```
git log --follow --diff-filter=AM -- <file>
    |
    v
For each commit hash + date:
    git show <hash>:<file> | head -n 1
    |
    v
Deduplicate consecutive identical lines
    |
    v
tac (reverse to chronological order)
    |
    v
Output: date  short_hash  first_line
```

### Key Files

| File | Purpose |
|------|---------|
| `first_line_history.sh` | Main script — POSIX shell, no dependencies |
| `SKILL.md` | Claude Code skill definition with trigger phrases |
| `run.sh` | Demo that creates a temp repo and runs the tool |

### Dependencies

- `git` — the only real dependency
- POSIX utilities: `head`, `cut`, `tac`, `echo`
- No Python, no Node, no external packages

## Limitations

- **Performance on huge repos**: Runs `git show` once per matching commit. On repos with thousands of commits touching the target file, this can be slow (linear in commit count).
- **Binary files**: Only meaningful for text files.
- **Merge commits**: Includes merge commits if they modified the file; this can occasionally produce duplicate entries (handled by dedup).
- **`tac` availability**: `tac` is GNU coreutils; on macOS use `tail -r` or install coreutils. The demo script handles this.
- **Line 1 only by default**: Tracking other lines requires a manual edit (`sed -n 'Np'`).

## Why It Matters for Claude-Driven Products

- **Agent Factories**: Agents that audit or onboard repos can use this to understand project identity evolution — critical for generating accurate documentation or changelogs.
- **Lead-Gen / Marketing**: Track competitor product renames and pivots by monitoring their public repos' README headers over time.
- **Ad Creatives**: Automatically detect when a product name changes to update ad copy and landing pages.
- **Voice AI**: When building voice agents that reference products, knowing the current (and historical) name prevents outdated references in conversations.

## References

- Source: [Simon Willison — Warelay -> OpenClaw](https://simonwillison.net/2026/May/16/openclaw-names/#atom-everything)
- Tool: [first_line_history.py](https://github.com/simonw/tools/blob/main/python/first_line_history.py)
