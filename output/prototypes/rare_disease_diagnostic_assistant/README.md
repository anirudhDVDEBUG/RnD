# Rare Disease Diagnostic Assistant

**AI-assisted phenotype-to-diagnosis matching for undiagnosed rare disease cases.** Takes structured patient phenotype data (HPO terms), scores it against a rare disease knowledge base, and produces ranked differential diagnoses with overlap scores, atypical features, and recommended next tests.

## Headline Result

```
Patient CASE-001 (F, onset 2y): Seizures + Dev delay + Macrocephaly
  #1  PTEN Hamartoma Tumor Syndrome  [HIGH]  60% overlap  → PTEN sequencing, Brain MRI
  #2  Sotos Syndrome                 [MEDIUM] 43% overlap → NSD1 sequencing
  #3  Tuberous Sclerosis Complex     [MEDIUM] 33% overlap → TSC1/TSC2 sequencing
```

Three mock patient cases processed in <1 second, no API keys needed.

## Quick Start

```bash
bash run.sh
```

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** — Installation, skill setup, trigger phrases, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** — Architecture, data flow, limitations, why this matters

## Source

Inspired by [Boston Children's Uses AI to Unlock New Diagnoses](https://openai.com/index/boston-childrens-hospital).
