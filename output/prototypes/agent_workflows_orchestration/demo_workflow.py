#!/usr/bin/env python3
"""
Demo: fan-out → pipeline → validate workflow using the fake adapter.

No API keys required.  Run with:  python demo_workflow.py
"""

from agent_workflows import Workflow, Step

def main():
    print("=" * 60)
    print("  agent-workflows demo: research-and-summarize")
    print("=" * 60)
    print()

    wf = Workflow(name="research-and-summarize", journal_path="demo_journal.sqlite")

    # 1. Fan-out: research three topics in parallel
    research_steps = wf.fan_out(
        prompt="Research the current state of {topic} and list 3 key takeaways.",
        topics=["AI safety", "agent architectures", "tool use in LLMs"],
        adapter="fake",
    )

    # 2. Pipeline: feed all research results into a summarizer
    summary = wf.pipeline(
        steps=research_steps,
        then=Step(prompt="Synthesize the research above into a concise executive summary."),
    )

    # 3. Validate: summary must be >= 50 chars
    wf.validate(summary, schema={"type": "string", "minLength": 50})

    # 4. Run with a $0.50 budget cap
    print("--- Executing workflow ---\n")
    run_id = wf.run(budget=0.50, adapter="fake")

    # 5. Show results
    print("\n--- Step results ---\n")
    for step in wf.steps:
        print(f"  [{step.status}] {step.name}")
        if step.result:
            for line in step.result.splitlines():
                print(f"         {line}")
        print()

    # 6. Show journal
    print("--- Run journal (SQLite) ---\n")
    for run in wf.journal.list_runs():
        print(f"  {run['run_id']}  {run['status']:<18}  cost=${run['total_cost']:.4f}  ({run['started_at']})")

    print()
    print("Done. Journal saved to demo_journal.sqlite")


if __name__ == "__main__":
    main()
