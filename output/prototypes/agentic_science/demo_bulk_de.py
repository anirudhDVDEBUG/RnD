"""
Demo: Bulk RNA-seq differential expression + gene set enrichment.
Uses scipy stats for DE and a simple Fisher-exact ORA for pathway analysis.
"""

import numpy as np
import pandas as pd
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(123)

# ---------- 1. Simulate bulk RNA-seq counts ----------
N_GENES = 1000
N_SAMPLES = 12  # 6 control + 6 treatment
gene_names = [f"Gene_{i:04d}" for i in range(N_GENES)]
conditions = ["Control"] * 6 + ["Treatment"] * 6

# Base expression
base_expr = np.random.lognormal(mean=5, sigma=1.5, size=(N_GENES, 1))
counts = np.random.negative_binomial(
    n=5, p=5 / (5 + base_expr), size=(N_GENES, N_SAMPLES)
).astype(float)

# Inject differential expression for 80 genes
de_genes = list(range(50, 130))
up_genes = de_genes[:40]
down_genes = de_genes[40:]
counts[up_genes, 6:] *= np.random.uniform(3, 6, size=(len(up_genes), 6))
counts[down_genes, 6:] *= np.random.uniform(0.1, 0.4, size=(len(down_genes), 6))

print(f"[BulkDE] Simulated: {N_GENES} genes, {N_SAMPLES} samples (6 ctrl + 6 trt)")
print(f"[BulkDE] Injected {len(de_genes)} DE genes ({len(up_genes)} up, {len(down_genes)} down)")

# ---------- 2. Normalize (simple CPM) ----------
lib_sizes = counts.sum(axis=0, keepdims=True)
cpm = counts / lib_sizes * 1e6
log_cpm = np.log2(cpm + 1)

# ---------- 3. Differential expression (t-test per gene) ----------
ctrl = log_cpm[:, :6]
trt = log_cpm[:, 6:]
log2fc = trt.mean(axis=1) - ctrl.mean(axis=1)
pvals = np.array([ttest_ind(ctrl[i], trt[i]).pvalue for i in range(N_GENES)])
_, padj, _, _ = multipletests(pvals, method="fdr_bh")

de_df = pd.DataFrame({
    "gene": gene_names,
    "log2FoldChange": log2fc.round(3),
    "pvalue": pvals,
    "padj": padj,
})
de_df["significant"] = (de_df["padj"] < 0.05) & (de_df["log2FoldChange"].abs() > 1)
n_sig = de_df["significant"].sum()
print(f"[BulkDE] Significant DE genes (|LFC|>1, FDR<0.05): {n_sig}")

de_df.to_csv(f"{OUTPUT_DIR}/bulk_de_results.csv", index=False)
print(f"[BulkDE] Saved DE table -> {OUTPUT_DIR}/bulk_de_results.csv")

# ---------- 4. Volcano plot ----------
fig, ax = plt.subplots(figsize=(8, 6))
neg_log10p = -np.log10(de_df["padj"].clip(lower=1e-50))
colors = ["#aaaaaa"] * N_GENES
for i in range(N_GENES):
    if de_df.iloc[i]["significant"]:
        colors[i] = "#e74c3c" if de_df.iloc[i]["log2FoldChange"] > 0 else "#3498db"
ax.scatter(de_df["log2FoldChange"], neg_log10p, c=colors, s=8, alpha=0.7)
ax.axhline(-np.log10(0.05), ls="--", color="grey", lw=0.8)
ax.axvline(1, ls="--", color="grey", lw=0.8)
ax.axvline(-1, ls="--", color="grey", lw=0.8)
ax.set_xlabel("log2 Fold Change", fontsize=12)
ax.set_ylabel("-log10(adjusted p-value)", fontsize=12)
ax.set_title("Volcano Plot: Treatment vs Control", fontsize=13)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/volcano_plot.png", dpi=120)
print(f"[BulkDE] Saved volcano plot -> {OUTPUT_DIR}/volcano_plot.png")

# ---------- 5. Mock pathway enrichment (ORA) ----------
from scipy.stats import fisher_exact

# Define mock pathways
pathways = {
    "Cell Cycle Regulation": set(range(50, 70)),
    "Apoptosis Signaling": set(range(70, 90)),
    "Immune Response": set(range(100, 130)),
    "Metabolism": set(range(200, 240)),
    "DNA Repair": set(range(300, 330)),
    "Signal Transduction": set(range(400, 440)),
}

sig_genes = set(de_df[de_df["significant"]].index)
all_genes = set(range(N_GENES))

print(f"\n[GSEA] Over-representation analysis (Fisher's exact):")
print(f"{'Pathway':<28} {'Overlap':>8} {'Size':>6} {'p-value':>10} {'Sig':>5}")
print("-" * 62)

ora_results = []
for pathway_name, pathway_genes in pathways.items():
    overlap = len(sig_genes & pathway_genes)
    a = overlap
    b = len(sig_genes) - overlap
    c = len(pathway_genes) - overlap
    d = len(all_genes) - len(sig_genes) - c
    _, pval = fisher_exact([[a, b], [c, d]], alternative="greater")
    sig_flag = "*" if pval < 0.05 else ""
    print(f"  {pathway_name:<26} {overlap:>8} {len(pathway_genes):>6} {pval:>10.2e} {sig_flag:>5}")
    ora_results.append({
        "pathway": pathway_name,
        "overlap": overlap,
        "pathway_size": len(pathway_genes),
        "pvalue": pval,
        "significant": pval < 0.05,
    })

ora_df = pd.DataFrame(ora_results)
ora_df.to_csv(f"{OUTPUT_DIR}/pathway_enrichment.csv", index=False)
print(f"\n[GSEA] Saved enrichment table -> {OUTPUT_DIR}/pathway_enrichment.csv")

# ---------- 6. Enrichment bar plot ----------
ora_df_sig = ora_df.sort_values("pvalue")
fig, ax = plt.subplots(figsize=(8, 4))
colors_bar = ["#e74c3c" if s else "#95a5a6" for s in ora_df_sig["significant"]]
ax.barh(ora_df_sig["pathway"], -np.log10(ora_df_sig["pvalue"]), color=colors_bar)
ax.axvline(-np.log10(0.05), ls="--", color="grey", lw=0.8, label="p=0.05")
ax.set_xlabel("-log10(p-value)", fontsize=12)
ax.set_title("Pathway Enrichment (Over-Representation Analysis)", fontsize=13)
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/pathway_enrichment.png", dpi=120)
print(f"[GSEA] Saved enrichment plot -> {OUTPUT_DIR}/pathway_enrichment.png")
