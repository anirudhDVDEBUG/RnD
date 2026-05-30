---
name: rare_disease_diagnostic_assistant
description: >
  Assists clinicians and researchers in structuring rare disease diagnostic workflows using AI.
  TRIGGER: user mentions rare disease diagnosis, undiagnosed patients, phenotype matching,
  differential diagnosis for rare conditions, or clinical AI for pediatric cases.
---

# Rare Disease Diagnostic Assistant

A skill for building AI-assisted rare disease diagnostic pipelines, inspired by Boston Children's Hospital's approach to using AI to unlock new diagnoses for complex, undiagnosed cases.

## When to use

- "Help me build a rare disease diagnostic tool"
- "Create a phenotype-to-diagnosis matching system"
- "I need to structure clinical data for differential diagnosis of undiagnosed patients"
- "Build an AI pipeline that maps symptoms to rare diseases"
- "Help me create a clinical decision support tool for pediatric rare diseases"

## How to use

### Step 1: Structure Patient Phenotype Data

Organize clinical observations into a structured format using HPO (Human Phenotype Ontology) terms:

```python
patient_profile = {
    "id": "CASE-001",
    "demographics": {"age_onset": "2 years", "sex": "F"},
    "hpo_terms": [
        "HP:0001250",  # Seizures
        "HP:0001263",  # Global developmental delay
        "HP:0000256",  # Macrocephaly
    ],
    "negative_findings": ["HP:0001249"],  # No intellectual disability
    "genetic_tests": ["WES", "CMA"],
    "prior_diagnoses_excluded": []
}
```

### Step 2: Build the Differential Diagnosis Engine

Use an LLM to cross-reference phenotype profiles against known rare disease databases:

```python
import json

def build_diagnostic_prompt(patient):
    return f"""You are a rare disease diagnostic assistant.

Given the following patient phenotype profile, generate a ranked differential
diagnosis list with supporting evidence for each candidate.

Patient Profile:
- HPO Terms: {json.dumps(patient['hpo_terms'])}
- Negative Findings: {json.dumps(patient['negative_findings'])}
- Age of Onset: {patient['demographics']['age_onset']}
- Prior Genetic Testing: {json.dumps(patient['genetic_tests'])}

For each candidate diagnosis, provide:
1. Disease name and OMIM ID
2. Matching phenotype overlap (percentage and specific terms)
3. Non-matching or atypical features
4. Recommended next diagnostic steps (genetic tests, imaging, labs)
5. Confidence level (high/medium/low)

Rank by phenotype overlap and clinical plausibility."""
```

### Step 3: Integrate Reference Databases

Cross-reference results against established rare disease knowledge bases:

- **OMIM** — Online Mendelian Inheritance in Man
- **Orphanet** — Rare disease reference portal
- **HGMD** — Human Gene Mutation Database
- **ClinVar** — Clinical variant interpretations
- **DECIPHER** — Database of genomic variation in clinical context

### Step 4: Generate a Structured Diagnostic Report

```python
report_template = {
    "patient_id": "CASE-001",
    "differential_diagnoses": [
        {
            "rank": 1,
            "disease": "Example Syndrome",
            "omim": "OMIM:123456",
            "phenotype_overlap": 0.85,
            "matching_hpo": ["HP:0001250", "HP:0001263"],
            "atypical_features": ["HP:0000256"],
            "recommended_tests": ["Gene panel X", "Brain MRI"],
            "confidence": "medium"
        }
    ],
    "summary": "Top candidates with rationale",
    "next_steps": ["Recommended follow-up actions"]
}
```

### Step 5: Review and Iterate

- Present results to the clinical team for expert review
- Refine phenotype terms based on new clinical findings
- Re-run the diagnostic pipeline as additional test results arrive
- Track outcomes to improve future diagnostic accuracy

## Key Principles

- **AI assists, clinicians decide.** The tool generates candidates; final diagnosis requires expert clinical judgment.
- **Structured data improves accuracy.** Use standardized ontologies (HPO, OMIM) rather than free-text descriptions.
- **Iterate as data arrives.** Rare disease diagnosis is often a multi-step process — rerun as new findings emerge.
- **Privacy first.** De-identify patient data before processing through any external AI service.
