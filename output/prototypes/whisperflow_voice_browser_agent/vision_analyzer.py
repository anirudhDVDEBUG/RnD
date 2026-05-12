"""GPT-4o Vision screenshot analyzer (or mock planner)."""

import os
import json

MOCK_MODE = os.environ.get("WHISPERFLOW_MOCK", "1") == "1"


class VisionAnalyzer:
    """Analyze a browser screenshot + page context to decide next actions."""

    def __init__(self, client=None):
        self.client = client

    def plan_actions(self, user_command: str, page_context: str, screenshot_b64: str) -> list[dict]:
        if MOCK_MODE:
            return self._mock_plan(user_command, page_context)
        return self._real_plan(user_command, page_context, screenshot_b64)

    # -- mock planner (keyword heuristic) ----------------------------------
    def _mock_plan(self, command: str, page_context: str) -> list[dict]:
        cmd = command.lower()
        actions = []

        if "go to" in cmd or "open" in cmd:
            # extract domain-ish target
            if "hacker news" in cmd:
                actions.append({"action": "navigate", "value": "https://news.ycombinator.com"})
            elif "wikipedia" in cmd:
                actions.append({"action": "navigate", "value": "https://en.wikipedia.org"})
            elif "google" in cmd:
                actions.append({"action": "navigate", "value": "https://www.google.com"})
            else:
                actions.append({"action": "navigate", "value": "https://www.google.com"})

        if "search" in cmd:
            query = cmd.split("search")[-1].strip().strip("'\"")
            if "for" in query:
                query = query.split("for", 1)[-1].strip().strip("'\"")
            actions.append({"action": "click", "selector": "input[name='q'], input[type='text']"})
            actions.append({"action": "type", "selector": "input[name='q'], input[type='text']", "value": query})
            actions.append({"action": "press", "value": "Enter"})

        if "scroll down" in cmd:
            actions.append({"action": "scroll_down"})
        if "scroll up" in cmd:
            actions.append({"action": "scroll_up"})
        if "click" in cmd:
            actions.append({"action": "click", "selector": "a"})
        if "go back" in cmd:
            actions.append({"action": "press", "value": "Alt+ArrowLeft"})
        if "screenshot" in cmd or "look" in cmd or "find" in cmd:
            pass  # screenshot is always taken

        if not actions:
            actions.append({"action": "wait", "value": "1000"})

        return actions

    # -- real planner (GPT-4o Vision) --------------------------------------
    def _real_plan(self, command: str, page_context: str, screenshot_b64: str) -> list[dict]:
        system_prompt = (
            "You are a browser automation agent. Given a user command, the current page context "
            "(JSON with title, url, interactive elements) and a screenshot, output a JSON array of "
            "actions. Each action is {action, selector?, value?}. Valid actions: click, type, "
            "navigate, scroll_down, scroll_up, wait, press. Be precise with CSS selectors."
        )
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Command: {command}\n\nPage context:\n{page_context}"},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}},
                    ],
                },
            ],
            response_format={"type": "json_object"},
            max_tokens=1024,
        )
        raw = response.choices[0].message.content
        parsed = json.loads(raw)
        return parsed.get("actions", parsed) if isinstance(parsed, dict) else parsed
