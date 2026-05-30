# How to Use

## Install

```bash
# Clone / copy this directory
cd rare_disease_diagnostic_assistant

# No external deps — pure Python 3.10+ stdlib
pip install -r requirements.txt   # (no-op, but included for convention)
```

## Run the Demo

```bash
bash run.sh
```

Processes three mock patient cases and prints differential diagnosis reports to the terminal. No API keys, no network access needed.

## Use as a Claude Code Skill

### 1. Drop the skill file

```bash
mkdir -p ~/.claude/skills/rare_disease_diagnostic_assistant
cp SKILL.md ~/.claude/skills/rare_disease_diagnostic_assistant/SKILL.md
```

### 2. Trigger phrases

Say any of these to Claude Code and it will activate the skill:

- "Help me build a rare disease diagnostic tool"
- "Create a phenotype-to-diagnosis matching system"
- "I need to structure clinical data for differential diagnosis of undiagnosed patients"
- "Build an AI pipeline that maps symptoms to rare diseases"
- "Help me create a clinical decision support tool for pediatric rare diseases"

The skill triggers on keywords: **rare disease diagnosis**, **undiagnosed patients**, **phenotype matching**, **differential diagnosis for rare conditions**, **clinical AI for pediatric cases**.

### 3. What Claude will do

When triggered, Claude will:

1. Help you structure patient phenotype data using HPO terms
2. Build or customize the diagnostic matching engine
3. Cross-reference against OMIM/Orphanet disease databases
4. Generate structured diagnostic reports with ranked candidates
5. Suggest next diagnostic steps (genetic tests, imaging, labs)

## First 60 Seconds

**Input:** Run `bash run.sh` or invoke via Claude Code with a patient description.

**Output (abbreviated):**

```
Patient CASE-001
  Sex: F  |  Onset: 2 years
  Phenotype (positive):
    HP:0001250 — Seizures
    HP:0001263 — Global developmental delay
    HP:0000256 — Macrocephaly
  Phenotype (negative/absent):
    HP:0001249 — Intellectual disability

========================================================================
  RARE DISEASE DIAGNOSTIC REPORT
========================================================================
  Patient: CASE-001
  Phenotypes entered: 3  |  Negatives: 1
  Diseases screened: 8

  #1  PTEN Hamartoma Tumor Syndrome  [HIGH confidence]
      OMIM: OMIM:158350  |  Gene: PTEN
      Overlap: 60%
      Matching HPO: HP:0000256, HP:0001250, HP:0001263
        (Macrocephaly, Seizures, Global developmental delay)
      Atypical/missing: Autistic behavior
      Recommended tests: PTEN gene sequencing; Brain MRI

  #2  Sotos Syndrome  [MEDIUM confidence]
      ...

  NEXT STEPS
    - [PTEN Hamartoma] PTEN gene sequencing
    - [PTEN Hamartoma] Brain MRI
    - [Sotos Syndrome] NSD1 gene sequencing / MLPA
    - Present differential to multidisciplinary team for review.
========================================================================
```

Plus a full JSON dump of the structured report for programmatic use.

## Customization

Edit `hpo_data.py` to add more diseases, HPO terms, or recommended tests. Edit `demo.py` to change the mock patient cases or integrate with a real HPO API.
