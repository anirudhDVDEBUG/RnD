"""Mock oncology guideline knowledge base (stands in for 70+ NCCN/ESMO guidelines).

In production, these would be loaded from PDF/structured sources and embedded
with PubMedBERT into a ChromaDB vector store.
"""

GUIDELINES = [
    {
        "id": "NCCN-NSCLC-2024-01",
        "title": "NCCN NSCLC Guidelines v4.2024 — First-Line Therapy",
        "cancer_type": "nsclc",
        "content": (
            "For metastatic NSCLC with EGFR exon 19 deletion or L858R mutation, "
            "first-line osimertinib (80 mg daily) is the preferred regimen (Category 1). "
            "Median PFS: 18.9 months vs 10.2 months for comparator TKIs. "
            "Continue until disease progression or unacceptable toxicity. "
            "Monitor for ILD/pneumonitis and QTc prolongation."
        ),
        "keywords": ["nsclc", "egfr", "osimertinib", "first-line", "exon 19", "l858r"],
    },
    {
        "id": "NCCN-NSCLC-2024-02",
        "title": "NCCN NSCLC Guidelines v4.2024 — ALK-Positive",
        "cancer_type": "nsclc",
        "content": (
            "For ALK-positive metastatic NSCLC, alectinib 600 mg BID is preferred "
            "first-line therapy (Category 1). Alternative: lorlatinib 100 mg daily. "
            "CNS activity is a key consideration for drug selection. "
            "Median PFS with alectinib: 34.8 months (ALEX trial)."
        ),
        "keywords": ["nsclc", "alk", "alectinib", "lorlatinib", "cns"],
    },
    {
        "id": "NCCN-NSCLC-2024-03",
        "title": "NCCN NSCLC Guidelines v4.2024 — Immunotherapy",
        "cancer_type": "nsclc",
        "content": (
            "For metastatic NSCLC without driver mutations, PD-L1 >= 50%: "
            "pembrolizumab monotherapy 200 mg Q3W is preferred (Category 1). "
            "For PD-L1 1-49%: pembrolizumab + platinum-doublet chemotherapy. "
            "For PD-L1 < 1%: platinum-doublet + pembrolizumab + pemetrexed (nonsquamous)."
        ),
        "keywords": ["nsclc", "immunotherapy", "pembrolizumab", "pd-l1", "checkpoint"],
    },
    {
        "id": "NCCN-BREAST-2024-01",
        "title": "NCCN Breast Cancer Guidelines — HER2-Positive",
        "cancer_type": "breast",
        "content": (
            "For HER2-positive metastatic breast cancer, first-line: "
            "pertuzumab + trastuzumab + docetaxel (Category 1, CLEOPATRA trial). "
            "Second-line: T-DXd (trastuzumab deruxtecan) based on DESTINY-Breast03. "
            "Monitor LVEF every 3 months during trastuzumab therapy."
        ),
        "keywords": ["breast", "her2", "trastuzumab", "pertuzumab", "t-dxd"],
    },
    {
        "id": "NCCN-BREAST-2024-02",
        "title": "NCCN Breast Cancer Guidelines — HR+/HER2-",
        "cancer_type": "breast",
        "content": (
            "For HR+/HER2- metastatic breast cancer, first-line: "
            "CDK4/6 inhibitor (ribociclib, palbociclib, or abemaciclib) + "
            "aromatase inhibitor (Category 1). Ribociclib + letrozole showed "
            "OS benefit in MONALEESA-2. Monitor CBC and LFTs."
        ),
        "keywords": ["breast", "hr-positive", "cdk4/6", "ribociclib", "palbociclib", "endocrine"],
    },
    {
        "id": "NCCN-CRC-2024-01",
        "title": "NCCN Colon Cancer Guidelines — First-Line Metastatic",
        "cancer_type": "colorectal",
        "content": (
            "For metastatic CRC, RAS wild-type, left-sided: FOLFOX or FOLFIRI + "
            "cetuximab or panitumumab (Category 1). For RAS-mutant: FOLFOX or "
            "FOLFIRI + bevacizumab. MSI-H/dMMR tumors: pembrolizumab first-line "
            "(KEYNOTE-177, Category 1)."
        ),
        "keywords": ["colorectal", "colon", "folfox", "folfiri", "cetuximab", "ras", "msi-h"],
    },
    {
        "id": "ESMO-MELANOMA-2024-01",
        "title": "ESMO Melanoma Guidelines — Advanced/Metastatic",
        "cancer_type": "melanoma",
        "content": (
            "For BRAF V600-mutant advanced melanoma: combination BRAF+MEK inhibition "
            "(dabrafenib+trametinib or encorafenib+binimetinib). "
            "For BRAF wild-type or as alternative: nivolumab + ipilimumab combination "
            "immunotherapy. Median OS with nivo+ipi: 72.1 months (CheckMate 067)."
        ),
        "keywords": ["melanoma", "braf", "dabrafenib", "nivolumab", "ipilimumab", "immunotherapy"],
    },
    {
        "id": "NCCN-PANCREATIC-2024-01",
        "title": "NCCN Pancreatic Cancer Guidelines — Metastatic",
        "cancer_type": "pancreatic",
        "content": (
            "For metastatic pancreatic adenocarcinoma, good PS (ECOG 0-1): "
            "FOLFIRINOX (Category 1) or gemcitabine + nab-paclitaxel (Category 1). "
            "For BRCA1/2-mutated: maintenance olaparib after platinum-based chemo "
            "(POLO trial). Median OS with FOLFIRINOX: 11.1 months."
        ),
        "keywords": ["pancreatic", "folfirinox", "gemcitabine", "brca", "olaparib"],
    },
]


def keyword_search(query: str, top_k: int = 5) -> list:
    """Simple keyword-overlap retrieval (stands in for vector similarity search)."""
    query_tokens = set(query.lower().split())
    scored = []
    for g in GUIDELINES:
        kw_set = set(g["keywords"])
        overlap = len(query_tokens & kw_set)
        # Also check content word overlap for broader matching
        content_tokens = set(g["content"].lower().split())
        content_overlap = len(query_tokens & content_tokens)
        score = overlap * 3 + content_overlap  # keyword matches weighted higher
        if score > 0:
            scored.append((score, g))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_k]]
