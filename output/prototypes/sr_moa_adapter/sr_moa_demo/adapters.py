import torch
import torch.nn as nn


class LoRAAdapter(nn.Module):
    """Lightweight LoRA-style adapter: down-project then up-project."""

    def __init__(self, hidden_dim: int, rank: int, alpha: int):
        super().__init__()
        self.scaling = alpha / rank
        self.down = nn.Linear(hidden_dim, rank, bias=False)
        self.up = nn.Linear(rank, hidden_dim, bias=False)
        # Initialize down with small random, up with zeros (standard LoRA init)
        nn.init.kaiming_uniform_(self.down.weight)
        nn.init.zeros_(self.up.weight)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.up(self.down(x)) * self.scaling


class LoRAAdapterPool(nn.Module):
    """Pool of LoRA adapters that can be composed via weighted sum."""

    def __init__(self, num_adapters: int, hidden_dim: int, rank: int, alpha: int):
        super().__init__()
        self.adapters = nn.ModuleList([
            LoRAAdapter(hidden_dim, rank, alpha) for _ in range(num_adapters)
        ])

    def forward(self, x: torch.Tensor, weights: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, hidden_dim) input hidden states
            weights: (batch, num_adapters) adapter composition weights
        Returns:
            (batch, seq_len, hidden_dim) weighted sum of adapter outputs
        """
        adapter_outputs = torch.stack([adapter(x) for adapter in self.adapters], dim=1)
        # adapter_outputs: (batch, num_adapters, seq_len, hidden_dim)
        # weights: (batch, num_adapters) -> (batch, num_adapters, 1, 1)
        w = weights.unsqueeze(-1).unsqueeze(-1)
        composed = (adapter_outputs * w).sum(dim=1)  # (batch, seq_len, hidden_dim)
        return composed
