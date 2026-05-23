# How to Use

## Option A: Install as a Claude Code Skill

### 1. Copy the skill folder

```bash
mkdir -p ~/.claude/skills/ftc_active_listening_settlement
cp SKILL.md ~/.claude/skills/ftc_active_listening_settlement/SKILL.md
```

### 2. Trigger phrases

Once installed, Claude Code will activate this skill when you ask things like:

- "What happened with the FTC active listening case?"
- "Explain the Cox Media Group ad targeting settlement"
- "How did the Active Listening marketing deception work?"
- "What are the FTC penalties for deceptive AI marketing claims?"
- "Can smart devices actually listen to target ads?"

### 3. What you get

Claude will respond with structured analysis covering:
- What the companies claimed vs. what the technology actually did
- Settlement amounts and regulatory outcomes
- Actionable compliance lessons for AI product marketing

---

## Option B: Run the standalone analyzer

### Install

```bash
pip install -r requirements.txt
```

(Only standard library is used -- no external packages needed.)

### Run

```bash
bash run.sh
```

Or directly:

```bash
python3 analyzer.py
```

### CLI flags

```bash
python3 analyzer.py --section deception    # Just the deception breakdown
python3 analyzer.py --section penalties     # Just the penalty details
python3 analyzer.py --section lessons       # Just the compliance lessons
python3 analyzer.py --format json           # Output as JSON instead of text
```

---

## First 60 Seconds

```
$ bash run.sh

=== FTC "Active Listening" Settlement Analysis ===

CASE: FTC v. Cox Media Group, MindSift, 1010 Digital Works (May 2026)

--- What They Claimed ---
- Smart devices capture real-time voice data from consumer conversations
- Voice data is paired with behavioral data to target in-market consumers
- Advertisers get access to "Active Listening" intent signals

--- What Actually Happened ---
- NO microphone data was collected or used
- Service relied on standard ad-targeting: cookies, behavioral data, demographics
- "Active Listening" was a misleading marketing label, not a technology
- Ads were also not accurately placed in customers' desired locations

--- Penalties ---
  Cox Media Group (CMG):  $499,227
  MindSift:               $349,459
  1010 Digital Works:     $149,768
  TOTAL:                  $998,454

--- Compliance Lessons ---
1. Technical claims in sales materials must match actual system capabilities
2. Aspirational language implying unbuilt functionality = deceptive trade practice
3. FTC actively enforces against misleading AI capability claims (Section 5)
4. "Phones are listening" fear is widespread but targeting comes from behavioral data
5. Audit pitch decks and marketing collateral for regulatory compliance

--- Timeline ---
  2024        CMG pitch deck surfaces claiming "active listening" via smart devices
  Sep 2024    Researchers analyze claims; hypothesize standard ad targeting rebranded
  May 2026    FTC settles; confirms service never used voice data

Report complete.
```
