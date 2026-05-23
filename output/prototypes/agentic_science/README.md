# Agentic Science

**39 scientific skills for AI coding agents** covering single-cell RNA-seq, bulk RNA-seq, epigenomics, GWAS, proteomics, clinical analysis, wet-lab APIs, and scientific reporting. Install once, then ask your agent to run any bioinformatics workflow in natural language.

## Headline result

```
[scRNA] Clustering ARI vs ground truth: 0.998
[BulkDE] Significant DE genes (|LFC|>1, FDR<0.05): 78
[GSEA]  Cell Cycle Regulation    overlap=20  p=3.4e-28 *
```

The demo generates cluster UMAP/t-SNE plots, volcano plots, marker gene tables, and pathway enrichment charts from synthetic data -- no API keys or real datasets required.

## Quick start

```bash
bash run.sh
```

Outputs land in `./output/` (PNGs + CSVs).

## Docs

- **[HOW_TO_USE.md](HOW_TO_USE.md)** -- installation, skill activation, first 60 seconds
- **[TECH_DETAILS.md](TECH_DETAILS.md)** -- architecture, limitations, why it matters
