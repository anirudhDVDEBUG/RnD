# Technical Details

## What It Does

This prototype implements a phenotype-driven rare disease differential diagnosis engine. It takes a patient profile expressed as HPO (Human Phenotype Ontology) terms, computes Jaccard-like overlap scores against a built-in rare disease knowledge base (8 diseases, expandable), penalizes candidates that conflict with negative findings, and produces ranked diagnostic reports with confidence levels, matching/atypical features, and recommended next tests.

The approach mirrors what Boston Children's Hospital described in their collaboration with OpenAI: structuring complex, multi-system patient presentations into standardized phenotype vocabularies, then using computational matching to surface candidate diagnoses that a clinician might not immediately consider — especially for the ~7,000 known rare diseases where any single clinician's experience is limited.

## Architecture

```
demo.py                  Entry point — defines 3 mock patient cases, runs engine, prints reports
diagnostic_engine.py     Core logic — PatientProfile, overlap scoring, ranking, report generation
hpo_data.py              Mock knowledge base — HPO terms, 8 rare diseases, recommended tests
run.sh                   One-command runner
```

### Data Flow

```
Patient HPO terms + negatives
        |
        v
  compute_overlap()       Jaccard overlap with penalty for negative contradictions
        |
        v
  rank_diagnoses()        Sort by overlap, assign confidence (high/medium/low)
        |
        v
  generate_report()       Structured dict with differentials, summary, next steps
        |
        v
  format_report_text()    Terminal-friendly pretty print
  json.dumps()            Machine-readable structured output
```

### Key Design Choices

- **Jaccard overlap with negative penalty**: `overlap = |patient ∩ disease| / |patient ∪ disease|`, reduced by 25% per contradicted negative finding. Simple but effective for small phenotype sets.
- **No LLM dependency for core matching**: The engine runs entirely offline with deterministic scoring. An LLM layer (Claude API) would sit on top for natural-language phenotype extraction, nuanced clinical reasoning, and report narratives.
- **Structured I/O**: Reports are generated as Python dicts / JSON, making them easy to pipe into downstream systems (EHR integrations, clinical dashboards, LLM prompts).

### Dependencies

None beyond Python 3.10+ stdlib. In a production build, you'd add:

- `anthropic` SDK — for LLM-powered phenotype extraction from clinical notes and refined differential reasoning
- `requests` — for live OMIM/Orphanet/HPO API queries
- A database (PostgreSQL, SQLite) — for persistent patient case tracking

## Limitations

- **Toy knowledge base**: Only 8 diseases. Real deployment needs OMIM's 8,000+ entries.
- **No NLP phenotype extraction**: Expects pre-coded HPO terms. Production would use an LLM to extract HPO terms from free-text clinical notes.
- **Simple scoring**: Jaccard overlap doesn't account for phenotype specificity (a rare symptom should count more than a common one). Information-content weighting (as used by tools like Exomiser) would improve accuracy.
- **No genomic integration**: Doesn't process VCF/variant data. A real pipeline would integrate with variant prioritization tools.
- **No HIPAA/compliance layer**: Mock data only. Real deployment needs de-identification, audit logging, and access controls.

## Why This Matters for Claude-Driven Products

1. **Clinical decision support is a high-value vertical**: Rare disease diagnosis affects ~400M people globally. AI tools that reduce the average 5-7 year diagnostic odyssey have clear clinical and commercial value.

2. **Structured skill pattern**: This demonstrates how to build a domain-specific Claude Code skill — trigger on domain keywords, provide structured workflows, output actionable results. The same pattern applies to agent factories building vertical SaaS tools.

3. **LLM + deterministic hybrid**: The core matching is deterministic (fast, auditable, reproducible), while the LLM layer handles the messy parts (NLP extraction, nuanced reasoning, report generation). This architecture is applicable to any domain where you need both reliability and flexibility.

4. **Lead-gen / marketing angle**: Healthcare AI tools that demonstrably reduce diagnostic time are strong case studies for AI consulting firms, health-tech startups, and enterprise sales teams targeting hospital systems.

## References

- [Boston Children's Uses AI to Unlock New Diagnoses](https://openai.com/index/boston-childrens-hospital)
- [Human Phenotype Ontology](https://hpo.jax.org/)
- [OMIM](https://omim.org/)
- [Orphanet](https://www.orpha.net/)
- [Exomiser](https://exomiser.monarchinitiative.org/) — phenotype-aware variant prioritization
