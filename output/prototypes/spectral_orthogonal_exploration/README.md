# Spectral Orthogonal Exploration (SOE) — Prototype Demo

Demonstrates the core inference-time framework from ["Student Guides Teacher: Weak-to-Strong Inference via Spectral Orthogonal Exploration"](https://arxiv.org/abs/2601.06160).

## What it does

SOE mitigates **reasoning collapse** — the phenomenon where temperature sampling produces only lexical variants of the same flawed reasoning — by injecting orthogonal signals from a weaker "student" model into a stronger "teacher" model's hidden-state subspace.

This prototype simulates the full SOE pipeline:

1. **Extracts dominant subspace** of teacher's hidden states via SVD
2. **Projects student signals** onto the teacher's orthogonal complement
3. **Injects the orthogonal signal** (scaled by alpha) into teacher's residual stream
4. **Compares diversity** of baseline vs. SOE-perturbed reasoning trajectories
5. **Sweeps alpha** to show the mixing coefficient's effect

Uses simulated small neural network models (no GPU or API keys required).

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
bash run.sh
```

## Expected output

- **Phase 1**: Baseline teacher sampling showing low trajectory diversity (reasoning collapse)
- **Phase 2**: SOE-perturbed sampling showing higher diversity
- **Phase 3**: Spectral analysis of teacher's low-rank bias and student's orthogonal signal
- **Phase 4**: Side-by-side comparison table (diversity gain, similarity reduction)
- **Bonus**: Alpha sweep showing diversity vs. mixing coefficient

Key metrics to observe:
- Trajectory diversity increases with SOE
- Average pairwise cosine similarity decreases (more geometrically distinct samples)
- The alpha sweep shows a sweet spot around 0.2–0.5
