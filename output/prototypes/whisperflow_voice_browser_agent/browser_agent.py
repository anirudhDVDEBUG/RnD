"""Browser automation via Playwright (real) or simulated DOM (mock)."""

import os
import base64
import json

MOCK_MODE = os.environ.get("WHISPERFLOW_MOCK", "1") == "1"


class BrowserAgent:
    """Wraps Playwright for navigation, screenshots, and action execution."""

    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
        self._mock_url = "https://news.ycombinator.com"
        self._mock_title = "Hacker News"
        self._mock_action_log: list[dict] = []

    async def start(self, headless=False):
        if MOCK_MODE:
            print("[mock-browser] Chromium launched (simulated)")
            return
        from playwright.async_api import async_playwright
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()

    async def navigate(self, url: str):
        if MOCK_MODE:
            self._mock_url = url
            self._mock_title = url.split("//")[-1].split("/")[0]
            print(f"[mock-browser] Navigated to {url}")
            return
        await self.page.goto(url, wait_until="domcontentloaded", timeout=15000)

    async def screenshot_base64(self) -> str:
        if MOCK_MODE:
            # 1x1 transparent PNG
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAAIABQAB"
        img_bytes = await self.page.screenshot(full_page=False)
        return base64.b64encode(img_bytes).decode()

    async def execute_action(self, action: dict) -> bool:
        act = action.get("action")
        selector = action.get("selector", "")
        value = action.get("value", "")

        if MOCK_MODE:
            self._mock_action_log.append(action)
            print(f"[mock-browser] Executed: {act} selector={selector!r} value={value!r}")
            if act == "navigate":
                await self.navigate(value)
            return True

        try:
            if act == "click":
                await self.page.click(selector, timeout=5000)
            elif act == "type":
                await self.page.fill(selector, value)
            elif act == "navigate":
                await self.navigate(value)
            elif act == "scroll_down":
                await self.page.evaluate("window.scrollBy(0, 500)")
            elif act == "scroll_up":
                await self.page.evaluate("window.scrollBy(0, -500)")
            elif act == "wait":
                await self.page.wait_for_timeout(int(value) if value else 2000)
            elif act == "press":
                await self.page.keyboard.press(value)
            return True
        except Exception as e:
            print(f"Action failed: {e}")
            return False

    async def get_page_context(self) -> str:
        if MOCK_MODE:
            return json.dumps({
                "title": self._mock_title,
                "url": self._mock_url,
                "elements": [
                    {"tag": "A", "text": "Top Story: AI Agents Are Everywhere", "href": "#story1"},
                    {"tag": "A", "text": "Second Story: Voice-First Interfaces", "href": "#story2"},
                    {"tag": "INPUT", "type": "text", "name": "q", "placeholder": "Search..."},
                    {"tag": "BUTTON", "text": "Submit"},
                ],
            })
        return await self.page.evaluate("""() => {
            const els = document.querySelectorAll('a, button, input, select, textarea, [role=button]');
            const items = Array.from(els).slice(0, 50).map(el => ({
                tag: el.tagName, text: el.innerText?.slice(0, 80),
                id: el.id, name: el.name, type: el.type,
                href: el.href, placeholder: el.placeholder
            }));
            return JSON.stringify({ title: document.title, url: location.href, elements: items });
        }""")

    async def close(self):
        if MOCK_MODE:
            print("[mock-browser] Browser closed")
            return
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
