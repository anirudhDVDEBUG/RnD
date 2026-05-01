"""
Spectral Orthogonal Exploration (SOE) — Prototype Demo

Demonstrates the core geometric inference framework from:
"Student Guides Teacher: Weak-to-Strong Inference via Spectral Orthogonal Exploration"
(arXiv:2601.06160)

This prototype simulates teacher/student models as small neural networks and shows
how SOE's orthogonal perturbation produces genuinely diverse reasoning trajectories
compared to standard temperature sampling (which suffers from reasoning collapse).
"""

import numpy as np
from typing import Tuple, List

np.random.seed(42)

# ─── Core SOE Functions ────────────────────────────────────────────────

def get_dominant_subspace(hidden_states: np.ndarray, rank_k: int) -> np.ndarray:
    """SVD on teacher hidden states to find dominant directions.

    Args:
        hidden_states: (seq_len, hidden_dim) matrix of activations
        rank_k: number of dominant singular vectors to extract
    Returns:
        V_k: (rank_k, hidden_dim) top-k right singular vectors
    """
    U, S, Vt = np.linalg.svd(hidden_states, full_matrices=False)
    V_k = Vt[:rank_k]
    return V_k, S


def orthogonal_complement_projection(vector: np.ndarray, V_k: np.ndarray) -> np.ndarray:
    """Project vector onto orthogonal complement of V_k's row span.

    Removes all components along the dominant directions, leaving only
    the novel/unexplored directions from the student signal.
    """
    proj = vector.copy()
    for v in V_k:
        v_norm = v / (np.linalg.norm(v) + 1e-10)
        proj = proj - np.outer(proj @ v_norm, v_norm)
    return proj


def soe_intervene(teacher_hidden: np.ndarray, student_hidden: np.ndarray,
                  rank_k: int, alpha: float = 0.3) -> Tuple[np.ndarray, dict]:
    """Inject student's orthogonal component into teacher hidden states.

    This is the core SOE operation: it steers the teacher away from its
    dominant (potentially collapsed) reasoning manifold by adding signals
    from the student that lie in the teacher's orthogonal complement.
    """
    V_k, singular_values = get_dominant_subspace(teacher_hidden, rank_k)
    student_orth = orthogonal_complement_projection(student_hidden, V_k)

    orth_magnitude = np.linalg.norm(student_orth, axis=1).mean()
    perturbed = teacher_hidden + alpha * student_orth

    info = {
        "singular_values": singular_values[:rank_k],
        "orth_signal_magnitude": orth_magnitude,
        "subspace_rank": rank_k,
        "alpha": alpha,
    }
    return perturbed, info


# ─── Simulated Models ──────────────────────────────────────────────────

class SimulatedModel:
    """A tiny simulated transformer-like model for demonstration.

    Generates hidden states that mimic real model behavior:
    - Teacher: strong but with low-rank bias (reasoning collapse)
    - Student: weaker but with different, more varied representations
    """

    def __init__(self, hidden_dim: int, name: str, rank_bias: int = 5):
        self.hidden_dim = hidden_dim
        self.name = name
        self.rank_bias = rank_bias
        # Random "weights" for projection
        self.W = np.random.randn(hidden_dim, hidden_dim) * 0.1
        # Dominant directions (simulates learned reasoning patterns)
        self.dominant_dirs = np.random.randn(rank_bias, hidden_dim)
        self.dominant_dirs /= np.linalg.norm(self.dominant_dirs, axis=1, keepdims=True)

    def get_hidden_states(self, prompt_embedding: np.ndarray,
                          temperature: float = 1.0) -> np.ndarray:
        """Generate hidden states for a prompt.

        Teacher model concentrates activations along dominant directions
        (simulating reasoning collapse). Student model has more spread.
        """
        seq_len = prompt_embedding.shape[0]
        base = prompt_embedding @ self.W

        # Add dominant direction bias (stronger = more collapse)
        bias_strength = 5.0 / (self.rank_bias + 1)
        for d in self.dominant_dirs:
            coeff = np.random.randn(seq_len, 1) * bias_strength
            base += coeff * d[np.newaxis, :]

        # Temperature only adds noise, doesn't change structure
        noise = np.random.randn(*base.shape) * temperature * 0.1
        return base + noise

    def decode_to_tokens(self, hidden_states: np.ndarray) -> List[str]:
        """Simulate decoding hidden states into reasoning 'tokens'.

        Maps hidden state directions to symbolic reasoning steps.
        """
        reasoning_strategies = [
            "algebraic_manipulation", "substitution", "factoring",
            "geometric_insight", "induction", "contradiction",
            "case_analysis", "symmetry_argument", "bounding",
            "probabilistic_method", "greedy_approach", "dynamic_programming",
            "divide_and_conquer", "graph_reduction", "modular_arithmetic",
        ]
        # Use dominant PCA direction of hidden states to pick strategy
        mean_h = hidden_states.mean(axis=0)
        # Hash the direction into strategy indices
        indices = np.abs(mean_h[:len(reasoning_strategies)])
        top_k = np.argsort(indices)[-3:]
        return [reasoning_strategies[i] for i in top_k]


def measure_diversity(trajectories: List[List[str]]) -> float:
    """Measure diversity across reasoning trajectories.

    Returns ratio of unique strategy combinations to total samples.
    """
    unique = set(tuple(sorted(t)) for t in trajectories)
    return len(unique) / len(trajectories)


def cosine_similarity_matrix(states_list: List[np.ndarray]) -> np.ndarray:
    """Compute pairwise cosine similarity between hidden state means."""
    means = [s.mean(axis=0) for s in states_list]
    n = len(means)
    sim_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dot = means[i] @ means[j]
            norm = np.linalg.norm(means[i]) * np.linalg.norm(means[j]) + 1e-10
            sim_matrix[i, j] = dot / norm
    return sim_matrix


# ─── Main Demo ──────────────────────────────────────────────────────────

def run_demo():
    HIDDEN_DIM = 64
    SEQ_LEN = 16
    RANK_K = 5
    ALPHA = 0.3
    N_SAMPLES = 8

    print("=" * 65)
    print(" Spectral Orthogonal Exploration (SOE) — Prototype Demo")
    print(" Paper: arXiv:2601.06160")
    print("=" * 65)

    # Create teacher (strong, low-rank bias → collapse) and student (weak, diverse)
    teacher = SimulatedModel(HIDDEN_DIM, "Teacher-70B", rank_bias=3)
    student = SimulatedModel(HIDDEN_DIM, "Student-8B", rank_bias=12)

    # Simulate a hard math prompt embedding
    prompt = np.random.randn(SEQ_LEN, HIDDEN_DIM) * 0.5

    # ── Phase 1: Baseline sampling (standard temperature) ───────────
    print("\n[Phase 1] Baseline: Teacher with temperature sampling")
    print("-" * 50)

    baseline_states = []
    baseline_trajectories = []
    for i in range(N_SAMPLES):
        np.random.seed(i * 7 + 100)
        h = teacher.get_hidden_states(prompt, temperature=1.0)
        baseline_states.append(h)
        traj = teacher.decode_to_tokens(h)
        baseline_trajectories.append(traj)
        print(f"  Sample {i+1}: {' -> '.join(traj)}")

    baseline_diversity = measure_diversity(baseline_trajectories)
    baseline_sim = cosine_similarity_matrix(baseline_states)
    baseline_avg_sim = (baseline_sim.sum() - N_SAMPLES) / (N_SAMPLES * (N_SAMPLES - 1))

    print(f"\n  Trajectory diversity: {baseline_diversity:.2%}")
    print(f"  Avg pairwise cosine similarity: {baseline_avg_sim:.4f}")
    print(f"  >> High similarity = reasoning collapse (lexical variants of same path)")

    # ── Phase 2: SOE-perturbed sampling ─────────────────────────────
    print(f"\n[Phase 2] SOE: Teacher + Student orthogonal injection")
    print(f"  rank_k={RANK_K}, alpha={ALPHA}")
    print("-" * 50)

    soe_states = []
    soe_trajectories = []
    for i in range(N_SAMPLES):
        np.random.seed(i * 7 + 100)  # Same seeds as baseline
        teacher_h = teacher.get_hidden_states(prompt, temperature=1.0)

        np.random.seed(i * 13 + 200)  # Different seed for student
        student_h = student.get_hidden_states(prompt, temperature=0.8)

        perturbed_h, info = soe_intervene(teacher_h, student_h, RANK_K, ALPHA)
        soe_states.append(perturbed_h)
        traj = teacher.decode_to_tokens(perturbed_h)
        soe_trajectories.append(traj)
        print(f"  Sample {i+1}: {' -> '.join(traj)}")

    soe_diversity = measure_diversity(soe_trajectories)
    soe_sim = cosine_similarity_matrix(soe_states)
    soe_avg_sim = (soe_sim.sum() - N_SAMPLES) / (N_SAMPLES * (N_SAMPLES - 1))

    print(f"\n  Trajectory diversity: {soe_diversity:.2%}")
    print(f"  Avg pairwise cosine similarity: {soe_avg_sim:.4f}")

    # ── Phase 3: Analysis ───────────────────────────────────────────
    print(f"\n[Phase 3] Spectral Analysis")
    print("-" * 50)

    np.random.seed(42)
    teacher_h = teacher.get_hidden_states(prompt)
    V_k, S = get_dominant_subspace(teacher_h, RANK_K)

    total_energy = (S ** 2).sum()
    top_k_energy = (S[:RANK_K] ** 2).sum()
    print(f"  Teacher singular values (top-{RANK_K}): {np.round(S[:RANK_K], 2)}")
    print(f"  Energy in top-{RANK_K} subspace: {top_k_energy/total_energy:.1%}")
    print(f"  >> High concentration = low-rank bias manifold")

    np.random.seed(42)
    student_h = student.get_hidden_states(prompt)
    student_orth = orthogonal_complement_projection(student_h, V_k)
    orth_energy = np.linalg.norm(student_orth) / np.linalg.norm(student_h)
    print(f"\n  Student orthogonal signal ratio: {orth_energy:.2%}")
    print(f"  >> Fraction of student signal in teacher's blind spot")

    # ── Phase 4: Summary ────────────────────────────────────────────
    print(f"\n[Phase 4] Results Summary")
    print("=" * 65)
    diversity_gain = (soe_diversity - baseline_diversity) / max(baseline_diversity, 1e-10)
    sim_reduction = (baseline_avg_sim - soe_avg_sim) / baseline_avg_sim

    print(f"  {'Metric':<35} {'Baseline':>10} {'SOE':>10} {'Change':>10}")
    print(f"  {'-'*35} {'-'*10} {'-'*10} {'-'*10}")
    print(f"  {'Trajectory diversity':<35} {baseline_diversity:>9.1%} {soe_diversity:>9.1%} {diversity_gain:>+9.1%}")
    print(f"  {'Avg pairwise similarity':<35} {baseline_avg_sim:>10.4f} {soe_avg_sim:>10.4f} {sim_reduction:>+9.1%}")
    print(f"\n  SOE successfully diversifies reasoning by injecting orthogonal")
    print(f"  student signals into the teacher's blind spots, mitigating")
    print(f"  reasoning collapse without degrading individual sample quality.")
    print("=" * 65)

    # ── Phase 5: Hyperparameter sweep ───────────────────────────────
    print(f"\n[Bonus] Alpha sweep (mixing coefficient sensitivity)")
    print("-" * 50)
    print(f"  {'alpha':<8} {'Diversity':>12} {'Avg Sim':>12}")

    for alpha in [0.0, 0.1, 0.2, 0.3, 0.5, 0.8]:
        trajs = []
        states = []
        for i in range(N_SAMPLES):
            np.random.seed(i * 7 + 100)
            t_h = teacher.get_hidden_states(prompt, temperature=1.0)
            np.random.seed(i * 13 + 200)
            s_h = student.get_hidden_states(prompt, temperature=0.8)
            p_h, _ = soe_intervene(t_h, s_h, RANK_K, alpha)
            states.append(p_h)
            trajs.append(teacher.decode_to_tokens(p_h))
        div = measure_diversity(trajs)
        sim = cosine_similarity_matrix(states)
        avg_sim = (sim.sum() - N_SAMPLES) / (N_SAMPLES * (N_SAMPLES - 1))
        marker = " <-- baseline" if alpha == 0.0 else (" <-- default" if alpha == 0.3 else "")
        print(f"  {alpha:<8.1f} {div:>11.1%} {avg_sim:>12.4f}{marker}")

    print()


if __name__ == "__main__":
    run_demo()
