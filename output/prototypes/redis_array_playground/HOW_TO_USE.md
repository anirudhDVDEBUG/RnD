# How to Use

## Install

No dependencies required — just Python 3 (for the local HTTP server) and a browser.

```bash
git clone <this-repo>
cd redis_array_playground
bash run.sh
# Opens on http://localhost:8765
```

Or serve with any static file server:

```bash
npx serve .           # Node
python3 -m http.server 8765  # Python
```

## First 60 Seconds

1. Run `bash run.sh` — a browser playground opens at `http://localhost:8765`
2. Click **"Load Sample Data"** — this creates three arrays: `fruits` (20 items), `scores` (10 numbers), `cities` (10 city names)
3. Click **ARGREP** in the sidebar
4. Set: key = `fruits`, predicate = `CONTAINS`, pattern = `berry`
5. Check **WITHVALUES** and **NOCASE**
6. Click **Run Command**
7. Output:

```
> ARGREP fruits CONTAINS berry WITHVALUES NOCASE
4) "elderberry"
15) "raspberry"
16) "strawberry"
```

8. Try **ARSCAN** with key = `fruits`, pattern = `*an*` to find banana, mango, tangerine, etc.
9. Try **AROP** with key = `scores`, index = `0`, op = `INCR` to bump the first score.

## As a Claude Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/redis_array_playground
cp SKILL.md ~/.claude/skills/redis_array_playground/SKILL.md
```

**Trigger phrases:**
- "Build a Redis Array command explorer in the browser"
- "Create a WASM playground for testing Redis ARGREP commands"
- "I want to try Redis array commands without a server"
- "Make an interactive UI for Redis array operations"

## Keyboard Shortcuts

- **Ctrl+Enter** — Run the current command
