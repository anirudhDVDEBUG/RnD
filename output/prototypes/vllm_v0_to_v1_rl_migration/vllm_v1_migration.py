"""
vLLM V0 to V1 Migration Validator for RL Workloads

Validates configuration, simulates logprob correctness checks, and generates
the proper vLLM V1 config for reinforcement learning pipelines.
"""

import json
import math
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VLLMConfig:
    """vLLM configuration for RL workloads."""
    use_v1: bool = True
    logprobs_mode: str = "processed_logprobs"
    enable_prefix_caching: bool = False
    async_scheduling: bool = False
    fp32_lm_head: bool = True

    def to_dict(self) -> dict:
        return {
            "vllm_config": {
                "use_v1": self.use_v1,
                "vllm_kwargs": {
                    "logprobs-mode": self.logprobs_mode,
                    "enable-prefix-caching": self.enable_prefix_caching,
                    "async-scheduling": self.async_scheduling,
                }
            },
            "model_config": {
                "fp32_lm_head": self.fp32_lm_head,
            }
        }

    def to_yaml_str(self) -> str:
        d = self.to_dict()
        lines = ["# vLLM V1 RL Configuration"]
        lines.append("vllm_config:")
        lines.append(f"  use_v1: {str(d['vllm_config']['use_v1']).lower()}")
        lines.append("  vllm_kwargs:")
        for k, v in d['vllm_config']['vllm_kwargs'].items():
            lines.append(f"    {k}: {str(v).lower() if isinstance(v, bool) else v}")
        lines.append("")
        lines.append("model_config:")
        lines.append(f"  fp32_lm_head: {str(d['model_config']['fp32_lm_head']).lower()}")
        return "\n".join(lines)


@dataclass
class MigrationIssue:
    severity: str  # "critical", "warning", "info"
    component: str
    message: str
    fix: str


@dataclass
class DiagnosticMetrics:
    """Simulated diagnostic metrics for validating backend parity."""
    clip_rate: float = 0.0
    policy_ratio_mean: float = 1.0
    policy_ratio_std: float = 0.0
    kl_divergence: float = 0.0
    entropy: float = 0.0
    effective_lag: int = 0


def check_logprob_mode(config: dict) -> Optional[MigrationIssue]:
    """Check if logprobs mode is set to processed_logprobs."""
    vllm_kwargs = config.get("vllm_config", {}).get("vllm_kwargs", {})
    mode = vllm_kwargs.get("logprobs-mode", "raw")
    if mode != "processed_logprobs":
        return MigrationIssue(
            severity="critical",
            component="logprobs",
            message=f"logprobs-mode is '{mode}' — V1 returns raw logprobs by default. "
                    "RL requires post-temperature/penalty logprobs for policy ratio accuracy.",
            fix="Set logprobs-mode: processed_logprobs in vllm_kwargs"
        )
    return None


def check_prefix_caching(config: dict) -> Optional[MigrationIssue]:
    """Check if prefix caching is disabled."""
    vllm_kwargs = config.get("vllm_config", {}).get("vllm_kwargs", {})
    if vllm_kwargs.get("enable-prefix-caching", True):
        return MigrationIssue(
            severity="critical",
            component="prefix_caching",
            message="Prefix caching is enabled. After weight updates, cached KV states "
                    "are stale and produce incorrect logprobs.",
            fix="Set enable-prefix-caching: false"
        )
    return None


def check_async_scheduling(config: dict) -> Optional[MigrationIssue]:
    """Check if async scheduling is disabled."""
    vllm_kwargs = config.get("vllm_config", {}).get("vllm_kwargs", {})
    if vllm_kwargs.get("async-scheduling", True):
        return MigrationIssue(
            severity="warning",
            component="async_scheduling",
            message="Async scheduling is enabled. This changes request ordering "
                    "compared to V0's synchronous behavior.",
            fix="Set async-scheduling: false for deterministic V0-matching behavior"
        )
    return None


def check_fp32_lm_head(config: dict) -> Optional[MigrationIssue]:
    """Check if fp32 is used for lm_head projection."""
    model_config = config.get("model_config", {})
    if not model_config.get("fp32_lm_head", False):
        return MigrationIssue(
            severity="warning",
            component="precision",
            message="lm_head not using fp32. Small logit differences accumulate in "
                    "policy ratio and KL divergence calculations.",
            fix="Enable fp32_lm_head in model config (recommended by ScaleRL, MiniMax-M1)"
        )
    return None


def check_v1_enabled(config: dict) -> Optional[MigrationIssue]:
    """Check if V1 is actually enabled."""
    if not config.get("vllm_config", {}).get("use_v1", False):
        return MigrationIssue(
            severity="info",
            component="version",
            message="use_v1 is not set to true. Still running V0 engine.",
            fix="Set use_v1: true to enable V1 engine"
        )
    return None


ALL_CHECKS = [
    check_v1_enabled,
    check_logprob_mode,
    check_prefix_caching,
    check_async_scheduling,
    check_fp32_lm_head,
]


def validate_config(config: dict) -> list[MigrationIssue]:
    """Run all migration checks against a config."""
    issues = []
    for check in ALL_CHECKS:
        issue = check(config)
        if issue:
            issues.append(issue)
    return issues


def simulate_logprob_mismatch(use_processed: bool, fp32: bool) -> DiagnosticMetrics:
    """
    Simulate the effect of config choices on RL diagnostic metrics.

    With correct config (processed logprobs + fp32), metrics stay healthy.
    With incorrect config, policy ratio diverges and clip rate spikes.
    """
    random.seed(42)

    base_clip_rate = 0.02
    base_ratio_std = 0.01
    base_kl = 0.005
    base_entropy = 2.1

    if not use_processed:
        # Raw logprobs cause significant mismatch
        base_clip_rate += 0.15
        base_ratio_std += 0.08
        base_kl += 0.12

    if not fp32:
        # fp16 lm_head adds precision noise
        base_clip_rate += 0.03
        base_ratio_std += 0.02
        base_kl += 0.02

    noise = random.gauss(0, 0.005)

    return DiagnosticMetrics(
        clip_rate=round(base_clip_rate + abs(noise), 4),
        policy_ratio_mean=round(1.0 + (0.0 if use_processed else 0.12) + noise, 4),
        policy_ratio_std=round(base_ratio_std + abs(noise), 4),
        kl_divergence=round(base_kl + abs(noise), 4),
        entropy=round(base_entropy - (0.0 if use_processed else 0.3), 4),
        effective_lag=0 if use_processed else 2,
    )


def generate_weight_update_snippet() -> str:
    """Generate the correct weight update code for V1."""
    return '''# Correct V1 weight update pattern for RL
async def update_weights(engine, engine_client, request):
    """
    Pause generation, update weights, resume.
    mode="keep" preserves inflight requests.
    clear_cache=False maintains cached state.
    """
    await engine.pause_generation(mode="keep", clear_cache=False)
    await engine_client.collective_rpc_async(
        "receive_weight_update",
        args=(request.model_dump_json(),),
    )
    await engine.resume_generation()
'''


def run_full_validation(config: dict) -> dict:
    """Run validation and simulation, return full report."""
    issues = validate_config(config)

    vllm_kwargs = config.get("vllm_config", {}).get("vllm_kwargs", {})
    use_processed = vllm_kwargs.get("logprobs-mode") == "processed_logprobs"
    fp32 = config.get("model_config", {}).get("fp32_lm_head", False)

    metrics = simulate_logprob_mismatch(use_processed, fp32)

    return {
        "issues": issues,
        "metrics": metrics,
        "config_valid": len([i for i in issues if i.severity == "critical"]) == 0,
    }
