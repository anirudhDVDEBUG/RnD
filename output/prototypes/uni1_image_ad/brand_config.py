"""Parse and validate brand configuration for ad generation."""

import yaml
from dataclasses import dataclass, field
from typing import List, Optional

ASPECT_RATIOS = {
    "facebook_feed": "1:1",
    "instagram_feed": "1:1",
    "instagram_stories": "9:16",
    "instagram_reels": "9:16",
    "facebook_link": "1.91:1",
    "facebook_stories": "9:16",
}


@dataclass
class BrandConfig:
    brand_name: str
    product: str
    tone: str = "modern"
    cta_text: str = "Learn More"
    color_palette: List[str] = field(default_factory=list)
    target_platform: str = "instagram_feed"

    @property
    def aspect_ratio(self) -> str:
        return ASPECT_RATIOS.get(self.target_platform, "1:1")

    @classmethod
    def from_yaml(cls, path: str) -> "BrandConfig":
        with open(path) as f:
            data = yaml.safe_load(f)
        return cls(**data)

    @classmethod
    def from_args(cls, brand_name: str, product: str, tone: str = "modern",
                  cta_text: str = "Learn More", ratio: Optional[str] = None,
                  platform: str = "instagram_feed") -> "BrandConfig":
        config = cls(
            brand_name=brand_name,
            product=product,
            tone=tone,
            cta_text=cta_text,
            target_platform=platform,
        )
        return config
