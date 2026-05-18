"""Multi-provider LLM abstraction layer."""

import os
from typing import Optional

import httpx


class LLMProvider:
    """Abstraction over multiple LLM providers (Anthropic, OpenAI)."""

    def __init__(self, mock_mode: bool = True):
        self.mock_mode = mock_mode
        self.providers = {
            "anthropic": {
                "api_key": os.getenv("ANTHROPIC_API_KEY", ""),
                "base_url": "https://api.anthropic.com/v1",
                "default_model": "claude-sonnet-4-20250514",
            },
            "openai": {
                "api_key": os.getenv("OPENAI_API_KEY", ""),
                "base_url": "https://api.openai.com/v1",
                "default_model": "gpt-4o",
            },
        }

    async def complete(
        self,
        prompt: str,
        provider: str = "anthropic",
        model: Optional[str] = None,
        system: Optional[str] = None,
    ) -> str:
        if self.mock_mode:
            return self._mock_complete(prompt, system)

        cfg = self.providers[provider]
        model = model or cfg["default_model"]

        if provider == "anthropic":
            return await self._anthropic_complete(cfg, model, prompt, system)
        elif provider == "openai":
            return await self._openai_complete(cfg, model, prompt, system)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def _anthropic_complete(self, cfg: dict, model: str, prompt: str, system: Optional[str]) -> str:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{cfg['base_url']}/messages",
                headers={
                    "x-api-key": cfg["api_key"],
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": model,
                    "max_tokens": 4096,
                    "system": system or "You are a helpful assistant.",
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=120.0,
            )
            resp.raise_for_status()
            return resp.json()["content"][0]["text"]

    async def _openai_complete(self, cfg: dict, model: str, prompt: str, system: Optional[str]) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{cfg['base_url']}/chat/completions",
                headers={
                    "Authorization": f"Bearer {cfg['api_key']}",
                    "Content-Type": "application/json",
                },
                json={"model": model, "messages": messages, "max_tokens": 4096},
                timeout=120.0,
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]

    def _mock_complete(self, prompt: str, system: Optional[str] = None) -> str:
        """Return contextual mock responses based on the system prompt."""
        sys = (system or "").lower()
        if "planner" in sys or "decompose" in sys:
            return (
                "1. Research competitor landing pages and identify key patterns\n"
                "2. Define page structure, sections, and copy direction\n"
                "3. Generate HTML/CSS implementation with responsive design\n"
                "4. Review output for quality, accessibility, and completeness"
            )
        elif "research" in sys:
            return (
                "Competitor Analysis:\n"
                "- Pattern 1: Hero section with bold headline + demo CTA\n"
                "- Pattern 2: Social proof (logos, testimonials) above the fold\n"
                "- Pattern 3: Feature grid with icons (3-4 key features)\n"
                "Key themes: clarity, social proof, single clear CTA, mobile-first"
            )
        elif "code" in sys or "generat" in sys:
            return (
                "```html\n"
                "<!DOCTYPE html>\n"
                "<html lang=\"en\">\n"
                "<head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
                "<title>WriteAI - AI Writing Assistant</title>\n"
                "<style>\n"
                "  * { margin:0; padding:0; box-sizing:border-box; }\n"
                "  body { font-family: system-ui, sans-serif; }\n"
                "  .hero { padding: 4rem 2rem; text-align: center; background: linear-gradient(135deg, #667eea, #764ba2); color: white; }\n"
                "  .hero h1 { font-size: 3rem; margin-bottom: 1rem; }\n"
                "  .hero p { font-size: 1.25rem; opacity: 0.9; max-width: 600px; margin: 0 auto 2rem; }\n"
                "  .cta { padding: 1rem 2.5rem; background: white; color: #667eea; border: none; border-radius: 8px; font-size: 1.1rem; cursor: pointer; }\n"
                "  .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; padding: 4rem 2rem; max-width: 1000px; margin: 0 auto; }\n"
                "  .feature { text-align: center; padding: 2rem; }\n"
                "  .feature h3 { margin-bottom: 0.5rem; }\n"
                "</style></head>\n"
                "<body>\n"
                "  <section class=\"hero\">\n"
                "    <h1>Write 10x Faster with AI</h1>\n"
                "    <p>WriteAI helps you draft, edit, and polish content in seconds.</p>\n"
                "    <button class=\"cta\">Start Writing Free</button>\n"
                "  </section>\n"
                "  <section class=\"features\">\n"
                "    <div class=\"feature\"><h3>Smart Drafts</h3><p>Generate first drafts from a single prompt.</p></div>\n"
                "    <div class=\"feature\"><h3>Tone Control</h3><p>Switch between professional, casual, and creative.</p></div>\n"
                "    <div class=\"feature\"><h3>SEO Built-in</h3><p>Automatic keyword optimization for every piece.</p></div>\n"
                "  </section>\n"
                "</body></html>\n"
                "```"
            )
        elif "review" in sys or "quality" in sys:
            return (
                "Quality Score: 8.5/10\n\n"
                "Strengths:\n"
                "- Clear value proposition in hero\n"
                "- Clean responsive grid layout\n"
                "- Strong CTA placement\n\n"
                "Suggestions:\n"
                "- Add a testimonials/social proof section\n"
                "- Improve mobile navigation with a hamburger menu\n"
                "- Add meta description for SEO\n"
                "- Consider adding a pricing section"
            )
        else:
            return (
                "1. Plan the task structure\n"
                "2. Research relevant context\n"
                "3. Generate the implementation\n"
                "4. Review and refine"
            )
