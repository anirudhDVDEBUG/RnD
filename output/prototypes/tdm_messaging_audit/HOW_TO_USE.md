# How to Use — TDM Messaging Audit

## Option A: Install as a Claude Code Skill (recommended)

### 1. Copy the skill file

```bash
mkdir -p ~/.claude/skills/tdm_messaging_audit
cp SKILL.md ~/.claude/skills/tdm_messaging_audit/SKILL.md
```

### 2. Trigger the skill

Open Claude Code in any project and use one of these phrases:

- `Audit my homepage copy for enterprise buyers`
- `Rewrite this messaging to appeal to technical decision makers`
- `Make our positioning more analyst-friendly`
- `How would a TDM perceive our landing page?`
- `Align our product narrative with Gartner trends`

Claude will follow the SKILL.md instructions to score and rewrite your copy.

### 3. Provide input

Either:
- Paste your landing page text directly into the chat
- Give Claude a URL and ask it to fetch and audit the content
- Point to a file in your repo: `Audit the copy in src/pages/landing.tsx`

---

## Option B: Run the standalone Python demo

### Install

```bash
git clone <this-repo>
cd tdm_messaging_audit
# No dependencies needed — pure Python 3.10+ stdlib
```

### Run

```bash
bash run.sh
```

### Audit your own copy

```bash
python3 tdm_audit.py path/to/your_landing_page.txt "YourProduct"
```

The text file should contain your raw landing page copy (HTML tags stripped).

---

## First 60 Seconds

**Input** — A developer-centric landing page:

```
AcmeDB — Blazingly fast vector database
Built by developers, for developers. AcmeDB lets you grok your data
at scale. Stop yak shaving with legacy databases...
Featured on Hacker News. Join our Discord.
```

**Output** — Scored audit with rewrites:

```
  Overall TDM Resonance Score: 1.4 / 5.0

  ┌─────────────────────────┬───────┬───────────┐
  │ Dimension               │ Score │ Visual    │
  ├─────────────────────────┼───────┼───────────┤
  │ Analyst Alignment       │   1   │ █░░░░     │
  │ Career-Safety Signaling │   1   │ █░░░░     │
  │ Trend Anchoring         │   2   │ ██░░░     │
  │ Jargon Calibration      │   1   │ █░░░░     │
  │ Defensibility Framing   │   2   │ ██░░░     │
  └─────────────────────────┴───────┴───────────┘

  ✗ Jargon Calibration (1/5)
    → Developer jargon detected: blazingly fast, grok, yak shaving, ...
    REWRITE: Remove developer-culture jargon. Replace 'blazingly fast'
    with 'high performance'...
```

The skill then provides concrete before/after rewrites for every dimension scoring below 3.
