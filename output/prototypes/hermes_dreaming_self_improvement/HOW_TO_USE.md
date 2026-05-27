# How to Use Hermes Dreaming

## Install

```bash
git clone https://github.com/asimons81/hermes-dreaming.git
cd hermes-dreaming
pip install -e .
```

Or use the prototype directly (no install needed):

```bash
cd hermes_dreaming_self_improvement
python -m hermes_dreaming --help
```

No external dependencies -- stdlib-only Python 3.10+.

## As a Claude Code Skill

Drop the skill file into your skills directory:

```bash
mkdir -p ~/.claude/skills/hermes_dreaming_self_improvement
cp SKILL.md ~/.claude/skills/hermes_dreaming_self_improvement/SKILL.md
```

**Trigger phrases** that activate it:

- "Run a dreaming cycle to improve agent memory and skills"
- "Stage self-improvement updates for review before applying"
- "Update my agent's facts and knowledge with review gates"
- "Run Hermes-style memory consolidation and skill refinement"
- "Propose skill and fact updates, then let me approve or discard"

## As an MCP Server

Paste this into your `~/.claude.json` under the `mcpServers` block:

```json
{
  "mcpServers": {
    "hermes-dreaming": {
      "command": "python",
      "args": ["-m", "hermes_dreaming", "serve"],
      "env": {}
    }
  }
}
```

## CLI Usage

```bash
python -m hermes_dreaming dream       # Propose updates from interaction log
python -m hermes_dreaming review      # Inspect staged proposals
python -m hermes_dreaming approve ID  # Approve a specific proposal
python -m hermes_dreaming approve --all  # Approve everything
python -m hermes_dreaming discard ID  # Reject a proposal
python -m hermes_dreaming apply       # Write approved changes to knowledge base
python -m hermes_dreaming status      # Show current state
```

## First 60 Seconds

```
$ bash run.sh

--- STEP 1: Dream (analyze mock interactions, propose updates) ---

=== Hermes Dreaming: Running self-improvement cycle ===

Generated 8 proposal(s):

  [+] a3f1  memory_update   Remember user interest: Python           (conf: 80%)
  [+] b7c2  memory_update   Remember user interest: Testing          (conf: 70%)
  [+] c4d3  memory_update   Remember user interest: Docker           (conf: 70%)
  [+] e5f6  memory_update   Remember user interest: CI/CD            (conf: 70%)
  [+] f1a2  skill_update    Add skill: pytest                        (conf: 85%)
  [+] g3b4  skill_update    Add skill: git                           (conf: 85%)
  [+] h5c6  skill_update    Add skill: docker-compose                (conf: 70%)
  [!] i7d8  fact_update     Correct fact: default_app_port           (conf: 85%)

--- STEP 2: Review (inspect staged proposals) ---

  [+] a3f1  memory_update   Remember user interest: Python           (conf: 80%)
    Reason: Observed 3 mentions across interactions
    After:  user_interest_python = frequently discussed topic (3 mentions)

  [!] i7d8  fact_update     Correct fact: default_app_port           (conf: 85%)
    Reason: Explicit user correction observed
    Before: Default app port: 3000
    After:  Default port is 8080, not 3000

--- STEP 3: Approve all proposals ---
Approved 8 proposal(s).

--- STEP 4: Apply ---
Applied 8 proposal(s) to agent knowledge base.

--- STEP 5: Final status ---
=== Proposal Status ===
  applied: 8

=== Knowledge Base ===
  Memory entries: 4
  Skills:         4
  Facts:          1
```

All data is persisted to `.hermes_data/` as JSON files you can inspect directly.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `HERMES_DATA_DIR` | `.hermes_data` | Directory for proposal/knowledge JSON files |
