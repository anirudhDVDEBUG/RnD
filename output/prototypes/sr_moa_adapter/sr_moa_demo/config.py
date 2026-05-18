from dataclasses import dataclass, field
from typing import List


@dataclass
class SRMoAConfig:
    num_adapters: int = 4
    lora_rank: int = 16
    lora_alpha: int = 32
    reflection_steps: int = 3
    router_hidden_dim: int = 256
    hidden_dim: int = 768  # base model hidden size
    target_modules: List[str] = field(default_factory=lambda: ["q_proj", "v_proj"])
    router_type: str = "self_reflective"
    top_k: int = 2
    adapter_names: List[str] = field(
        default_factory=lambda: ["reasoning", "creative", "code", "factual"]
    )
