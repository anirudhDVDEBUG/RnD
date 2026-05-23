"""
Demo: Single-cell RNA-seq analysis pipeline using synthetic data.
Mirrors what Agentic Science skills do with scanpy, but uses only
numpy/scipy/sklearn so the demo runs without heavy bio-deps.
"""

import numpy as np
import pandas as pd
from scipy.sparse import random as sparse_random
from scipy.stats import mannwhitneyu
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

np.random.seed(42)

# ---------- 1. Simulate a 2000-cell x 500-gene count matrix ----------
N_CELLS, N_GENES = 2000, 500
N_CLUSTERS = 5

# Assign ground-truth clusters
true_labels = np.repeat(np.arange(N_CLUSTERS), N_CELLS // N_CLUSTERS)

# Base expression + cluster-specific marker genes
counts = np.random.poisson(lam=2, size=(N_CELLS, N_GENES)).astype(float)
for k in range(N_CLUSTERS):
    marker_start = k * 20
    marker_end = marker_start + 20
    mask = true_labels == k
    counts[mask, marker_start:marker_end] += np.random.poisson(lam=8, size=(mask.sum(), 20))

gene_names = [f"Gene_{i}" for i in range(N_GENES)]
cell_ids = [f"Cell_{i}" for i in range(N_CELLS)]

print(f"[scRNA] Simulated count matrix: {N_CELLS} cells x {N_GENES} genes, {N_CLUSTERS} clusters")

# ---------- 2. QC: filter low-count cells/genes ----------
cell_counts = counts.sum(axis=1)
gene_counts = counts.sum(axis=0)
keep_cells = cell_counts > np.percentile(cell_counts, 5)
keep_genes = gene_counts > np.percentile(gene_counts, 5)
counts = counts[keep_cells][:, keep_genes]
true_labels = true_labels[keep_cells]
gene_names = [gene_names[i] for i, k in enumerate(keep_genes) if k]
print(f"[scRNA] After QC: {counts.shape[0]} cells, {counts.shape[1]} genes")

# ---------- 3. Normalize (CPM-like) + log1p ----------
lib_size = counts.sum(axis=1, keepdims=True)
norm = counts / lib_size * 1e4
log_norm = np.log1p(norm)

# ---------- 4. HVG selection (top variance) ----------
gene_var = log_norm.var(axis=0)
hvg_idx = np.argsort(gene_var)[-200:]
X_hvg = log_norm[:, hvg_idx]

# ---------- 5. PCA ----------
pca = PCA(n_components=20)
X_pca = pca.fit_transform(X_hvg)
print(f"[scRNA] PCA: {pca.explained_variance_ratio_[:3].round(3)} (first 3 components)")

# ---------- 6. Clustering (KMeans as Leiden proxy) ----------
km = KMeans(n_clusters=N_CLUSTERS, n_init=10, random_state=42)
pred_labels = km.fit_predict(X_pca)

from sklearn.metrics import adjusted_rand_score
ari = adjusted_rand_score(true_labels, pred_labels)
print(f"[scRNA] Clustering ARI vs ground truth: {ari:.3f}")

# ---------- 7. t-SNE embedding ----------
tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_2d = tsne.fit_transform(X_pca)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for ax, labels, title in zip(axes, [true_labels, pred_labels], ["Ground Truth", "Predicted Clusters"]):
    scatter = ax.scatter(X_2d[:, 0], X_2d[:, 1], c=labels, cmap="tab10", s=5, alpha=0.7)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel("t-SNE 1")
    ax.set_ylabel("t-SNE 2")
    plt.colorbar(scatter, ax=ax, label="Cluster")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/scrna_clusters.png", dpi=120)
print(f"[scRNA] Saved cluster plot -> {OUTPUT_DIR}/scrna_clusters.png")

# ---------- 8. Marker gene detection (Wilcoxon) ----------
print("\n[scRNA] Top 3 marker genes per cluster (Wilcoxon rank-sum):")
hvg_names = [gene_names[i] for i in hvg_idx]
marker_results = []
for k in range(N_CLUSTERS):
    in_cluster = pred_labels == k
    scores = []
    for g in range(X_hvg.shape[1]):
        stat, pval = mannwhitneyu(X_hvg[in_cluster, g], X_hvg[~in_cluster, g], alternative="greater")
        lfc = X_hvg[in_cluster, g].mean() - X_hvg[~in_cluster, g].mean()
        scores.append((hvg_names[g], lfc, pval))
    scores.sort(key=lambda x: x[2])
    top3 = scores[:3]
    marker_results.append(top3)
    genes_str = ", ".join(f"{g}(LFC={l:.2f})" for g, l, p in top3)
    print(f"  Cluster {k}: {genes_str}")

# Save marker table
rows = []
for k, markers in enumerate(marker_results):
    for gene, lfc, pval in markers:
        rows.append({"cluster": k, "gene": gene, "log2FC": round(lfc, 3), "pvalue": pval})
pd.DataFrame(rows).to_csv(f"{OUTPUT_DIR}/scrna_markers.csv", index=False)
print(f"[scRNA] Saved marker table -> {OUTPUT_DIR}/scrna_markers.csv")
