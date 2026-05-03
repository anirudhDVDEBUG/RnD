"""
Claude Design Agents Toolkit — core design agents.

Provides four specialized agents:
  1. LayoutAgent      — generates semantic HTML + Tailwind layouts
  2. ColorAgent       — creates color palettes and design tokens
  3. ComponentAgent   — turns descriptions into component specs
  4. DesignToCodeAgent — translates a design spec into ready-to-use code

All agents work offline (no API keys) using template-based generation.
"""

from __future__ import annotations

import json
import colorsys
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ── Colour helpers ──────────────────────────────────────────────────────────

def _hex_to_hsl(hex_color: str):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100


def _hsl_to_hex(h: float, s: float, l: float) -> str:
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


def generate_palette(base_hex: str = "#3b82f6", name: str = "primary") -> Dict:
    """Generate a 10-shade palette from a base colour (50–950)."""
    h, s, l = _hex_to_hsl(base_hex)
    shades = {}
    targets = [
        ("50", 96), ("100", 90), ("200", 80), ("300", 70), ("400", 60),
        ("500", 50), ("600", 40), ("700", 30), ("800", 20), ("900", 14), ("950", 8),
    ]
    for label, lightness in targets:
        shades[label] = _hsl_to_hex(h, s, lightness)
    return {name: shades}


# ── Design token system ────────────────────────────────────────────────────

DEFAULT_SPACING = {"xs": "0.25rem", "sm": "0.5rem", "md": "1rem", "lg": "1.5rem", "xl": "2rem", "2xl": "3rem"}
DEFAULT_FONT_SIZES = {"xs": "0.75rem", "sm": "0.875rem", "base": "1rem", "lg": "1.125rem", "xl": "1.25rem", "2xl": "1.5rem", "3xl": "1.875rem", "4xl": "2.25rem"}
DEFAULT_RADII = {"none": "0", "sm": "0.125rem", "md": "0.375rem", "lg": "0.5rem", "xl": "0.75rem", "full": "9999px"}


@dataclass
class DesignTokens:
    colors: Dict[str, Dict[str, str]] = field(default_factory=dict)
    spacing: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_SPACING))
    font_sizes: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_FONT_SIZES))
    border_radius: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_RADII))

    def to_css_vars(self) -> str:
        lines = [":root {"]
        for palette_name, shades in self.colors.items():
            for shade, value in shades.items():
                lines.append(f"  --color-{palette_name}-{shade}: {value};")
        for key, value in self.spacing.items():
            lines.append(f"  --spacing-{key}: {value};")
        for key, value in self.font_sizes.items():
            lines.append(f"  --font-size-{key}: {value};")
        for key, value in self.border_radius.items():
            lines.append(f"  --radius-{key}: {value};")
        lines.append("}")
        return "\n".join(lines)

    def to_tailwind_config(self) -> Dict:
        return {
            "theme": {
                "extend": {
                    "colors": self.colors,
                    "spacing": self.spacing,
                    "fontSize": self.font_sizes,
                    "borderRadius": self.border_radius,
                }
            }
        }

    def to_json(self) -> str:
        return json.dumps(self.to_tailwind_config(), indent=2)


# ── Layout Agent ────────────────────────────────────────────────────────────

LAYOUT_TEMPLATES = {
    "dashboard": {
        "description": "Dashboard with sidebar navigation, header, and main content area",
        "html": """\
<div class="min-h-screen flex bg-gray-50">
  <!-- Sidebar -->
  <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
    <div class="p-4 border-b border-gray-200">
      <h1 class="text-xl font-bold text-gray-800">{app_name}</h1>
    </div>
    <nav class="flex-1 p-4 space-y-1">
      <a href="#" class="flex items-center px-3 py-2 rounded-md bg-primary-50 text-primary-700 font-medium">Dashboard</a>
      <a href="#" class="flex items-center px-3 py-2 rounded-md text-gray-600 hover:bg-gray-100">Analytics</a>
      <a href="#" class="flex items-center px-3 py-2 rounded-md text-gray-600 hover:bg-gray-100">Settings</a>
    </nav>
  </aside>

  <!-- Main area -->
  <div class="flex-1 flex flex-col">
    <header class="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6">
      <h2 class="text-lg font-semibold text-gray-800">Dashboard</h2>
      <div class="flex items-center space-x-4">
        <button class="text-gray-500 hover:text-gray-700">Notifications</button>
        <div class="w-8 h-8 rounded-full bg-primary-500 text-white flex items-center justify-center text-sm font-medium">U</div>
      </div>
    </header>

    <main class="flex-1 p-6">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 class="text-sm font-medium text-gray-500">Total Users</h3>
          <p class="text-2xl font-bold text-gray-900 mt-1">12,489</p>
        </div>
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 class="text-sm font-medium text-gray-500">Revenue</h3>
          <p class="text-2xl font-bold text-gray-900 mt-1">$48,352</p>
        </div>
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 class="text-sm font-medium text-gray-500">Conversion</h3>
          <p class="text-2xl font-bold text-gray-900 mt-1">3.24%</p>
        </div>
      </div>
    </main>
  </div>
</div>""",
    },
    "landing": {
        "description": "Landing page with hero, features, and CTA sections",
        "html": """\
<div class="min-h-screen bg-white">
  <!-- Hero -->
  <header class="bg-gradient-to-r from-primary-600 to-primary-800 text-white">
    <nav class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
      <span class="text-xl font-bold">{app_name}</span>
      <div class="space-x-6">
        <a href="#features" class="hover:text-primary-200">Features</a>
        <a href="#pricing" class="hover:text-primary-200">Pricing</a>
        <a href="#" class="bg-white text-primary-700 px-4 py-2 rounded-md font-medium hover:bg-primary-50">Get Started</a>
      </div>
    </nav>
    <div class="max-w-7xl mx-auto px-6 py-24 text-center">
      <h1 class="text-5xl font-extrabold leading-tight">Build faster with {app_name}</h1>
      <p class="mt-4 text-xl text-primary-100 max-w-2xl mx-auto">Ship beautiful products in half the time with our design-first toolkit.</p>
      <button class="mt-8 bg-white text-primary-700 px-8 py-3 rounded-lg font-semibold text-lg hover:bg-primary-50">Start Free Trial</button>
    </div>
  </header>

  <!-- Features -->
  <section id="features" class="max-w-7xl mx-auto px-6 py-20">
    <h2 class="text-3xl font-bold text-center text-gray-900">Features</h2>
    <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
      <div class="text-center p-6">
        <div class="w-12 h-12 bg-primary-100 text-primary-600 rounded-lg mx-auto flex items-center justify-center text-xl font-bold">1</div>
        <h3 class="mt-4 text-lg font-semibold text-gray-900">Fast Setup</h3>
        <p class="mt-2 text-gray-600">Get started in under a minute with zero configuration.</p>
      </div>
      <div class="text-center p-6">
        <div class="w-12 h-12 bg-primary-100 text-primary-600 rounded-lg mx-auto flex items-center justify-center text-xl font-bold">2</div>
        <h3 class="mt-4 text-lg font-semibold text-gray-900">Beautiful Defaults</h3>
        <p class="mt-2 text-gray-600">Production-ready design tokens and components out of the box.</p>
      </div>
      <div class="text-center p-6">
        <div class="w-12 h-12 bg-primary-100 text-primary-600 rounded-lg mx-auto flex items-center justify-center text-xl font-bold">3</div>
        <h3 class="mt-4 text-lg font-semibold text-gray-900">AI-Powered</h3>
        <p class="mt-2 text-gray-600">Claude agents generate and refine designs based on your feedback.</p>
      </div>
    </div>
  </section>
</div>""",
    },
    "form": {
        "description": "Responsive form layout with validation styling",
        "html": """\
<div class="min-h-screen bg-gray-50 flex items-center justify-center p-6">
  <div class="w-full max-w-md bg-white rounded-xl shadow-lg p-8">
    <h2 class="text-2xl font-bold text-gray-900 text-center">{app_name}</h2>
    <p class="mt-2 text-gray-600 text-center">Fill in your details to get started.</p>
    <form class="mt-8 space-y-5">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Full Name</label>
        <input type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent" placeholder="Jane Doe" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input type="email" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent" placeholder="jane@example.com" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
        <input type="password" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent" placeholder="8+ characters" />
      </div>
      <button type="submit" class="w-full bg-primary-600 text-white py-2.5 rounded-lg font-medium hover:bg-primary-700 transition-colors">Create Account</button>
    </form>
  </div>
</div>""",
    },
}


class LayoutAgent:
    """Generates responsive HTML + Tailwind layouts from descriptions."""

    def __init__(self, app_name: str = "MyApp"):
        self.app_name = app_name

    def available_layouts(self) -> List[str]:
        return list(LAYOUT_TEMPLATES.keys())

    def generate(self, layout_type: str) -> str:
        template = LAYOUT_TEMPLATES.get(layout_type)
        if not template:
            raise ValueError(f"Unknown layout: {layout_type}. Available: {self.available_layouts()}")
        return template["html"].format(app_name=self.app_name)

    def describe(self, layout_type: str) -> str:
        template = LAYOUT_TEMPLATES.get(layout_type)
        if not template:
            raise ValueError(f"Unknown layout: {layout_type}")
        return template["description"]


# ── Color Agent ─────────────────────────────────────────────────────────────

PRESET_PALETTES = {
    "ocean":  {"primary": "#0ea5e9", "secondary": "#06b6d4", "accent": "#8b5cf6"},
    "forest": {"primary": "#22c55e", "secondary": "#14b8a6", "accent": "#f59e0b"},
    "sunset": {"primary": "#f97316", "secondary": "#ef4444", "accent": "#a855f7"},
    "slate":  {"primary": "#6366f1", "secondary": "#8b5cf6", "accent": "#ec4899"},
}


class ColorAgent:
    """Creates colour palettes and design tokens from themes or base colours."""

    def generate_tokens(self, theme: str = "ocean") -> DesignTokens:
        preset = PRESET_PALETTES.get(theme, PRESET_PALETTES["ocean"])
        tokens = DesignTokens()
        for name, hex_val in preset.items():
            tokens.colors.update(generate_palette(hex_val, name))
        # Neutral grays
        tokens.colors.update(generate_palette("#64748b", "gray"))
        return tokens

    def generate_from_hex(self, base_hex: str, name: str = "brand") -> DesignTokens:
        tokens = DesignTokens()
        tokens.colors.update(generate_palette(base_hex, name))
        tokens.colors.update(generate_palette("#64748b", "gray"))
        return tokens

    def available_themes(self) -> List[str]:
        return list(PRESET_PALETTES.keys())


# ── Component Spec Agent ────────────────────────────────────────────────────

@dataclass
class ComponentSpec:
    name: str
    description: str
    props: Dict[str, str]
    html: str
    tailwind_classes: List[str]

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "props": self.props,
            "html_template": self.html,
            "key_classes": self.tailwind_classes,
        }


COMPONENT_LIBRARY = {
    "button": ComponentSpec(
        name="Button",
        description="Primary action button with hover/focus states",
        props={"label": "string", "variant": "'primary' | 'secondary' | 'outline'", "size": "'sm' | 'md' | 'lg'", "disabled": "boolean"},
        html='<button class="inline-flex items-center justify-center px-4 py-2 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">{label}</button>',
        tailwind_classes=["bg-primary-600", "hover:bg-primary-700", "focus:ring-2", "rounded-lg", "transition-colors"],
    ),
    "card": ComponentSpec(
        name="Card",
        description="Content card with optional header and footer",
        props={"title": "string", "children": "ReactNode", "footer": "ReactNode | null"},
        html='<div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">\n  <div class="p-6">\n    <h3 class="text-lg font-semibold text-gray-900">{title}</h3>\n    <div class="mt-2 text-gray-600">{children}</div>\n  </div>\n</div>',
        tailwind_classes=["bg-white", "rounded-xl", "shadow-sm", "border", "border-gray-200"],
    ),
    "input": ComponentSpec(
        name="TextInput",
        description="Text input with label, placeholder, and validation states",
        props={"label": "string", "placeholder": "string", "error": "string | null", "required": "boolean"},
        html='<div>\n  <label class="block text-sm font-medium text-gray-700 mb-1">{label}</label>\n  <input type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent" placeholder="{placeholder}" />\n</div>',
        tailwind_classes=["border", "border-gray-300", "rounded-lg", "focus:ring-2", "focus:ring-primary-500"],
    ),
    "avatar": ComponentSpec(
        name="Avatar",
        description="User avatar with fallback initials",
        props={"src": "string | null", "name": "string", "size": "'sm' | 'md' | 'lg'"},
        html='<div class="w-10 h-10 rounded-full bg-primary-500 text-white flex items-center justify-center text-sm font-medium">{initials}</div>',
        tailwind_classes=["rounded-full", "bg-primary-500", "flex", "items-center", "justify-center"],
    ),
    "badge": ComponentSpec(
        name="Badge",
        description="Status badge / tag with color variants",
        props={"label": "string", "variant": "'success' | 'warning' | 'error' | 'info'"},
        html='<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">{label}</span>',
        tailwind_classes=["rounded-full", "text-xs", "font-medium", "bg-primary-100", "text-primary-800"],
    ),
}


class ComponentAgent:
    """Generates component specs from descriptions."""

    def available_components(self) -> List[str]:
        return list(COMPONENT_LIBRARY.keys())

    def get_spec(self, component_name: str) -> ComponentSpec:
        spec = COMPONENT_LIBRARY.get(component_name)
        if not spec:
            raise ValueError(f"Unknown component: {component_name}. Available: {self.available_components()}")
        return spec

    def generate_all_specs(self) -> List[Dict]:
        return [spec.to_dict() for spec in COMPONENT_LIBRARY.values()]


# ── Design-to-Code Agent ───────────────────────────────────────────────────

class DesignToCodeAgent:
    """Combines layout, colour, and component agents to produce full page output."""

    def __init__(self, app_name: str = "MyApp", theme: str = "ocean"):
        self.layout_agent = LayoutAgent(app_name)
        self.color_agent = ColorAgent()
        self.component_agent = ComponentAgent()
        self.tokens = self.color_agent.generate_tokens(theme)

    def generate_page(self, layout_type: str) -> Dict[str, str]:
        html_body = self.layout_agent.generate(layout_type)
        css_vars = self.tokens.to_css_vars()
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{self.layout_agent.app_name}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
{css_vars}
  </style>
</head>
<body>
{html_body}
</body>
</html>"""
        tailwind_config = self.tokens.to_json()
        return {
            "html": full_html,
            "css_variables": css_vars,
            "tailwind_config": tailwind_config,
        }
