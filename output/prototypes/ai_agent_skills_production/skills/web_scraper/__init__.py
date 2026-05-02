"""Web scraper skill - extracts structured data from web pages."""

import re
from skills.base import BaseSkill, SkillResult
from skills.registry import registry


@registry.register
class WebScraperSkill(BaseSkill):
    name = "web_scraper"
    description = "Extract structured data from HTML content"
    version = "1.0.0"

    def validate_input(self, input_data: dict) -> bool:
        return "html" in input_data or "url" in input_data

    def execute(self, input_data: dict) -> SkillResult:
        html = input_data.get("html", "")
        selector = input_data.get("selector", "title")

        # Simple extraction without external deps (production would use BeautifulSoup)
        if selector == "title":
            match = re.search(r"<title>(.*?)</title>", html, re.DOTALL)
            extracted = match.group(1).strip() if match else None
        elif selector == "links":
            extracted = re.findall(r'href="(.*?)"', html)
        elif selector == "headings":
            extracted = re.findall(r"<h[1-6]>(.*?)</h[1-6]>", html)
        else:
            extracted = re.findall(f"<{selector}>(.*?)</{selector}>", html, re.DOTALL)

        return SkillResult(
            success=True,
            data=extracted,
            metadata={"selector": selector, "source_length": len(html)},
        )
