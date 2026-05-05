"""Core Agent: orchestrates memory, vision grounding, and skill execution."""

import time
from photo_agents.memory import MemoryLayer
from photo_agents.vision import VisionGrounding
from photo_agents.skills import SkillRegistry


class Agent:
    """Autonomous self-evolving agent with vision-grounded layered memory."""

    def __init__(
        self,
        memory: MemoryLayer | None = None,
        vision: VisionGrounding | None = None,
        skill_dir: str = "./skills",
        auto_skill_extraction: bool = True,
        name: str = "PhotoAgent",
    ):
        self.name = name
        self.memory = memory or MemoryLayer()
        self.vision = vision or VisionGrounding()
        self.skills = SkillRegistry(skill_dir=skill_dir)
        self.auto_skill_extraction = auto_skill_extraction
        self._action_log: list[str] = []

    def think(self, observation: str) -> str:
        """Process an observation, ground it in vision, store in memory."""
        # Capture visual context
        capture = self.vision.capture(context=observation)

        # Store in working memory with vision anchor
        self.memory.remember(observation, vision_anchor=capture.path)

        # Check if we have a relevant skill
        relevant_skills = [
            s for s in self.skills.list_skills()
            if any(word in s for word in observation.lower().split())
        ]

        if relevant_skills:
            reasoning = f"[{self.name}] Observed: '{observation}' | Found relevant skill: {relevant_skills[0]} | Vision grounded at: {capture.path}"
        else:
            reasoning = f"[{self.name}] Observed: '{observation}' | No matching skill, exploring... | Vision grounded at: {capture.path}"

        return reasoning

    def act(self, action: str) -> str:
        """Execute an action, record it, potentially extract skills."""
        self._action_log.append(action)

        # Ground the action with a screenshot
        capture = self.vision.capture(context=f"action:{action}")
        self.memory.remember(f"Executed: {action}", vision_anchor=capture.path)

        # Check if this matches an existing skill
        skill = self.skills.get_skill(action)
        if skill:
            result = skill.execute()
            return f"[{self.name}] Executed skill '{action}':\n{result}"

        # Record action sequence for potential skill extraction
        if self.auto_skill_extraction and len(self._action_log) >= 2:
            self.skills.record_action_sequence(self._action_log[-3:], success=True)

        return f"[{self.name}] Executed action: {action} [OK]"

    def run(self, task: str, steps: int = 5, computer_use: bool = False, safety_mode: bool = True) -> dict:
        """Run the agent on a task for a given number of reasoning steps."""
        print(f"\n{'='*60}")
        print(f"  Agent: {self.name}")
        print(f"  Task: {task}")
        print(f"  Computer-use: {computer_use} | Safety: {safety_mode}")
        print(f"{'='*60}\n")

        # Store task in semantic memory
        self.memory.semantic.store("current_task", task)

        results = []
        for step in range(1, steps + 1):
            print(f"--- Step {step}/{steps} ---")

            # Think phase
            observation = f"Step {step} context for: {task}"
            thought = self.think(observation)
            print(f"  THINK: {thought}")

            # Act phase
            action = f"step_{step}_action"
            action_result = self.act(action)
            print(f"  ACT:   {action_result}")

            results.append({"step": step, "thought": thought, "action": action_result})

            # Record episode
            self.memory.episodic.record_episode(
                actions=[action],
                outcome=f"Completed step {step}",
                vision_frames=[self.vision._captures[-1].path] if self.vision._captures else [],
            )
            print()

        # Final summary
        summary = {
            "task": task,
            "steps_completed": steps,
            "memory": self.memory.summarize(),
            "skills_available": self.skills.list_skills(),
            "vision_captures": self.vision.capture_count,
        }

        print(f"{'='*60}")
        print(f"  COMPLETE - Memory: {summary['memory']}")
        print(f"  Skills learned: {summary['skills_available']}")
        print(f"  Vision captures: {summary['vision_captures']}")
        print(f"{'='*60}\n")

        return summary
