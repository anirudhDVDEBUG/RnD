#!/usr/bin/env python3
"""Agentic Organization Requirements Accelerator — CLI entry point."""

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from intake import parse_requirements
from agents import decomposition, dependency, feasibility, specwriter
from validator import cross_validate, generate_report

console = Console()


def run_agent(name, func, requirements):
    """Wrapper to run an agent and track timing."""
    start = time.time()
    result = func(requirements)
    elapsed = time.time() - start
    return name, result, elapsed


def main():
    parser = argparse.ArgumentParser(description="Agentic Requirements Accelerator")
    parser.add_argument("--input", "-i", default="sample_requirements.yaml", help="Path to requirements YAML")
    parser.add_argument("--output", "-o", default="output", help="Output directory")
    args = parser.parse_args()

    # Header
    console.print(Panel.fit(
        "[bold]Agentic Organization Requirements Accelerator[/bold]\n"
        "Parallel agent pipeline for requirements analysis",
        border_style="blue",
    ))

    # Step 1: Intake
    console.print("\n[bold cyan]Step 1:[/bold cyan] Parsing requirements...")
    try:
        intake = parse_requirements(args.input)
    except FileNotFoundError:
        console.print(f"[red]Error: File '{args.input}' not found[/red]")
        sys.exit(1)

    console.print(f"  Project: [bold]{intake.project_name}[/bold]")
    console.print(f"  Requirements loaded: [bold]{len(intake.requirements)}[/bold]")

    # Step 2: Parallel agent execution
    console.print("\n[bold cyan]Step 2:[/bold cyan] Running analysis agents in parallel...\n")

    agents = [
        ("Decomposition Agent", decomposition.run),
        ("Dependency Mapping Agent", dependency.run),
        ("Technical Feasibility Agent", feasibility.run),
        ("Specification Writer Agent", specwriter.run),
    ]

    results = {}
    total_start = time.time()

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(run_agent, name, func, intake.requirements): name
            for name, func in agents
        }
        for i, future in enumerate(as_completed(futures), 1):
            name, result, elapsed = future.result()
            results[name] = result

            # Agent-specific summary
            if name == "Decomposition Agent":
                detail = f"{len(result)} user stories extracted"
            elif name == "Dependency Mapping Agent":
                deps = len(result.get("dependencies", []))
                conflicts = len(result.get("conflicts", []))
                detail = f"{deps} dependencies, {conflicts} conflicts found"
            elif name == "Technical Feasibility Agent":
                detail = f"{len(result)} estimates produced"
            else:
                detail = f"{len(result)} specs generated"

            console.print(f"  [green]Agent {i}/4[/green] {name:<30s} {detail:<40s} [dim]({elapsed:.2f}s)[/dim]")

    total_elapsed = time.time() - total_start

    # Step 3: Cross-validation
    console.print(f"\n[bold cyan]Step 3:[/bold cyan] Cross-validating agent outputs...")

    stories = results["Decomposition Agent"]
    dep_result = results["Dependency Mapping Agent"]
    estimates = results["Technical Feasibility Agent"]
    specs = results["Specification Writer Agent"]

    validation = cross_validate(stories, dep_result, estimates, specs)

    console.print(f"  Warnings: [yellow]{len(validation['warnings'])}[/yellow]")
    console.print(f"  Gaps identified: [yellow]{len(validation['gaps'])}[/yellow]")
    console.print(f"  Total story points: [bold]{validation['total_story_points']}[/bold]")

    # Summary table
    console.print()
    table = Table(title="Phase Breakdown", show_header=True)
    table.add_column("Phase", style="bold")
    table.add_column("Items", justify="right")
    table.add_column("Story Points", justify="right")
    for phase_num in sorted(validation["phase_breakdown"].keys()):
        info = validation["phase_breakdown"][phase_num]
        table.add_row(f"Phase {phase_num}", str(info["count"]), str(info["points"]))
    console.print(table)

    # Step 4: Generate report
    console.print(f"\n[bold cyan]Step 4:[/bold cyan] Generating consolidated report...")

    report = generate_report(
        intake.project_name,
        intake.description,
        stories, dep_result, estimates, specs, validation,
    )

    out_dir = Path(args.output)
    out_dir.mkdir(exist_ok=True)
    report_path = out_dir / "analysis_report.md"
    report_path.write_text(report)

    # Final summary
    total_items = len(stories) + len(dep_result.get("dependencies", [])) + len(estimates) + len(specs)
    console.print(f"\n  Output: [bold green]{report_path}[/bold green] ({total_items} items across 3 phases)")
    console.print(f"  Total analysis time: [bold]{total_elapsed:.2f}s[/bold]")

    console.print(Panel.fit(
        f"[bold green]Done![/bold green] {len(intake.requirements)} requirements -> "
        f"{len(stories)} stories, {validation['total_story_points']} points, "
        f"{len(validation['phase_breakdown'])} phases\n"
        f"Report: {report_path}",
        border_style="green",
    ))

    # Print warnings
    if validation["warnings"]:
        console.print("\n[bold yellow]Warnings:[/bold yellow]")
        for w in validation["warnings"]:
            console.print(f"  [yellow]![/yellow] {w}")

    if validation["gaps"]:
        console.print("\n[bold yellow]Gaps:[/bold yellow]")
        for g in validation["gaps"]:
            console.print(f"  [yellow]![/yellow] {g['message']}")


if __name__ == "__main__":
    main()
