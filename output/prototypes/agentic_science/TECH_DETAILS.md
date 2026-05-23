# Technical Details

## What it actually does

Agentic Science is a **skill pack** -- a collection of 39 markdown files that inject domain-specific bioinformatics knowledge into AI coding agents. Each skill file teaches the agent how to write and execute a specific analysis pipeline (e.g., "single-cell QC and clustering" or "GWAS fine-mapping"). The agent reads the relevant skill at prompt time, then generates and runs Python code using standard bioinformatics libraries (scanpy, PyDESeq2, GSEApy, pysam, etc.).

The skill pack does not contain executable code itself. It contains structured instructions, best-practice recipes, parameter recommendations, and output format specifications that guide the agent through each analysis type. Think of it as a bioinformatics textbook that lives in the agent's context window.

## Architecture

```
User prompt ("analyze this scRNA-seq data")
  |
  v
Agent matches trigger phrases --> loads relevant skill .md files
  |
  v
Skill file provides:
  - Step-by-step analysis recipe
  - Recommended libraries + function calls
  - Default parameters + QC thresholds
  - Output format specs (plots, tables, reports)
  |
  v
Agent generates + executes Python code
  |
  v
Results: figures, CSV tables, reproducible notebook
```

### Key files in the source repo

- `SKILL.md` -- top-level skill definition with trigger rules
- `skills/*.md` -- 39 individual skill files organized by domain:
  - **scRNA-seq** (8 skills): QC, normalization, HVG selection, PCA, clustering, marker genes, trajectory, cell type annotation
  - **Bulk RNA-seq** (5 skills): counting, normalization, DE (DESeq2-style), visualization, batch correction
  - **GSEA** (3 skills): pre-ranked GSEA, ORA, pathway databases
  - **Epigenomics** (5 skills): ChIP-seq peaks, ATAC-seq, motif enrichment, chromatin state, differential peaks
  - **Statistical genetics** (4 skills): GWAS summary stats, LD, fine-mapping, PRS
  - **Functional genomics** (3 skills): variant annotation, regulatory elements, eQTL
  - **Proteomics** (3 skills): mass spec processing, quantification, PTM analysis
  - **Clinical** (4 skills): survival analysis, biomarker discovery, clinical trials, patient stratification
  - **Wet-lab APIs** (2 skills): LIMS integration, instrument control
  - **Reporting** (2 skills): figure generation, methods section drafting

### Dependencies (for real analysis)

| Library | Purpose |
|---------|---------|
| scanpy / anndata | Single-cell RNA-seq |
| PyDESeq2 | Bulk differential expression |
| GSEApy | Gene set enrichment |
| pysam | BAM/SAM file handling |
| pybedtools | Genomic interval operations |
| matplotlib / seaborn | Visualization |
| pandas / numpy / scipy | Core data handling |

The demo in this repo substitutes lightweight equivalents (sklearn, scipy.stats) so it runs without the full bio stack.

## Limitations

- **No data included.** Skills generate code; you supply the data (.h5ad, count matrices, BAM files, etc.).
- **Python-only pipelines.** R-based tools (DESeq2 via R, Seurat) are not directly supported -- PyDESeq2 is used as the Python equivalent.
- **No model fine-tuning.** The skills are prompt-injected instructions, not trained adapters. Quality depends on the base model's coding ability.
- **Wet-lab API skills are thin.** They provide templates for LIMS/instrument integration but require site-specific configuration.
- **No multi-omics integration skill.** Individual modalities are covered but there's no dedicated skill for joint analysis (e.g., CITE-seq, spatial + scRNA).
- **Dependent on agent context window.** Loading many skills simultaneously may crowd out user data context in smaller models.

## Why it matters for Claude-driven products

1. **Agent factories / vertical SaaS.** If you're building domain-specific agents for biotech, pharma, or academic labs, this skill pack is a ready-made knowledge layer. Drop it in and your agent can handle the most common bioinformatics requests without custom training.

2. **Lead-gen for biotech tools.** A Claude-powered assistant that can actually run scRNA-seq analysis or GWAS pipelines is a compelling demo for biotech prospects. The skill pack turns a generic coding agent into a domain expert.

3. **Reproducible science.** Every analysis the agent produces comes with code, parameters, and outputs -- making it auditable and reproducible. This matters for regulated environments (clinical trials, FDA submissions).

4. **Skills.sh ecosystem.** This is one of the larger skill packs on skills.sh, demonstrating that the skill-file pattern scales to complex technical domains. Useful reference if you're building your own skill packs for other verticals.
