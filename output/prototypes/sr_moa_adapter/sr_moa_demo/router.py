import torch
import torch.nn as nn
import torch.nn.functional as F


class SelfReflectiveRouter(nn.Module):
    """Routes inputs to adapters with iterative self-reflection."""

    def __init__(self, hidden_dim: int, num_adapters: int, router_hidden_dim: int = 256):
        super().__init__()
        self.num_adapters = num_adapters

        # Initial routing network
        self.initial_router = nn.Sequential(
            nn.Linear(hidden_dim, router_hidden_dim),
            nn.GELU(),
            nn.Linear(router_hidden_dim, num_adapters),
        )

        # Reflection network: takes hidden state + previous scores + adapter outputs
        self.reflection_net = nn.Sequential(
            nn.Linear(hidden_dim + num_adapters, router_hidden_dim),
            nn.GELU(),
            nn.Linear(router_hidden_dim, num_adapters),
        )

    def initial_route(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """Produce initial adapter scores from hidden states."""
        # Pool over sequence length
        pooled = hidden_states.mean(dim=1)  # (batch, hidden_dim)
        logits = self.initial_router(pooled)  # (batch, num_adapters)
        return F.softmax(logits, dim=-1)

    def reflect(self, hidden_states: torch.Tensor, prev_scores: torch.Tensor) -> torch.Tensor:
        """Refine routing scores given previous scores and hidden states."""
        pooled = hidden_states.mean(dim=1)  # (batch, hidden_dim)
        combined = torch.cat([pooled, prev_scores], dim=-1)
        logits = self.reflection_net(combined)
        # Residual connection with previous scores for stability
        refined = F.softmax(logits, dim=-1) * 0.7 + prev_scores * 0.3
        return refined / refined.sum(dim=-1, keepdim=True)
