# Technical Details — Claude Code Session Picker

## What it does

The session picker scans `~/.claude/projects/` for `.jsonl` session files that Claude Code creates during conversations. It parses each file to extract metadata (timestamp, message count, first user prompt as a summary, and the project working directory), then presents an interactive fuzzy-search picker via fzf. When the user selects a session, the tool `cd`s into the original project directory and runs `claude --resume <session-id>`, seamlessly continuing the conversation.

The Python port in this repo faithfully replicates the original Go tool's behavior while adding `--demo`, `--json`, `--dry-run`, and `--pick` flags for scripting and evaluation.

## Architecture

### Key files

| File | Role |
|------|------|
| `ccsession.py` | Single-file CLI — session discovery, parsing, fzf integration, resume logic |
| `run.sh` | End-to-end demo with mock data |

### Data flow

```
~/.claude/projects/
  └─ <encoded-path>/
       └─ <session-id>.jsonl
              │
              ▼
     find_sessions()          ← Walk dirs, parse .jsonl first/last lines
              │
              ▼
     List[session_dict]       ← {id, project, timestamp, messages, summary}
              │
       ┌──────┴──────┐
       ▼              ▼
   print_table()   pick_with_fzf()
                       │
                       ▼
                  resume_session()
                       │
                       ▼
              os.chdir(project_cwd)
              os.execvp("claude", ["claude", "--resume", id])
```

### Dependencies

**Python port (this repo):** Python 3.10+ stdlib only. fzf is optional (falls back to numbered input).

**Original Go tool:** Go 1.21+, fzf (required).

### How project paths are decoded

Claude Code encodes project paths as directory names by replacing `/` with `-`. For example, `/home/user/my-project` becomes `-home-user-my-project`. The tool reverses this to reconstruct the original working directory.

### No model calls

This tool makes zero LLM API calls. It's a local filesystem utility that reads existing session files and shells out to `claude --resume`.

## Limitations

- **Path decoding is heuristic.** The `-` to `/` conversion can be ambiguous for paths that contain literal hyphens. The original Go tool has the same limitation.
- **Summary extraction is best-effort.** It reads the first user message in the JSONL; if the format changes across Claude Code versions, summaries may degrade.
- **No session search by content.** Only metadata (timestamp, project, first message) is indexed — full-text search across all messages is not supported.
- **fzf is required for the interactive picker.** Without it, you get a numbered list fallback (Python port) or an error (Go original).
- **macOS / Linux only.** Windows paths would need different decoding logic.
- **Read-only.** Cannot delete, rename, or tag sessions — it's purely a viewer/launcher.

## Why it matters

For anyone building Claude-driven products — agent factories, marketing automation pipelines, voice AI workflows — session management becomes a real problem at scale. Developers frequently context-switch between projects and lose track of which Claude Code session had the right conversation context.

This tool solves the "which session was I in?" problem:

- **Agent factory developers** can quickly resume sessions where they were tuning agent behavior across multiple projects.
- **Lead-gen / marketing engineers** working on Claude-powered content pipelines can pick up exactly where they left off on any campaign.
- **Multi-project teams** avoid the overhead of manually searching session IDs or restarting conversations from scratch.

It's a small DX utility, but for heavy Claude Code users managing 10+ projects, the time savings compound.
