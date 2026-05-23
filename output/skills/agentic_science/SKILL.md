---
name: Agentic Science
description: |
  39 scientific skills for AI coding agents covering single-cell and bulk RNA-seq, epigenomics, statistical genetics, functional genomics, proteomics, clinical analysis, wet-lab APIs, and scientific reporting.
  TRIGGER when: user asks about RNA-seq analysis, single-cell sequencing, differential expression, gene set enrichment, epigenomics, GWAS, proteomics, scientific data analysis, bioinformatics pipelines, or wet-lab automation.
  DO NOT TRIGGER when: general data science, non-biological statistics, or unrelated programming tasks.
---

# Agentic Science

Open-source skillpack providing 39 scientific skills for AI coding agents. Covers the full spectrum of computational biology: single-cell and bulk RNA-seq, epigenomics, statistical genetics, functional genomics, proteomics, clinical analysis, wet-lab API integration, and scientific reporting.

## When to use

- "Analyze this single-cell RNA-seq dataset and identify cell clusters"
- "Run differential expression analysis on these bulk RNA-seq counts"
- "Perform gene set enrichment analysis on my DE results"
- "Help me build an epigenomics or GWAS analysis pipeline"
- "Generate a scientific report from these proteomics or clinical trial results"

## How to use

1. **Install the skillpack** via skills.sh or directly from the repository:
   ```bash
   # Via skills.sh
   skills install 001TMF/agentic-science

   # Or clone directly
   git clone https://github.com/001TMF/agentic-science.git
   ```

2. **Ensure dependencies are available.** Most skills rely on standard Python bioinformatics libraries:
   ```bash
   pip install scanpy anndata pandas numpy scipy matplotlib seaborn
   pip install pydeseq2 gseapy pysam pybedtools
   ```

3. **Invoke a skill by describing your scientific task.** The skillpack covers:
   - **Single-cell RNA-seq:** QC, normalization, clustering, trajectory inference, cell type annotation
   - **Bulk RNA-seq:** Read counting, differential expression (DESeq2-style), visualization
   - **Gene set enrichment:** GSEA, over-representation analysis, pathway databases
   - **Epigenomics:** ChIP-seq, ATAC-seq peak analysis, motif enrichment
   - **Statistical genetics:** GWAS summary statistics, LD analysis, fine-mapping
   - **Functional genomics:** Variant annotation, regulatory element analysis
   - **Proteomics:** Mass spec data processing, protein quantification
   - **Clinical analysis:** Survival analysis, biomarker discovery
   - **Wet-lab APIs:** Integration with lab information systems and instrument APIs
   - **Scientific reporting:** Automated figure generation, methods sections, reproducible notebooks

4. **Example workflow — single-cell RNA-seq:**
   ```
   User: "I have a 10X Genomics h5ad file. Run standard preprocessing,
          cluster the cells, and identify marker genes."

   The agent will:
   - Load the dataset with scanpy
   - Filter cells/genes, normalize, log-transform
   - Find highly variable genes, run PCA, build neighbor graph
   - Cluster with Leiden algorithm
   - Compute marker genes per cluster with rank_genes_groups
   - Generate UMAP plots and marker gene dot plots
   ```

5. **Example workflow — bulk RNA-seq differential expression:**
   ```
   User: "Compare treatment vs control from this counts matrix and
          run pathway analysis on significant genes."

   The agent will:
   - Load counts and metadata
   - Run differential expression with PyDESeq2
   - Filter by adjusted p-value and log2 fold change
   - Generate volcano and MA plots
   - Run GSEA against MSigDB or KEGG pathways
   - Produce a summary report with key findings
   ```

## References

- **Source repository:** https://github.com/001TMF/agentic-science
- **Skills.sh registry:** https://skills.sh
- **Key dependencies:** [Scanpy](https://scanpy.readthedocs.io/), [PyDESeq2](https://pydeseq2.readthedocs.io/), [GSEApy](https://gseapy.readthedocs.io/)
