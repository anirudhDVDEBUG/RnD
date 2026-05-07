#!/usr/bin/env python3
"""
Demo: vLLM V0 to V1 Migration Validator for RL Workloads

Shows how misconfigured vLLM V1 causes logprob mismatch in RL,
and how the correct configuration fixes it.
"""

from vllm_v1_migration import (
    VLLMConfig,
    validate_config,
    simulate_logprob_mismatch,
    generate_weight_update_snippet,
    run_full_validation,
)


def print_header(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def print_issues(issues):
    if not issues:
        print("  No issues found!")
        return
    for issue in issues:
        icon = {"critical": "[CRITICAL]", "warning": "[WARNING]", "info": "[INFO]"}
        print(f"  {icon[issue.severity]} [{issue.component}]")
        print(f"    Problem: {issue.message}")
        print(f"    Fix:     {issue.fix}")
        print()


def print_metrics(metrics, label: str):
    print(f"  --- {label} ---")
    print(f"  Clip rate:           {metrics.clip_rate:.4f}  {'(OK)' if metrics.clip_rate < 0.05 else '(HIGH!)'}")
    print(f"  Policy ratio mean:   {metrics.policy_ratio_mean:.4f}  {'(OK)' if abs(metrics.policy_ratio_mean - 1.0) < 0.02 else '(DIVERGED!)'}")
    print(f"  Policy ratio std:    {metrics.policy_ratio_std:.4f}  {'(OK)' if metrics.policy_ratio_std < 0.03 else '(HIGH!)'}")
    print(f"  KL divergence:       {metrics.kl_divergence:.4f}  {'(OK)' if metrics.kl_divergence < 0.02 else '(HIGH!)'}")
    print(f"  Entropy:             {metrics.entropy:.4f}")
    print(f"  Effective lag:       {metrics.effective_lag} steps")
    print()


def main():
    # =========================================================
    # Scenario 1: Naive V1 migration (default V1 settings)
    # =========================================================
    print_header("Scenario 1: Naive V1 Migration (V1 defaults)")

    naive_config = {
        "vllm_config": {
            "use_v1": True,
            "vllm_kwargs": {
                "logprobs-mode": "raw",           # V1 default - WRONG for RL
                "enable-prefix-caching": True,     # V1 default - WRONG for RL
                "async-scheduling": True,          # V1 default - WRONG for RL
            }
        },
        "model_config": {
            "fp32_lm_head": False,                 # Not set - loses precision
        }
    }

    print("Config: Using V1 defaults (raw logprobs, prefix caching ON, async ON)")
    print()

    result = run_full_validation(naive_config)

    print("Issues detected:")
    print_issues(result["issues"])

    metrics_bad = simulate_logprob_mismatch(use_processed=False, fp32=False)
    print_metrics(metrics_bad, "Simulated RL Metrics (BROKEN)")

    print(f"  Config valid for RL: {'YES' if result['config_valid'] else 'NO'}")

    # =========================================================
    # Scenario 2: Correct V1 migration for RL
    # =========================================================
    print_header("Scenario 2: Correct V1 Migration for RL")

    correct = VLLMConfig()
    correct_config = correct.to_dict()

    print("Generated YAML config:")
    print()
    for line in correct.to_yaml_str().split("\n"):
        print(f"  {line}")
    print()

    result = run_full_validation(correct_config)

    print("Issues detected:")
    print_issues(result["issues"])

    metrics_good = simulate_logprob_mismatch(use_processed=True, fp32=True)
    print_metrics(metrics_good, "Simulated RL Metrics (CORRECT)")

    print(f"  Config valid for RL: {'YES' if result['config_valid'] else 'NO'}")

    # =========================================================
    # Comparison
    # =========================================================
    print_header("Side-by-Side Comparison")

    print(f"  {'Metric':<22} {'Naive V1':<14} {'Correct V1':<14} {'Status'}")
    print(f"  {'-'*22} {'-'*14} {'-'*14} {'-'*10}")
    print(f"  {'Clip rate':<22} {metrics_bad.clip_rate:<14.4f} {metrics_good.clip_rate:<14.4f} {'FIXED' if metrics_good.clip_rate < 0.05 else 'ISSUE'}")
    print(f"  {'Policy ratio mean':<22} {metrics_bad.policy_ratio_mean:<14.4f} {metrics_good.policy_ratio_mean:<14.4f} {'FIXED' if abs(metrics_good.policy_ratio_mean - 1.0) < 0.02 else 'ISSUE'}")
    print(f"  {'Policy ratio std':<22} {metrics_bad.policy_ratio_std:<14.4f} {metrics_good.policy_ratio_std:<14.4f} {'FIXED' if metrics_good.policy_ratio_std < 0.03 else 'ISSUE'}")
    print(f"  {'KL divergence':<22} {metrics_bad.kl_divergence:<14.4f} {metrics_good.kl_divergence:<14.4f} {'FIXED' if metrics_good.kl_divergence < 0.02 else 'ISSUE'}")
    print(f"  {'Effective lag':<22} {metrics_bad.effective_lag:<14} {metrics_good.effective_lag:<14} {'FIXED' if metrics_good.effective_lag == 0 else 'ISSUE'}")
    print()

    # =========================================================
    # Weight Update Pattern
    # =========================================================
    print_header("V1 Weight Update Pattern")
    print(generate_weight_update_snippet())

    # =========================================================
    # Key Takeaway
    # =========================================================
    print_header("Key Methodology")
    print("  1. Fix BACKEND CORRECTNESS first (inference parity)")
    print("     - logprobs-mode: processed_logprobs")
    print("     - enable-prefix-caching: false")
    print("     - async-scheduling: false")
    print("     - fp32 lm_head projection")
    print()
    print("  2. Only THEN apply objective-side corrections")
    print("     - Off-policy adjustments")
    print("     - Async training compensations")
    print()
    print("  Applying corrections before fixing parity MASKS inference bugs.")
    print()


if __name__ == "__main__":
    main()
