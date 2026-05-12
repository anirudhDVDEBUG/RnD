# How to Use — GCC Market Intelligence

## This is a Claude Code Skill

No pip install or npm install required. The skill is a single `SKILL.md` file that teaches Claude how to answer GCC market-entry questions.

## Install the skill

```bash
# 1. Create the skill directory
mkdir -p ~/.claude/skills/gcc-market-intelligence

# 2. Copy the skill file
cp SKILL.md ~/.claude/skills/gcc-market-intelligence/SKILL.md
```

That's it. Next time you start Claude Code, the skill is active.

## Trigger phrases

The skill activates automatically when you ask Claude about:

- **Country entry:** "How do I enter the Saudi market as a B2B SaaS company?"
- **Sovereign wealth funds:** "What sovereign wealth funds should I target in the GCC?"
- **Procurement:** "Walk me through GCC procurement and B2G sales processes"
- **Compliance:** "What localization and compliance requirements exist for UAE and Saudi?"
- **Soft-landing:** "Help me build a soft-landing strategy for the Gulf region"
- **Specific funds:** Mentioning PIF, ADIA, QIA, Mubadala, or KIA
- **Vision programs:** "Tell me about Saudi Vision 2030 opportunities"
- **MENA/Gulf:** Any question about B2B or B2G in the Gulf/MENA region

**Does NOT trigger for:** general international expansion, B2C products, or regions outside the GCC.

## First 60 seconds

After installing, open Claude Code and type:

```
I'm building a cybersecurity SaaS product. How should I enter the Saudi market?
```

Claude will respond with structured intelligence covering:

1. **Market overview** — KSA as largest GCC economy, Vision 2030 digital transformation spend
2. **Key stakeholders** — PIF ($930B+), SDAIA, NCA, relevant family offices
3. **Procurement** — Etimad portal, IKTVA requirements, Saudization quotas
4. **Compliance** — PDPL data residency, local entity requirements (SAGIA LLC)
5. **Soft-landing playbook** — 6 steps from demand validation to product localization
6. **Incentives** — SVC co-investment, Monsha'at grants, MCIT Cloud First

Try follow-ups:

```
Compare UAE vs Saudi for my product
What family offices invest in cybersecurity?
What events should I attend in Q1?
```

## Standalone CLI demo

The repo also includes a Python CLI that demonstrates the same intelligence without Claude:

```bash
# Single-country briefing
python3 gcc_intel.py --country saudi --vertical cybersecurity

# Compare countries
python3 gcc_intel.py --compare saudi uae qatar --vertical fintech

# All six countries
python3 gcc_intel.py --all

# JSON output (for piping into other tools)
python3 gcc_intel.py --country uae --vertical fintech --json
```

No dependencies beyond Python 3.10+ stdlib.
