"""Style preset definitions for Seidr-Smidja avatar generation."""

PRESETS = {
    "anime": {
        "vertex_density": "medium",
        "eye_scale": 1.4,
        "head_ratio": 1.2,
        "shading": "cel",
        "default_hair": "long_straight",
        "default_eyes": "large_round",
        "default_outfit": "school_uniform",
        "spring_bones": 20,
        "palette": ["#FFB6C1", "#87CEEB", "#FFFFFF", "#333333"],
    },
    "cyberpunk": {
        "vertex_density": "high",
        "eye_scale": 1.1,
        "head_ratio": 1.0,
        "shading": "pbr_toon",
        "default_hair": "spiky_long",
        "default_eyes": "narrow_glowing",
        "default_outfit": "jacket_techwear",
        "spring_bones": 24,
        "palette": ["#FF00FF", "#00FFFF", "#1A1A2E", "#0F0F0F"],
    },
    "fantasy": {
        "vertex_density": "high",
        "eye_scale": 1.3,
        "head_ratio": 1.1,
        "shading": "cel_detailed",
        "default_hair": "flowing_long",
        "default_eyes": "elven",
        "default_outfit": "robe_ornate",
        "spring_bones": 28,
        "palette": ["#FFD700", "#4B0082", "#228B22", "#F5F5DC"],
    },
    "casual": {
        "vertex_density": "medium",
        "eye_scale": 1.2,
        "head_ratio": 1.1,
        "shading": "cel",
        "default_hair": "short_messy",
        "default_eyes": "relaxed",
        "default_outfit": "hoodie_jeans",
        "spring_bones": 16,
        "palette": ["#4A90D9", "#F5A623", "#FFFFFF", "#2C2C2C"],
    },
}


def resolve_style(style_name, hair=None, eyes=None, outfit=None, accessories=None):
    """Resolve a style preset with optional overrides."""
    base = PRESETS.get(style_name, PRESETS["anime"]).copy()

    config = {
        "style": style_name,
        "vertex_density": base["vertex_density"],
        "eye_scale": base["eye_scale"],
        "head_ratio": base["head_ratio"],
        "shading": base["shading"],
        "spring_bones": base["spring_bones"],
        "palette": base["palette"],
        "hair": hair or base["default_hair"],
        "eyes": eyes or base["default_eyes"],
        "outfit": outfit or base["default_outfit"],
        "accessories": accessories or [],
    }

    # Adjust spring bones for accessories
    if accessories:
        config["spring_bones"] += len(accessories) * 2

    return config
