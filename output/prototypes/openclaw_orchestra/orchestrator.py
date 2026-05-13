"""
Orchestrator: decomposes tasks, assigns to specialist agents, coordinates execution.
Optionally integrates with Linear for ticket-backed oversight.
"""

import os
import json
import time
from datetime import datetime

from agent import SpecialistAgent
from orchestra_config import load_config


class LinearTracker:
    """Mock Linear integration for ticket oversight."""

    def __init__(self, api_key=None, team_id=None):
        self.api_key = api_key
        self.team_id = team_id
        self.enabled = bool(api_key and team_id)
        self.tickets = []

    def create_ticket(self, title, description, assignee=None):
        ticket = {
            "id": f"LIN-{len(self.tickets) + 100}",
            "title": title,
            "description": description,
            "assignee": assignee,
            "status": "Todo",
            "created": datetime.now().isoformat(),
        }
        self.tickets.append(ticket)
        if self.enabled:
            print(f"  [Linear] Created ticket {ticket['id']}: {title}")
        else:
            print(f"  [Linear-Mock] Created ticket {ticket['id']}: {title}")
        return ticket

    def update_ticket(self, ticket_id, status):
        for t in self.tickets:
            if t["id"] == ticket_id:
                t["status"] = status
                print(f"  [Linear-Mock] {ticket_id} -> {status}")
                return t
        return None


class TaskDecomposer:
    """Breaks a high-level task into subtasks assigned to specialist agents."""

    DECOMPOSITION_RULES = {
        "backend-specialist": [
            "data model", "api", "endpoint", "database", "server",
            "authentication", "backend", "logic", "migration",
        ],
        "frontend-specialist": [
            "ui", "component", "form", "page", "frontend", "style",
            "layout", "button", "input", "display",
        ],
        "reviewer": [],  # reviewer always gets a review subtask
    }

    def decompose(self, task_description, agents_config):
        """Split task into subtasks based on agent specializations."""
        subtasks = []
        task_lower = task_description.lower()
        idx = 0

        for agent_cfg in agents_config:
            name = agent_cfg["name"]
            if name == "reviewer":
                continue  # reviewer added last

            keywords = self.DECOMPOSITION_RULES.get(name, [])
            # Check if any keyword matches or assign by default
            relevant = any(kw in task_lower for kw in keywords) or not keywords
            if relevant:
                idx += 1
                subtasks.append({
                    "id": f"subtask_{idx:03d}",
                    "title": f"[{name}] {task_description}",
                    "assigned_to": name,
                    "description": task_description,
                    "priority": "high" if idx == 1 else "medium",
                })

        # Always add a review subtask
        idx += 1
        subtasks.append({
            "id": f"subtask_{idx:03d}",
            "title": f"[reviewer] Review: {task_description}",
            "assigned_to": "reviewer",
            "description": f"Review all agent outputs for: {task_description}",
            "priority": "medium",
        })

        return subtasks


class Orchestrator:
    """Main orchestrator that coordinates specialist agents."""

    def __init__(self, config_path=None, use_api=False):
        self.config = load_config(config_path)
        self.use_api = use_api
        self.decomposer = TaskDecomposer()
        self.linear = LinearTracker(
            api_key=os.environ.get("LINEAR_API_KEY"),
            team_id=os.environ.get("LINEAR_TEAM_ID"),
        )
        self.agents = {}
        self._init_agents()

    def _init_agents(self):
        for agent_cfg in self.config["agents"]:
            agent = SpecialistAgent(
                name=agent_cfg["name"],
                workspace=agent_cfg["workspace"],
                tools=agent_cfg["tools"],
                prompt=agent_cfg["prompt"],
                use_api=self.use_api,
            )
            self.agents[agent_cfg["name"]] = agent

    def run(self, task_description):
        """Execute a full orchestration run."""
        print(f"\n{'='*60}")
        print(f"OPENCLAW ORCHESTRA - Multi-Agent Orchestration")
        print(f"{'='*60}")
        print(f"Task: {task_description}")
        print(f"Agents: {', '.join(self.agents.keys())}")
        print(f"Mode: {'API' if self.use_api else 'Mock (no API key needed)'}")
        print(f"Linear: {'Connected' if self.linear.enabled else 'Mock mode'}")
        print(f"{'='*60}\n")

        # Step 1: Decompose task
        print("[Orchestrator] Decomposing task into subtasks...")
        subtasks = self.decomposer.decompose(task_description, self.config["agents"])
        print(f"[Orchestrator] Created {len(subtasks)} subtasks:\n")
        for st in subtasks:
            print(f"  - {st['id']}: {st['title']} (priority: {st['priority']})")
        print()

        # Step 2: Create Linear tickets
        print("[Orchestrator] Creating oversight tickets...\n")
        ticket_map = {}
        for st in subtasks:
            ticket = self.linear.create_ticket(
                title=st["title"],
                description=st["description"],
                assignee=st["assigned_to"],
            )
            ticket_map[st["id"]] = ticket
        print()

        # Step 3: Execute subtasks (specialist agents first, reviewer last)
        results = []
        specialist_tasks = [s for s in subtasks if s["assigned_to"] != "reviewer"]
        review_tasks = [s for s in subtasks if s["assigned_to"] == "reviewer"]

        print("[Orchestrator] Executing specialist agent subtasks...\n")
        for st in specialist_tasks:
            agent = self.agents[st["assigned_to"]]
            ticket = ticket_map[st["id"]]
            self.linear.update_ticket(ticket["id"], "In Progress")

            result = agent.execute_subtask(st)
            results.append(result)

            status = "Done" if result["status"] == "completed" else "Failed"
            self.linear.update_ticket(ticket["id"], status)
            print()

        print("[Orchestrator] Running review agent...\n")
        for st in review_tasks:
            agent = self.agents[st["assigned_to"]]
            ticket = ticket_map[st["id"]]
            self.linear.update_ticket(ticket["id"], "In Progress")

            result = agent.execute_subtask(st)
            results.append(result)

            status = "Done" if result["status"] == "completed" else "Failed"
            self.linear.update_ticket(ticket["id"], status)
            print()

        # Step 4: Summary
        self._print_summary(results, ticket_map)
        return results

    def _print_summary(self, results, ticket_map):
        print(f"{'='*60}")
        print("ORCHESTRATION SUMMARY")
        print(f"{'='*60}\n")

        completed = sum(1 for r in results if r["status"] == "completed")
        failed = sum(1 for r in results if r["status"] != "completed")

        print(f"  Total subtasks: {len(results)}")
        print(f"  Completed:      {completed}")
        print(f"  Failed:         {failed}")
        print()

        print("  Agent Workspaces:")
        for name, agent in self.agents.items():
            files = []
            if os.path.exists(agent.workspace):
                files = [f for f in os.listdir(agent.workspace) if not f.startswith(".")]
            print(f"    {name}: {agent.workspace} ({len(files)} artifacts)")

        print()
        print("  Linear Tickets:")
        for ticket in self.linear.tickets:
            print(f"    {ticket['id']}: [{ticket['status']}] {ticket['title']}")

        print(f"\n{'='*60}")
        print("All agents finished. Artifacts written to ./workspaces/")
        print(f"{'='*60}\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="OpenClaw Orchestra - Multi-Agent Orchestration")
    parser.add_argument("--config", default=None, help="Path to orchestra YAML/JSON config")
    parser.add_argument("--task", default="Implement user authentication flow",
                        help="Task description to orchestrate")
    parser.add_argument("--use-api", action="store_true", help="Use real Claude API (requires ANTHROPIC_API_KEY)")
    args = parser.parse_args()

    orchestrator = Orchestrator(config_path=args.config, use_api=args.use_api)
    orchestrator.run(args.task)


if __name__ == "__main__":
    main()
