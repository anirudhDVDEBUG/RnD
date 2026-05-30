# How to Use — Claude Code Session Picker

## Install

### Option A: Python port (this repo)

No install — just run:

```bash
python3 ccsession.py
```

Requires Python 3.10+ (stdlib only, zero dependencies).

For the interactive picker, also install **fzf**:

```bash
# macOS
brew install fzf

# Debian / Ubuntu
sudo apt install fzf
```

### Option B: Original Go binary

```bash
go install github.com/sorafujitani/ccsession@latest
```

Or build from source:

```bash
git clone https://github.com/sorafujitani/ccsession.git
cd ccsession && go build -o ccsession .
```

Requires Go 1.21+ and fzf.

---

## This is a CLI tool (not a Skill or MCP server)

There is no SKILL.md to drop or `mcpServers` JSON to configure.
You invoke it directly from your terminal.

---

## CLI usage

```bash
# Interactive fzf picker (requires fzf)
python3 ccsession.py

# Table listing only
python3 ccsession.py --list

# JSON output (for scripting)
python3 ccsession.py --json

# Auto-pick session #2, dry-run (don't actually resume)
python3 ccsession.py --pick 2 --dry-run

# Demo mode with mock data (no real sessions needed)
python3 ccsession.py --demo --list
```

---

## First 60 seconds

### 1. Run the demo

```bash
bash run.sh
```

Output:

```
==============================================
  Claude Code Session Picker — Demo
==============================================

>>> Listing mock sessions (--demo --list):

  #  Date              Msgs  Project                         Summary
───  ────────────────  ─────  ──────────────────────────────  ──────────────────────────────────────
  1  2026-05-29 14:30     47  /home/user/projects/web-app    Add dark mode toggle to settings page
  2  2026-05-29 10:15     23  /home/user/projects/api-server Fix rate limiting middleware returning 500
  3  2026-05-28 18:45    112  /home/user/projects/ml-pipeline Refactor data preprocessing to use Polars
  ...

>>> Auto-picking session #3 (--demo --pick 3 --dry-run):

  Session:   i9j0k1l2-session-003
  Project:   /home/user/projects/ml-pipeline
  Summary:   Refactor data preprocessing to use Polars instead of Pandas
  Messages:  112
  Started:   2026-05-28 18:45

  [dry-run] Would run: claude --resume i9j0k1l2-session-003
  [dry-run] From directory: /home/user/projects/ml-pipeline
```

### 2. Try it with your real sessions

```bash
python3 ccsession.py --list
```

If you have Claude Code sessions in `~/.claude/projects/`, they'll appear here.

### 3. Pick and resume

```bash
python3 ccsession.py
```

fzf opens → type to filter → Enter to resume from the original directory.

---

## How sessions are stored

Claude Code writes session logs as `.jsonl` files inside:

```
~/.claude/projects/<encoded-project-path>/<session-id>.jsonl
```

Each line is a JSON message. The tool parses the first message's timestamp and content to build the summary shown in the picker.

---

## Shell alias (recommended)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias ccs='python3 /path/to/ccsession.py'
```

Then just type `ccs` to pick a session.
