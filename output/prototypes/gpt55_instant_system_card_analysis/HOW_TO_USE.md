# How to Use

## Install

No external dependencies. Requires Python 3.10+.

```bash
git clone <this-repo>
cd gpt55_instant_system_card_analysis
bash run.sh
```

## As a Claude Skill

This is a Claude Code skill. To install:

1. Copy the `SKILL.md` file into your skills directory:

```bash
mkdir -p ~/.claude/skills/gpt55_instant_system_card_analysis
cp SKILL.md ~/.claude/skills/gpt55_instant_system_card_analysis/SKILL.md
```

2. Trigger phrases that activate the skill:

- "What safety evaluations were done for GPT-5.5 Instant?"
- "Summarize the GPT-5.5 Instant system card"
- "How does GPT-5.5 Instant compare to previous models on safety benchmarks?"
- "What are the deployment mitigations for GPT-5.5 Instant?"
- "What risks were identified in the GPT-5.5 Instant evaluation?"
- Any question about GPT-5.5 Instant safety or OpenAI model risk assessments

## First 60 seconds

**Input:**

```bash
bash run.sh
```

**Output (excerpt):**

```
============================================================
  GPT-5.5 INSTANT SYSTEM CARD ANALYSIS
============================================================

Model: GPT-5.5 Instant
Publisher: OpenAI
Context Window: 128,000 tokens
Training Cutoff: 2026-03

============================================================
  PREPAREDNESS FRAMEWORK RISK ASSESSMENT
============================================================

  Chemical, Biological, Radiological, Nuclear         [LOW]
  Cybersecurity                                        [LOW]
  Persuasion and Manipulation                          [LOW]
  Model Autonomy and Self-Replication                  [LOW]

============================================================
  SAFETY BENCHMARK RESULTS
============================================================

  TruthfulQA (accuracy)
    GPT-5.5 Instant: 0.710
    vs GPT-4o:        0.640  ^ better
    vs GPT-5:         0.740  v worse

  ...

============================================================
  EXECUTIVE SUMMARY
============================================================

  Overall Risk: LOW across all Preparedness categories

  Safety vs GPT-4o: 5/5 benchmarks improved
  Safety vs GPT-5:  3/5 benchmarks on par or better
```

## Custom data

To analyze a different system card, create a JSON file matching the schema in `system_card_data.json` and run:

```bash
python3 analyzer.py path/to/your_card.json
```

## Updating the data

To get the latest data from the actual system card:

1. Visit https://openai.com/index/gpt-5-5-instant-system-card
2. Update values in `system_card_data.json` with official numbers
3. Re-run `bash run.sh`
