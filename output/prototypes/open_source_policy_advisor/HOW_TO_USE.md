# How to Use

## Option A: Install as a Claude Code Skill

This is a **Claude Code skill** — a markdown file that gives Claude domain expertise when triggered by relevant prompts.

### Installation

```bash
# Create the skill directory and copy the file
mkdir -p ~/.claude/skills/open_source_policy_advisor
cp SKILL.md ~/.claude/skills/open_source_policy_advisor/SKILL.md
```

### Trigger phrases

Once installed, Claude Code will activate this skill when you ask things like:

- "Should we make our government code private after a security incident?"
- "How do we handle vulnerability disclosures in open source public sector projects?"
- "We found vulnerabilities in our public repos — should we close them down?"
- "Help me draft an open source policy that addresses AI-discovered vulnerabilities"
- "What's the best practice for open source policy in government organizations?"

### Example interaction

```
You: We just got a Project Glasswing report showing 4 vulnerabilities in our
     public NHS repos. The board wants to close everything. What should we do?

Claude: [Activates open_source_policy_advisor skill]
        Based on GDS guidance published May 2026, the recommended approach is
        "fix and stay open." Here's why...
```

## Option B: Run the CLI Demo

The Python script demonstrates the advisory logic with three mock public-sector scenarios. No API keys or external services required.

### Prerequisites

- Python 3.8+

### Install & run

```bash
pip install -r requirements.txt   # no external deps, but file exists for convention
bash run.sh
```

### First 60 seconds

```bash
# Run all 3 scenarios (NHS Digital, HMRC, Local Council):
python3 advisor.py

# Run a single scenario (1-3):
python3 advisor.py 2

# Get JSON output for programmatic use:
python3 advisor.py --json
```

**Input:** A scenario describing an organisation, its repos, vulnerabilities found, whether AI scanning was involved, and whether there is political pressure to close repos.

**Output:** A structured report containing:
- Risk score (0-10)
- Recommended action (stay open / temporary closure / permanent closure)
- Rationale citing GDS principles
- Numbered immediate steps
- Draft policy clauses ready for adoption

### Sample output (truncated)

```
========================================================================
  OPEN SOURCE POLICY ADVISORY REPORT
  Organisation: NHS Digital
  Repositories: 157 public repos
========================================================================

  Vulnerabilities Assessed: 4
    [CRITICAL] SQL injection in patient lookup API
               PATCHED
    [HIGH    ] XSS in appointment booking form
               PATCHED
    ...

  Risk Score: 4.0/10

  Recommendation: STAY OPEN (recommended)
  ----------------------------------------
    No actively exploited vulnerabilities found. The GDS principle
    applies: remain open by default, fix vulnerabilities in place,
    and invest in security practices rather than obscurity.
```
