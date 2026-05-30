# Claude Code Session Picker

**Fuzzy-find and resume any past Claude Code session from its original working directory.**

Claude Code stores session history as `.jsonl` files under `~/.claude/projects/`. This tool scans them, presents an interactive fzf picker (or a table), and resumes the selected session with `claude --resume <id>` — automatically `cd`-ing into the right project folder.

```
  #  Date              Msgs  Project                         Summary
───  ────────────────  ─────  ──────────────────────────────  ────────────────────────────
  1  2026-05-29 14:30     47  /home/user/projects/web-app    Add dark mode toggle to settings page
  2  2026-05-29 10:15     23  /home/user/projects/api-server Fix rate limiting middleware returning 500
  3  2026-05-28 18:45    112  /home/user/projects/ml-pipeline Refactor data preprocessing to use Polars
```

## Quick start

```bash
bash run.sh          # demo with mock data, no dependencies needed
python3 ccsession.py --demo --list   # table view
python3 ccsession.py                 # real sessions + fzf picker
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Installation, usage, trigger phrases
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations

## Origin

Python port of [sorafujitani/ccsession](https://github.com/sorafujitani/ccsession) (Go).
