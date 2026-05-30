# How to Use — CVE Triage Skill

## This is a Claude Code Skill

It's a markdown instruction file that teaches Claude Code how to triage CVEs. No server, no daemon — just a skill file dropped into the right directory.

## Installation (30 seconds)

### Option A: From the original repo

```bash
git clone https://github.com/moltenbit/should-i-care.git
mkdir -p ~/.claude/skills/should-i-care
cp should-i-care/SKILL.md ~/.claude/skills/should-i-care/SKILL.md
```

### Option B: From this prototype

```bash
mkdir -p ~/.claude/skills/should-i-care
cp SKILL.md ~/.claude/skills/should-i-care/SKILL.md
```

That's it. No `pip install`, no `npm install`, no config files.

## Where to put it

```
~/.claude/
  skills/
    should-i-care/
      SKILL.md          <-- the skill definition
```

Claude Code automatically loads skills from `~/.claude/skills/*/SKILL.md`.

## Trigger phrases

Say any of these in Claude Code and the skill activates:

- "Should I care about CVE-2024-3094?"
- "Triage this CVE for my environment"
- "Is this vulnerability relevant to my stack?"
- "Assess whether CVE-2024-XXXXX affects us"
- "Check if this CVE applies to our systems"

## First 60 seconds

1. Install the skill (Option A or B above)
2. Open Claude Code in a project directory
3. Type: **"Should I care about CVE-2024-3094?"**

Claude will:
1. Look up CVE details from NVD/MITRE APIs (requires internet)
2. Scan your project's `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `Gemfile`, or `*.csproj`
3. Compare your installed versions against the affected range
4. Output a structured triage report with verdict, reasoning, and recommended actions

### Example output

```
## CVE Triage: CVE-2024-3094

**Verdict**: [OK] NOT AFFECTED

**CVE Summary**: Malicious code in xz-utils tarballs starting with v5.6.0...
**CVSS Score**: 10.0 (CRITICAL)
**Affected Product**: xz-utils (>=5.6.0, <=5.6.1)

### Applicability to This Environment
- **Software present?**: Yes (xz-utils v5.4.5 in system packages)
- **Version in affected range?**: No (5.4.5 < 5.6.0)
- **Vulnerable code path reachable?**: N/A — version not affected

### Reasoning
The software is present but the installed version (5.4.5) is below
the affected range (5.6.0–5.6.1). No action required.

### Recommended Actions
- No immediate action needed
- Monitor for changes to the advisory scope

### Sources
- https://nvd.nist.gov/vuln/detail/CVE-2024-3094
- https://www.openwall.com/lists/oss-security/2024/03/29/4
```

## Running the standalone demo

The prototype includes a Python implementation that demonstrates the triage logic with mock data:

```bash
# Run all demo scenarios
bash run.sh

# Triage a specific CVE
python3 cve_triage.py CVE-2024-3094

# Point at a real project
python3 cve_triage.py CVE-2024-3094 --project-dir /path/to/your/project

# Point at a specific dependency file
python3 cve_triage.py CVE-2024-3094 --dep-file /path/to/package.json
```

## What it does NOT do

- Does not auto-patch or upgrade dependencies
- Does not scan container images or OS-level packages (skill instructs Claude to check `dpkg -l` etc., but that depends on permissions)
- Does not replace a full vulnerability scanner (Snyk, Trivy, Grype)
- Mock data only covers 5 CVEs; real usage requires internet access to NVD/MITRE APIs
