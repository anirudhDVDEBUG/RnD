# Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use

A runnable demo of the **Trace-Free+** framework principles from [arXiv:2602.20426](https://arxiv.org/abs/2602.20426). It takes a catalog of vague, human-oriented tool descriptions and rewrites them so LLM agents can select the correct tool more reliably — especially as catalogs grow large.

## What it does

1. **Audits** an 8-tool restaurant API catalog, flagging ambiguous phrasing, vague parameters, and missing return schemas.
2. **Rewrites** every description using the Trace-Free+ principles: discriminative verb-object leads, explicit NOT-boundaries, typed parameters, return schemas, canonical examples, and cross-references.
3. **Validates** accuracy by running 16 contrastive queries through a TF-IDF cosine-similarity tool selector, comparing the original vs. rewritten catalog.

No external API keys are needed — tool selection is simulated with TF-IDF matching from the Python standard library.

## Install

```bash
# Python 3.10+ required, no pip dependencies
pip install -r requirements.txt   # (empty — stdlib only)
```

## Run

```bash
bash run.sh
```

## Expected output

```
STEP 1: AUDIT ORIGINAL CATALOG
  [1] AMBIGUOUS: 'get_reviews' and 'get_restaurants' share similar leading phrase...
  [2] VAGUE PARAM: 'get_restaurants.q' has a generic name...
  ...
  Total issues found: ~12

STEP 2: REWRITE EXAMPLE (get_restaurants)
  BEFORE:  "Get data from the restaurant API."
  AFTER:   "Search restaurant listings by location and cuisine type. ..."

STEP 3: FULL REWRITTEN CATALOG
  (8 tools with discriminative descriptions, typed params, examples)

STEP 4: CONTRASTIVE QUERY VALIDATION
  Original catalog:  ~6/16 (38%)
  Rewritten catalog: ~13/16 (81%)
  Improvement:       +7 correct selections (44% points)
```

Exact numbers depend on TF-IDF token overlap; the rewritten catalog consistently outperforms the original.

## Key principles applied

1. Lead with a unique, discriminative verb-object phrase
2. State what each tool does NOT do
3. Enumerate parameters with types, defaults, and constraints inline
4. Specify the return schema concisely
5. Include a single canonical example per tool
6. Keep total length under 200 words
7. Cross-reference commonly confused tools
8. Validate with contrastive queries

## Reference

- Paper: [Learning to Rewrite Tool Descriptions for Reliable LLM-Agent Tool Use](https://arxiv.org/abs/2602.20426)
