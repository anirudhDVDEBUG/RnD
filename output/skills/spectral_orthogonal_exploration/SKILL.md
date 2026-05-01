---
name: spectral_orthogonal_exploration
description: |
  Implement Spectral Orthogonal Exploration (SOE), a geometric inference framework that uses a weak "student" model to guide a stronger "teacher" model's reasoning by injecting orthogonal signals into the teacher's hidden-state subspace, mitigating reasoning collapse on hard math/logic/code tasks.
  TRIGGER when: user mentions "reasoning collapse", "weak-to-strong inference", "spectral orthogonal exploration", "SOE inference", "student guides teacher", "diverse reasoning trajectories", or wants to improve LLM sampling diversity on math/logic/code benchmarks.
---

# Spectral Orthogonal Exploration (SOE)

A geometric inference-time framework from the "Student Guides Teacher" paradigm. SOE steers a strong (teacher) LLM away from degenerate low-rank reasoning manifolds by using a weaker (student) model as an orthogonal probe, injecting semantically heterogeneous signals into the teacher's hidden-state orthogonal complement.

## When to use

- "My large model keeps generating the same wrong reasoning even with high temperature"
- "I want to implement weak-to-strong inference to improve math reasoning accuracy"
- "How do I use spectral methods to diversify LLM reasoning traces?"
- "Help me mitigate reasoning collapse when sampling from an LLM"
- "Implement SOE / Student Guides Teacher for code or logic benchmarks"

## Core Concepts

**Reasoning Collapse**: When stochastic sampling (e.g., temperature, top-k) produces only lexical variations of the same flawed reasoning rather than genuinely different solution paths. This is linked to a low-rank bias manifold in the model's hidden-state geometry.

**SOE Pipeline**:
1. **Extract hidden states** from the teacher model on a given prompt.
2. **Compute dominant subspace** via SVD/PCA of the teacher's hidden-state activations.
3. **Probe with student model** — run the weaker model on the same prompt to obtain its hidden states.
4. **Project into orthogonal complement** — project the student's hidden states onto the orthogonal complement of the teacher's dominant subspace.
5. **Inject orthogonal signal** — add the projected student signal back into the teacher's residual stream (scaled by a mixing coefficient) to steer generation toward unexplored reasoning directions.
6. **Decode** — let the teacher continue generation from the perturbed hidden states.

## How to use

### Step 1 — Set up model pair

Choose a strong teacher (e.g., Llama-3-70B, GPT-4-class) and a weaker student (e.g., Llama-3-8B, Phi-3-mini). Both must expose hidden-state activations (use HuggingFace `output_hidden_states=True` or equivalent).

### Step 2 — Extract teacher's dominant subspace

```python
import torch

def get_dominant_subspace(hidden_states, rank_k):
    """SVD on teacher hidden states to find dominant directions."""
    # hidden_states: (seq_len, hidden_dim)
    U, S, Vt = torch.linalg.svd(hidden_states, full_matrices=False)
    # Top-k right singular vectors span the dominant subspace
    V_k = Vt[:rank_k]  # (rank_k, hidden_dim)
    return V_k

def orthogonal_complement_projection(vector, V_k):
    """Project vector onto orthogonal complement of V_k's row span."""
    # Remove components along each dominant direction
    proj = vector.clone()
    for v in V_k:
        proj = proj - (proj @ v) * v
    return proj
```

### Step 3 — Generate student probe signal

Run the student model on the same prompt. Extract hidden states from a target layer (typically a middle-to-late layer).

```python
student_hidden = student_model(input_ids, output_hidden_states=True)
    .hidden_states[target_layer]  # (batch, seq_len, hidden_dim)
```

### Step 4 — Inject orthogonal signal into teacher

```python
def soe_intervene(teacher_hidden, student_hidden, rank_k, alpha=0.3):
    """Inject student's orthogonal component into teacher hidden states."""
    V_k = get_dominant_subspace(teacher_hidden.squeeze(0), rank_k)
    student_orth = orthogonal_complement_projection(
        student_hidden.squeeze(0), V_k
    )
    # Mix orthogonal student signal into teacher
    perturbed = teacher_hidden.squeeze(0) + alpha * student_orth
    return perturbed.unsqueeze(0)
```

### Step 5 — Decode with perturbed states

Replace the teacher's hidden states at the intervention layer with the perturbed states, then continue autoregressive decoding normally.

### Key hyperparameters

| Parameter | Description | Typical range |
|-----------|-------------|---------------|
| `rank_k` | Rank of teacher's dominant subspace to subtract | 5–30 |
| `alpha` | Mixing coefficient for orthogonal signal | 0.1–0.5 |
| `target_layer` | Layer index for intervention | Middle-to-late layers |
| `n_samples` | Number of diverse samples to generate | 8–64 |

### Step 6 — Aggregate and select

Generate multiple reasoning traces with SOE perturbation, then select the best via majority voting, reward-model scoring, or self-consistency.

## Expected gains

Per the paper's experiments on mathematical benchmarks:
- **+62.4% average accuracy** over baseline sampling methods
- **+113.7% average sampling efficiency** (fewer samples needed to find correct answer)
- Also effective on logic and code generation benchmarks

## References

- Paper: [Student Guides Teacher: Weak-to-Strong Inference via Spectral Orthogonal Exploration](https://arxiv.org/abs/2601.06160)
- arXiv ID: 2601.06160v2
- Domain: cs.AI — LLM reasoning, mathematical reasoning, spectral methods, inference strategies
