# How to Use

## What this is

A **Claude Code skill** that teaches Claude a structured vulnerability research methodology. When installed, saying "find security vulnerabilities in this codebase" triggers a multi-pass audit following Mozilla's Steer/Scale/Stack approach.

## Install the skill

```bash
# Create the skill directory and copy the skill file
mkdir -p ~/.claude/skills/llm_vuln_harness
cp SKILL.md ~/.claude/skills/llm_vuln_harness/SKILL.md
```

That's it. Claude Code will now pick up the skill automatically.

### Trigger phrases

Any of these will activate the skill:

- "Find security vulnerabilities in this codebase"
- "Run an automated security audit on this project"
- "Set up a vulnerability research pipeline for this repo"
- "Check this C/C++ code for memory safety bugs"
- "Do a deep security review like Mozilla did with Firefox"

## Run the demo (no API key needed)

```bash
git clone <this-repo>
cd llm_vuln_harness
bash run.sh
```

The demo scans `sample_targets/` (intentionally vulnerable C code) and produces a full security report in your terminal.

### JSON output

```bash
python3 vuln_harness.py sample_targets json
```

### Point at your own code

```bash
python3 vuln_harness.py /path/to/your/c/project
```

Note: The demo scanner uses pattern-matching heuristics. For real vulnerability research, use the installed Claude Code skill — Claude traces actual data flows and reasons about exploitability.

## First 60 seconds

**Input:** `bash run.sh`

**Output** (abbreviated):

```
======================================================================
  LLM VULNERABILITY RESEARCH HARNESS - SCAN REPORT
======================================================================
  Methodology: Steer / Scale / Stack  (Mozilla Firefox approach)

========================================================================
  [!!] Critical  Heap Buffer Overflow
========================================================================
  Location:  sample_targets/parser.c:30  in  parse_tag()
  Pass:      2  |  Validated: Yes

  Description
    Unbounded copy into fixed-size buffer tag_name[MAX_TAG_LEN].
    Loop copies from input until '>' without checking j < MAX_TAG_LEN.

  Root Cause
    Missing bounds check on destination index j against MAX_TAG_LEN (64).

  Trigger Scenario
    Send a tag with name longer than 64 bytes: '<' + 'A'*200 + '>'

  Suggested Fix
    Add `&& j < MAX_TAG_LEN - 1` to the while condition.

... (7 more findings across 7 vuln classes) ...

========================================================================
  SCAN SUMMARY
========================================================================
  Total validated findings: 8
    [!!] Critical: 3
    [!]  High:     3
    [~]  Medium:   2
```

## Dependencies

Python 3.10+ (stdlib only, no pip install needed).
