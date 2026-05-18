import torch
import torch.nn as nn
from .config import SRMoAConfig
from .router import SelfReflectiveRouter
from .adapters import LoRAAdapterPool


class SRMoAModel(nn.Module):
    """
    Self-Reflective Mixture of Adapters model.
    Wraps a frozen base representation and adds dynamic adapter composition.
    """

    def __init__(self, config: SRMoAConfig):
        super().__init__()
        self.config = config

        # Simulated frozen base model (linear projection as stand-in)
        self.base_model = nn.Linear(config.hidden_dim, config.hidden_dim, bias=False)
        # Freeze it
        for p in self.base_model.parameters():
            p.requires_grad = False

        self.router = SelfReflectiveRouter(
            hidden_dim=config.hidden_dim,
            num_adapters=config.num_adapters,
            router_hidden_dim=config.router_hidden_dim,
        )

        self.adapter_pool = LoRAAdapterPool(
            num_adapters=config.num_adapters,
            hidden_dim=config.hidden_dim,
            rank=config.lora_rank,
            alpha=config.lora_alpha,
        )

    def forward(self, x: torch.Tensor, verbose: bool = False):
        """
        Args:
            x: (batch, seq_len, hidden_dim) input embeddings
            verbose: if True, return intermediate routing info
        Returns:
            output tensor and optionally routing history
        """
        # Base model forward (frozen)
        base_output = self.base_model(x)

        # Initial routing
        scores = self.router.initial_route(base_output)
        history = [scores.detach().clone()]

        # Self-reflective loop
        current_hidden = base_output
        for step in range(self.config.reflection_steps):
            # Compose adapters with current scores
            adapter_delta = self.adapter_pool(current_hidden, scores)
            current_hidden = base_output + adapter_delta

            # Reflect and refine scores
            scores = self.router.reflect(current_hidden, scores)
            history.append(scores.detach().clone())

        # Final composition
        final_delta = self.adapter_pool(base_output, scores)
        output = base_output + final_delta

        if verbose:
            return output, history
        return output
