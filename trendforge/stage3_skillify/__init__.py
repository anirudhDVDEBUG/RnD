"""Stage 3: skillify — generate Claude skill folders for selected items."""
from .skill_generator import generate_skill_for_item, skillify_watched, slugify

__all__ = ["generate_skill_for_item", "skillify_watched", "slugify"]
