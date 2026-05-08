# How to Use — Fabric & Power BI Workflow Skill

## Installation (30 seconds)

This is a **Claude Code skill** (not an MCP server). Drop it into your skills directory:

```bash
# Create the skill folder
mkdir -p ~/.claude/skills/fabric_powerbi_workflow

# Copy the skill file
cp SKILL.md ~/.claude/skills/fabric_powerbi_workflow/SKILL.md
```

That's it. Claude Code auto-discovers skills from `~/.claude/skills/`.

## Trigger Phrases

Claude activates this skill when you mention any of:

| Phrase | Example |
|--------|---------|
| Microsoft Fabric | "Set up a Fabric lakehouse pipeline" |
| Power BI | "Build a Power BI report for sales" |
| DAX | "Write a DAX measure for YoY growth" |
| Power Query M | "Create a Power Query M transformation" |
| Fabric notebook | "Configure a Fabric notebook with PySpark" |
| Semantic model | "Help me design a semantic model" |
| Fabric pipeline | "Create a Fabric pipeline for daily ingestion" |
| Fabric lakehouse / warehouse | "Query the Fabric warehouse with T-SQL" |

## First 60 Seconds

**Input:**
```
Write a DAX measure for calculating year-over-year revenue growth,
following best practices for a star schema with a Date dimension.
```

**Output (Claude generates):**
```dax
Revenue YoY Growth % =
VAR CurrentRevenue =
    SUM( FactSales[Revenue] )
VAR PriorYearRevenue =
    CALCULATE(
        SUM( FactSales[Revenue] ),
        DATEADD( DimDate[Date], -1, YEAR )
    )
RETURN
    IF(
        NOT ISBLANK( PriorYearRevenue ),
        DIVIDE(
            CurrentRevenue - PriorYearRevenue,
            PriorYearRevenue
        )
    )
```

Notice: uses `VAR/RETURN` for readability, `DIVIDE` for safe division, references star-schema table names (`FactSales`, `DimDate`), and handles blank prior year gracefully.

## Running the Demo

```bash
bash run.sh
```

This runs a local Python demo that generates example Fabric/Power BI artifacts (DAX measures, Power Query M scripts, PySpark notebook cells, and a medallion-architecture layout) — no API keys needed.
