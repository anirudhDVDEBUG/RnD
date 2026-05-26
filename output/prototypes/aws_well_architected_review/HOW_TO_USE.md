# How to Use

## Option A: Install as a Claude Code Skill

### 1. Create the skill directory

```bash
mkdir -p ~/.claude/skills/aws-well-architected-review
cp SKILL.md ~/.claude/skills/aws-well-architected-review/SKILL.md
```

### 2. Trigger phrases

Once installed, Claude Code activates this skill when you say things like:

- "Review this architecture for AWS best practices"
- "Is this infrastructure Well-Architected?"
- "Check this AWS deployment for security and reliability issues"
- "Optimize this cloud architecture for cost and performance"
- "Help me apply the Well-Architected Framework to this design"

Claude will then walk through each of the six pillars (Security, Reliability, Operational Excellence, Performance Efficiency, Cost Optimization, Sustainability) and produce prioritized findings with fix recommendations.

### 3. What Claude does with the skill

When triggered, Claude will:
1. Identify all IaC files (`.tf`, `.json`, `.yaml`) and application code in scope
2. Evaluate each file against the six Well-Architected pillars
3. Produce findings with risk levels (HIGH/MEDIUM/LOW)
4. Recommend specific code changes for high-priority items

---

## Option B: Run the standalone CLI analyzer

The included `wa_reviewer.py` performs offline static analysis — no AWS credentials or API keys needed.

### Install

```bash
git clone <this-repo>
cd aws_well_architected_review
# No pip install needed — Python 3.10+ stdlib only
```

### Run

```bash
python3 wa_reviewer.py samples/          # scan the included sample files
python3 wa_reviewer.py /path/to/your/tf/ # scan your own IaC directory
python3 wa_reviewer.py main.tf           # scan a single file
```

Or use the wrapper:

```bash
bash run.sh
```

---

## First 60 Seconds

**Input:** A directory with Terraform files, IAM policy JSON, and Python source containing common anti-patterns (public S3 buckets, wildcard IAM, hard-coded secrets, single-AZ RDS, open security groups).

**Output:**

```
========================================================================
  AWS WELL-ARCHITECTED REVIEW REPORT
========================================================================

  Total findings: 21
    HIGH:   13
    MEDIUM: 6
    LOW:    2

  Findings by pillar:
    [SEC] Security                  11  ###########
    [REL] Reliability                5  #####
    [CST] Cost Optimization          3  ###
    [OPS] Operational Excellence     2  ##

------------------------------------------------------------------------

  [HIGH  ] #1  IAM policy grants full admin access (Action: *, Resource: *)
  Pillar : Security
  File   : samples/bad_iam.json
  Detail : This policy is equivalent to AdministratorAccess ...
  Fix    : Scope actions and resources to only what the role/user needs ...
  --------------------------------------------------------------------

  [HIGH  ] #2  Hard-coded AWS access key in source code
  Pillar : Security
  File   : samples/bad_app.py:5
  ...

========================================================================
  VERDICT: 13 HIGH-risk findings require immediate attention.
========================================================================
```

Each finding includes the pillar, risk level, file location, description, and a concrete remediation step.
