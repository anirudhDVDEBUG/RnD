# How to Use Agentic Science

## What it is

A **Claude Code skill pack** (also works with Codex, Cursor, Copilot, Windsurf, and 45+ agents via skills.sh). It gives your AI coding agent 39 bioinformatics skills so you can say "run differential expression on this counts matrix" and get working code + results.

## Installation

### Option A: via skills.sh (recommended)

```bash
skills install 001TMF/agentic-science
```

This auto-places skill files where your agent can find them.

### Option B: manual install for Claude Code

```bash
git clone https://github.com/001TMF/agentic-science.git
cp -r agentic-science/.skills/* ~/.claude/skills/
```

The skill files land in `~/.claude/skills/agentic-science/`. Claude Code loads them automatically on next session start.

### Option C: clone and use directly

```bash
git clone https://github.com/001TMF/agentic-science.git
cd agentic-science
pip install scanpy anndata pandas numpy scipy matplotlib seaborn pydeseq2 gseapy
```

Then open the repo in your AI editor and prompt it.

### Python dependencies (for real analysis)

```bash
pip install scanpy anndata pandas numpy scipy matplotlib seaborn
pip install pydeseq2 gseapy pysam pybedtools
```

The demo in this repo uses only lightweight deps (numpy, scipy, sklearn, matplotlib, statsmodels) so you can evaluate without installing the full bio stack.

## Trigger phrases

Once installed, the skill activates when you say things like:

| Phrase | Skill area |
|--------|-----------|
| "Analyze this single-cell RNA-seq dataset" | scRNA-seq pipeline |
| "Run differential expression on these counts" | Bulk RNA-seq DE |
| "Perform gene set enrichment analysis" | GSEA / ORA |
| "Build a ChIP-seq peak analysis pipeline" | Epigenomics |
| "Analyze these GWAS summary statistics" | Statistical genetics |
| "Process this mass spec proteomics data" | Proteomics |
| "Run survival analysis on this clinical data" | Clinical analysis |
| "Generate a scientific report" | Reporting |

It does **not** trigger for general data science, non-biological statistics, or unrelated programming.

## First 60 seconds

```bash
# 1. Run the demo (no API keys needed)
bash run.sh

# 2. Check outputs
ls output/
#  scrna_clusters.png       -- t-SNE cluster plot (ground truth vs predicted)
#  scrna_markers.csv        -- top marker genes per cluster
#  volcano_plot.png         -- differential expression volcano
#  bulk_de_results.csv      -- full DE table (gene, LFC, padj)
#  pathway_enrichment.png   -- enrichment bar chart
#  pathway_enrichment.csv   -- pathway ORA results

# 3. With real data (after installing full deps):
#    Open your Claude Code session in a directory containing an .h5ad file:
#    > "Load my_data.h5ad, run standard scRNA-seq preprocessing,
#       cluster the cells, and find marker genes."
```

### Expected demo output (abbreviated)

```
[scRNA] Simulated count matrix: 2000 cells x 500 genes, 5 clusters
[scRNA] After QC: 1900 cells, 475 genes
[scRNA] Clustering ARI vs ground truth: 0.998
[scRNA] Top 3 marker genes per cluster (Wilcoxon rank-sum):
  Cluster 0: Gene_4(LFC=2.14), Gene_12(LFC=1.97), Gene_0(LFC=1.89)
  ...

[BulkDE] Significant DE genes (|LFC|>1, FDR<0.05): 78
[GSEA]  Cell Cycle Regulation  overlap=20  p=3.4e-28 *
```

## Skill file location (Claude Code)

```
~/.claude/skills/
  agentic-science/
    SKILL.md          # Main skill definition (trigger rules + instructions)
    skills/           # Individual skill files (39 total)
      scrna_qc.md
      scrna_clustering.md
      bulk_de.md
      gsea.md
      chipseq.md
      gwas.md
      ...
```
