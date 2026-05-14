# How to Use

## Install & Run

**Prerequisites:** Node.js 18+ (no npm packages needed -- uses built-in `http` module only).

```bash
git clone <this-repo> && cd csp_allowlist_sandbox
bash run.sh
# => Server starts at http://localhost:8090
```

Or manually:

```bash
node server.js          # serves on port 8090
PORT=3000 node server.js  # use a custom port
```

Open `http://localhost:8090` in any modern browser.

## As a Claude Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/csp_allowlist_sandbox
cp SKILL.md ~/.claude/skills/csp_allowlist_sandbox/SKILL.md
```

**Trigger phrases** that activate this skill:

- "csp sandbox"
- "iframe allow-list"
- "fetch intercept csp"
- "sandboxed iframe security"
- "content security policy allow-list"

## First 60 Seconds

1. **Run `bash run.sh`** -- the server starts and prints a URL.
2. **Open `http://localhost:8090`** in your browser. You'll see a two-panel layout: an editor on the left with sample HTML, and a sandboxed preview on the right.
3. **The sample code** immediately tries to `fetch()` two APIs:
   - `httpbin.org` -- not in the allow-list, so it gets **blocked**.
   - `jsonplaceholder.typicode.com` -- also blocked.
4. **A browser `confirm()` dialog pops up** asking: _"The sandbox tried to connect to https://httpbin.org. Add this origin to the CSP connect-src allow-list and refresh?"_
5. **Click OK.** The origin appears as a green tag in the allow-list bar, the CSP updates, and the preview reloads. The httpbin request now succeeds.
6. **The second `confirm()` pops up** for `jsonplaceholder.typicode.com`. Accept it too.
7. Both requests now succeed. The preview shows the fetched data.

You can also:
- **Manually add origins** via the text input + Add button in the toolbar.
- **Remove origins** by clicking the x on any tag.
- **Clear the entire allow-list** with the "Clear Allow-list" button.
- **Edit the HTML** in the editor and click "Refresh Preview" to re-run with the current CSP.

The allow-list persists in `localStorage`, so it survives page reloads.
