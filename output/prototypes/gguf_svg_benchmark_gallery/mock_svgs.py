"""Generate procedural mock SVG pelicans with controlled variation per quantization level."""

import random
import math

QUANTIZATIONS = [
    ("Q2_K", 1.2),
    ("Q4_K_M", 2.1),
    ("Q5_K_M", 2.6),
    ("Q6_K", 3.1),
    ("Q8_0", 3.8),
    ("IQ4_NL", 2.0),
    ("F16", 5.8),
    ("BF16", 5.8),
]


def generate_pelican_svg(quant_name: str, seed: int) -> str:
    """Generate a unique pelican SVG based on quantization name as seed."""
    rng = random.Random(seed)

    # Body ellipse params
    cx, cy = 150 + rng.randint(-10, 10), 200 + rng.randint(-5, 5)
    rx, ry = 60 + rng.randint(-8, 8), 45 + rng.randint(-5, 5)

    # Head
    hx, hy = cx - 40 + rng.randint(-5, 5), cy - 70 + rng.randint(-10, 10)
    hr = 20 + rng.randint(-3, 3)

    # Beak (pouch)
    beak_len = 35 + rng.randint(-5, 15)
    pouch_depth = 12 + rng.randint(0, 8)

    # Bicycle wheels
    wheel_r = 25 + rng.randint(-3, 3)
    w1x, w1y = cx - 50, cy + 80
    w2x, w2y = cx + 50, cy + 80

    # Colors vary by "quantization quality"
    body_colors = ["#f5f5dc", "#fff8dc", "#faebd7", "#ffe4c4", "#ffdab9", "#ffe4b5", "#ffefd5", "#fff5ee"]
    beak_colors = ["#ff8c00", "#ffa500", "#ff7f50", "#ff6347", "#e8860c", "#d2691e", "#cd853f", "#daa520"]
    idx = hash(quant_name) % len(body_colors)
    body_color = body_colors[idx]
    beak_color = beak_colors[idx]

    # Number of spokes varies (simulating detail level)
    num_spokes = rng.choice([4, 6, 8, 12])

    spokes1 = ""
    spokes2 = ""
    for i in range(num_spokes):
        angle = (2 * math.pi * i) / num_spokes
        dx = wheel_r * math.cos(angle)
        dy = wheel_r * math.sin(angle)
        spokes1 += f'<line x1="{w1x}" y1="{w1y}" x2="{w1x+dx:.1f}" y2="{w1y+dy:.1f}" stroke="#555" stroke-width="1"/>\n'
        spokes2 += f'<line x1="{w2x}" y1="{w2y}" x2="{w2x+dx:.1f}" y2="{w2y+dy:.1f}" stroke="#555" stroke-width="1"/>\n'

    # Optional extras based on quant
    extras = ""
    if rng.random() > 0.4:
        # Add wing detail
        wing_pts = f"{cx-20},{cy-10} {cx-50},{cy-30} {cx-30},{cy+10}"
        extras += f'<polygon points="{wing_pts}" fill="#ddd" stroke="#999" stroke-width="1"/>\n'
    if rng.random() > 0.5:
        # Add eye
        extras += f'<circle cx="{hx+5}" cy="{hy-3}" r="3" fill="#333"/>\n'
        extras += f'<circle cx="{hx+5}" cy="{hy-3}" r="1" fill="white"/>\n'

    # Frame connecting wheels
    frame_color = rng.choice(["#333", "#444", "#555", "#222"])

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 320" width="300" height="320">
  <rect width="300" height="320" fill="#e8f4f8"/>
  <!-- Bicycle frame -->
  <line x1="{w1x}" y1="{w1y}" x2="{cx}" y2="{cy+30}" stroke="{frame_color}" stroke-width="3"/>
  <line x1="{w2x}" y1="{w2y}" x2="{cx}" y2="{cy+30}" stroke="{frame_color}" stroke-width="3"/>
  <line x1="{cx}" y1="{cy+30}" x2="{cx+10}" y2="{cy+10}" stroke="{frame_color}" stroke-width="2"/>
  <!-- Wheels -->
  <circle cx="{w1x}" cy="{w1y}" r="{wheel_r}" fill="none" stroke="#333" stroke-width="2.5"/>
  <circle cx="{w2x}" cy="{w2y}" r="{wheel_r}" fill="none" stroke="#333" stroke-width="2.5"/>
  {spokes1}
  {spokes2}
  <!-- Pelican body -->
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{body_color}" stroke="#999" stroke-width="1.5"/>
  <!-- Neck -->
  <path d="M {cx-20},{cy-30} Q {cx-35},{cy-55} {hx},{hy+hr}" fill="none" stroke="{body_color}" stroke-width="12"/>
  <path d="M {cx-20},{cy-30} Q {cx-35},{cy-55} {hx},{hy+hr}" fill="none" stroke="#999" stroke-width="1"/>
  <!-- Head -->
  <circle cx="{hx}" cy="{hy}" r="{hr}" fill="{body_color}" stroke="#999" stroke-width="1.5"/>
  <!-- Beak with pouch -->
  <path d="M {hx+hr-2},{hy+2} L {hx+hr+beak_len},{hy-2} L {hx+hr+beak_len},{hy+4}
           Q {hx+hr+beak_len//2},{hy+4+pouch_depth} {hx+hr-2},{hy+5} Z"
        fill="{beak_color}" stroke="#b8600a" stroke-width="1"/>
  {extras}
  <!-- Label -->
  <text x="150" y="310" text-anchor="middle" font-family="monospace" font-size="11" fill="#666">{quant_name}</text>
</svg>'''
    return svg


def generate_all(model_base: str = "granite-4.1-3b") -> dict:
    """Generate SVGs for all quantization levels. Returns {filename: svg_content}."""
    results = {}
    for quant_name, _size_gb in QUANTIZATIONS:
        seed = hash(f"{model_base}-{quant_name}") & 0xFFFFFFFF
        filename = f"{model_base}-{quant_name}.svg"
        results[filename] = generate_pelican_svg(quant_name, seed)
    return results


if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)
    for filename, svg in generate_all().items():
        path = os.path.join("output", filename)
        with open(path, "w") as f:
            f.write(svg)
        print(f"[*] Created output/{filename} ({len(svg)} bytes)")
