---
name: fabric_powerbi_workflow
description: |
  Configure Claude Code for Microsoft Fabric and Power BI data engineering workflows on Windows.
  TRIGGER: user mentions Microsoft Fabric, Power BI, Fabric lakehouse, Fabric warehouse, DAX, Power Query M, Fabric notebooks, Fabric pipelines, semantic models, or analytics engineering with Fabric/PBI.
  DO NOT TRIGGER: general data engineering without Fabric/PBI context, Azure Synapse (non-Fabric), or plain SQL tasks.
---

# Fabric & Power BI Workflow Skill

Claude Code skill for Microsoft Fabric and Power BI data engineering workflows. Provides conventions, patterns, and rules for working with Fabric lakehouses, warehouses, notebooks, pipelines, semantic models, DAX, Power Query M, and Power BI report development.

## When to use

- "Set up a Fabric lakehouse pipeline for ingesting CSV data"
- "Write a DAX measure for year-over-year growth in Power BI"
- "Create a Power Query M transformation for cleaning customer data"
- "Help me build a semantic model in Microsoft Fabric"
- "Configure a Fabric notebook for data transformation with PySpark"

## How to use

1. **Fabric Lakehouse & Warehouse workflows**:
   - Use T-SQL for Fabric warehouse queries; PySpark or Spark SQL for lakehouse notebooks.
   - Follow medallion architecture (bronze/silver/gold) for data layering in lakehouses.
   - Use Delta Lake format as the default table format in Fabric lakehouses.
   - Prefer `COPY INTO` or Fabric pipelines for data ingestion over manual uploads.

2. **Power BI semantic models & DAX**:
   - Write DAX measures using `CALCULATE`, `FILTER`, `ALL`, `REMOVEFILTERS` for complex calculations.
   - Use variables (`VAR`/`RETURN`) in DAX for readability and performance.
   - Follow star schema design: fact tables with surrogate keys referencing dimension tables.
   - Prefer measures over calculated columns for aggregations.

3. **Power Query M transformations**:
   - Use `let`/`in` blocks for step-by-step transformations.
   - Apply query folding where possible (push computation to source).
   - Name steps descriptively (e.g., `RemovedNulls`, `FilteredByDate`).
   - Use `Table.TransformColumnTypes` early in the query to set types.

4. **Fabric notebooks & pipelines**:
   - Use PySpark with `spark.read.format("delta")` for reading lakehouse tables.
   - Write notebooks with clear markdown cells explaining each transformation step.
   - Use Fabric pipeline parameters for environment-specific configuration.
   - Leverage Fabric's built-in Git integration for version control.

5. **Windows-specific conventions**:
   - Use PowerShell or Windows Terminal for CLI operations.
   - Reference paths with backslashes or raw strings in Python (`r"C:\path"`).
   - Use `.pbix` files for Power BI Desktop development; `.bim` / TMDL for model definitions.

## References

- Source: [wardawgmalvicious/claude-config](https://github.com/wardawgmalvicious/claude-config) — Personal Claude Code config with skills, subagents, hooks, and rules for Microsoft Fabric and Power BI workflows on Windows.
