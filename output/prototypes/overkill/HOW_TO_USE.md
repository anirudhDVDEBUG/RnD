# How to Use: Overkill Skill

## What it is

Overkill is a **Claude Code skill** (a SKILL.md file). It is NOT an MCP server
and does NOT require any package installation. It gives Claude a persona that
over-engineers every coding request to an absurd degree.

## Install the skill

```bash
# Clone the source repo
git clone https://github.com/santiago-vargas-de-kruijf/claude-overkill.git

# Copy the skill folder into your Claude Code skills directory
mkdir -p ~/.claude/skills/overkill
cp claude-overkill/SKILL.md ~/.claude/skills/overkill/SKILL.md
```

That's it. No `pip install`, no `npm install`, no API keys.

## Trigger phrases

Once installed, use any of these phrases in Claude Code to activate the skill:

- "Over-engineer this for me"
- "Go overkill on this implementation"
- "Make this enterprise-grade"
- "Give me the most robust version possible"
- "Apply every design pattern you know to this"

## First 60 seconds

1. Install the skill (above).
2. Open Claude Code in any project.
3. Type:

```
Over-engineer a function that adds two numbers
```

4. Claude produces ~400 lines featuring:
   - Strategy Pattern with 3 pluggable addition algorithms
   - Factory Pattern for dynamic algorithm selection
   - Circuit Breaker for fault tolerance
   - Result Monad for railway-oriented error handling
   - Custom exception hierarchy
   - Structured logging with correlation IDs
   - Metrics collection
   - Feature flags
   - 4-stage input validation pipeline

The code compiles, runs, and actually adds the numbers correctly.

## Running the demo locally

```bash
cd output/prototypes/overkill
bash run.sh
```

Requires Python 3.10+. No external dependencies.

**Sample output:**

```
  DEMO 1: Add 2 + 3 (integer path -> bitwise strategy)
  [        INFO] [AdditionService] Executing addition: 2.0 + 3.0
  Result: 5.0
  Strategy: BitwiseHalfAdderSimulation
  Time: 0.0012 ms
```
