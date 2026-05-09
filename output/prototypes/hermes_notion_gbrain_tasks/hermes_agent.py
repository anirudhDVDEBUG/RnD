"""
Hermes Agent: Natural language task management via WhatsApp/Slack -> Notion
with GBrain knowledge enrichment.
"""

import json
import re
import os
from datetime import datetime, timedelta


class NLPParser:
    """Parses natural language messages into structured task intents."""

    INTENT_PATTERNS = {
        "create": [
            r"(?:add|create|make|new|schedule)\s+(?:a\s+)?task\s+(?:to\s+)?(.+)",
            r"(?:remind me to|i need to|don't forget to)\s+(.+)",
            r"(?:todo|to-do|to do)[:;]?\s+(.+)",
        ],
        "update": [
            r"(?:update|change|modify|edit)\s+(?:the\s+)?task\s+['\"]?(.+?)['\"]?\s+(?:to|with)\s+(.+)",
            r"(?:set|mark)\s+['\"]?(.+?)['\"]?\s+(?:as|to)\s+(.+)",
        ],
        "complete": [
            r"(?:complete|finish|done|close)\s+(?:the\s+)?task\s+['\"]?(.+?)['\"]?$",
            r"(?:i(?:'ve)?|we(?:'ve)?)\s+(?:completed|finished|done)\s+['\"]?(.+?)['\"]?$",
        ],
        "list": [
            r"(?:list|show|get|what are)\s+(?:my\s+|all\s+|the\s+)?tasks",
            r"what(?:'s| is) (?:on my|pending|left|to do)",
        ],
    }

    PRIORITY_KEYWORDS = {
        "high": ["urgent", "asap", "critical", "important", "high priority", "immediately"],
        "medium": ["soon", "this week", "medium priority", "normal"],
        "low": ["eventually", "when possible", "low priority", "no rush", "sometime"],
    }

    DATE_PATTERNS = {
        r"by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)": "next_weekday",
        r"by\s+(tomorrow)": "tomorrow",
        r"by\s+(?:end of\s+)?(today)": "today",
        r"by\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)": "date",
        r"in\s+(\d+)\s+days?": "relative_days",
        r"(?:next|this)\s+(week|month)": "relative_period",
    }

    def parse(self, message: str) -> dict:
        message_lower = message.lower().strip()
        intent = self._detect_intent(message_lower)
        result = {
            "raw_message": message,
            "intent": intent["type"],
            "confidence": intent["confidence"],
            "title": self._extract_title(message, intent),
            "priority": self._detect_priority(message_lower),
            "due_date": self._extract_due_date(message_lower),
            "tags": self._extract_tags(message),
            "parsed_at": datetime.now().isoformat(),
        }
        return result

    def _detect_intent(self, message: str) -> dict:
        for intent_type, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, message, re.IGNORECASE):
                    return {"type": intent_type, "confidence": 0.9}
        if any(word in message for word in ["task", "todo", "to-do"]):
            return {"type": "create", "confidence": 0.6}
        return {"type": "create", "confidence": 0.5}

    def _extract_title(self, message: str, intent: dict) -> str:
        for pattern in self.INTENT_PATTERNS.get(intent["type"], []):
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Remove trailing date/priority phrases
                title = re.sub(r"\s+by\s+\w+$", "", title)
                title = re.sub(r"\s+(?:urgent|asap|high priority)$", "", title, flags=re.IGNORECASE)
                return title
        return message.strip()

    def _detect_priority(self, message: str) -> str:
        for priority, keywords in self.PRIORITY_KEYWORDS.items():
            if any(kw in message for kw in keywords):
                return priority
        return "medium"

    def _extract_due_date(self, message: str) -> str | None:
        today = datetime.now()
        if "tomorrow" in message:
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")
        if "today" in message:
            return today.strftime("%Y-%m-%d")
        match = re.search(r"in\s+(\d+)\s+days?", message)
        if match:
            days = int(match.group(1))
            return (today + timedelta(days=days)).strftime("%Y-%m-%d")
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for i, day in enumerate(weekdays):
            if f"by {day}" in message:
                current_day = today.weekday()
                diff = (i - current_day) % 7
                if diff == 0:
                    diff = 7
                return (today + timedelta(days=diff)).strftime("%Y-%m-%d")
        return None

    def _extract_tags(self, message: str) -> list[str]:
        tags = re.findall(r"#(\w+)", message)
        category_keywords = {
            "work": ["meeting", "report", "review", "presentation", "deadline"],
            "personal": ["buy", "grocery", "doctor", "gym", "call mom"],
            "dev": ["deploy", "code", "bug", "feature", "test", "merge"],
        }
        for category, keywords in category_keywords.items():
            if any(kw in message.lower() for kw in keywords):
                if category not in tags:
                    tags.append(category)
        return tags


class GBrainEnricher:
    """Enriches tasks with knowledge from GBrain knowledge base."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key
        # Mock knowledge base for demo
        self.knowledge_base = {
            "report": {
                "context": "Company reports follow the Q-template format. Last quarterly review highlighted revenue growth of 15%.",
                "related_docs": ["Q3-Report-Template.docx", "Revenue-Dashboard-Link"],
                "suggested_assignees": ["analytics-team"],
            },
            "deploy": {
                "context": "Deployment follows CI/CD pipeline: staging -> QA -> production. Requires 2 approvals.",
                "related_docs": ["Deployment-Checklist.md", "CI-CD-Pipeline-Docs"],
                "suggested_assignees": ["devops-team"],
            },
            "meeting": {
                "context": "Team meetings use the standing-agenda template. Record action items in #meeting-notes.",
                "related_docs": ["Meeting-Agenda-Template", "Zoom-Room-Links"],
                "suggested_assignees": ["team-lead"],
            },
            "review": {
                "context": "Code reviews require at least 2 approvals. Use the PR template for consistency.",
                "related_docs": ["PR-Template.md", "Code-Review-Guidelines"],
                "suggested_assignees": ["senior-devs"],
            },
            "design": {
                "context": "Design assets are in Figma. Follow the brand guidelines v2.1 for all new work.",
                "related_docs": ["Brand-Guidelines-v2.1", "Figma-Project-Link"],
                "suggested_assignees": ["design-team"],
            },
        }

    def enrich(self, parsed_task: dict) -> dict:
        title_lower = parsed_task.get("title", "").lower()
        tags = parsed_task.get("tags", [])
        enrichment = {
            "knowledge_context": None,
            "related_documents": [],
            "suggested_assignees": [],
            "enrichment_score": 0.0,
        }
        for keyword, knowledge in self.knowledge_base.items():
            if keyword in title_lower or keyword in " ".join(tags):
                enrichment["knowledge_context"] = knowledge["context"]
                enrichment["related_documents"] = knowledge["related_docs"]
                enrichment["suggested_assignees"] = knowledge["suggested_assignees"]
                enrichment["enrichment_score"] = 0.85
                break

        if enrichment["enrichment_score"] == 0.0:
            enrichment["knowledge_context"] = "No specific knowledge match found. Consider adding context manually."
            enrichment["enrichment_score"] = 0.2

        parsed_task["gbrain_enrichment"] = enrichment
        return parsed_task


class NotionTaskManager:
    """Manages tasks in a Notion database."""

    def __init__(self, api_key: str | None = None, database_id: str | None = None):
        self.api_key = api_key
        self.database_id = database_id
        self.tasks: list[dict] = []

    def create_task(self, enriched_task: dict) -> dict:
        notion_page = {
            "id": f"notion-{len(self.tasks) + 1:04d}",
            "properties": {
                "Name": {"title": [{"text": {"content": enriched_task["title"]}}]},
                "Status": {"select": {"name": "To Do"}},
                "Priority": {"select": {"name": enriched_task["priority"].capitalize()}},
                "Due Date": {"date": {"start": enriched_task.get("due_date")} if enriched_task.get("due_date") else None},
                "Tags": {"multi_select": [{"name": t} for t in enriched_task.get("tags", [])]},
            },
            "children": [],
        }
        # Add GBrain enrichment as a block
        gbrain = enriched_task.get("gbrain_enrichment", {})
        if gbrain.get("knowledge_context"):
            notion_page["children"].append({
                "type": "callout",
                "callout": {
                    "rich_text": [{"text": {"content": f"GBrain Context: {gbrain['knowledge_context']}"}}],
                    "icon": {"emoji": "🧠"},
                },
            })
        if gbrain.get("related_documents"):
            notion_page["children"].append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"text": {"content": f"Related: {', '.join(gbrain['related_documents'])}"}}],
                },
            })
        self.tasks.append(notion_page)
        return notion_page

    def list_tasks(self) -> list[dict]:
        return self.tasks

    def complete_task(self, task_id: str) -> dict | None:
        for task in self.tasks:
            if task["id"] == task_id:
                task["properties"]["Status"]["select"]["name"] = "Done"
                return task
        return None

    def format_task_summary(self, task: dict) -> str:
        props = task["properties"]
        title = props["Name"]["title"][0]["text"]["content"]
        status = props["Status"]["select"]["name"]
        priority = props["Priority"]["select"]["name"]
        due = props["Due Date"]["date"]["start"] if props["Due Date"] else "No due date"
        tags = ", ".join(t["name"] for t in props["Tags"]["multi_select"]) if props["Tags"]["multi_select"] else "none"
        return f"  [{status}] {title} | Priority: {priority} | Due: {due} | Tags: {tags}"


class HermesAgent:
    """Main agent coordinating NLP parsing, GBrain enrichment, and Notion task management."""

    def __init__(self, notion_api_key=None, notion_db_id=None, gbrain_api_key=None):
        self.parser = NLPParser()
        self.enricher = GBrainEnricher(api_key=gbrain_api_key)
        self.notion = NotionTaskManager(api_key=notion_api_key, database_id=notion_db_id)

    def process_message(self, message: str, source: str = "whatsapp") -> dict:
        parsed = self.parser.parse(message)
        parsed["source_channel"] = source

        if parsed["intent"] == "create":
            enriched = self.enricher.enrich(parsed)
            notion_page = self.notion.create_task(enriched)
            return {
                "action": "created",
                "task": enriched,
                "notion_page_id": notion_page["id"],
                "reply": f"Task created: \"{enriched['title']}\" (Priority: {enriched['priority']}, Due: {enriched.get('due_date', 'unset')})",
            }
        elif parsed["intent"] == "list":
            tasks = self.notion.list_tasks()
            summaries = [self.notion.format_task_summary(t) for t in tasks]
            return {
                "action": "listed",
                "count": len(tasks),
                "reply": f"You have {len(tasks)} task(s):\n" + "\n".join(summaries) if tasks else "No tasks found.",
            }
        elif parsed["intent"] == "complete":
            # Try to find matching task
            for task in self.notion.tasks:
                title = task["properties"]["Name"]["title"][0]["text"]["content"].lower()
                if parsed["title"].lower() in title or title in parsed["title"].lower():
                    self.notion.complete_task(task["id"])
                    return {
                        "action": "completed",
                        "task_id": task["id"],
                        "reply": f"Task \"{parsed['title']}\" marked as done!",
                    }
            return {"action": "not_found", "reply": f"Could not find task matching \"{parsed['title']}\""}
        else:
            return {"action": "unknown", "reply": f"I understood intent '{parsed['intent']}' but this action isn't implemented in the demo."}
