# Technical Details — Fabric & Power BI Workflow Skill

## What It Does

This skill injects domain-specific conventions into Claude Code's context whenever a user works on Microsoft Fabric or Power BI tasks. It encodes best practices for:

- **Medallion architecture** (bronze/silver/gold) data layering in Fabric lakehouses
- **DAX patterns** — `VAR/RETURN`, `CALCULATE` with proper filter context, `DIVIDE` for safe division
- **Power Query M** — query folding awareness, typed step naming, `let/in` structure
- **PySpark notebooks** — Delta Lake reads, markdown documentation cells, parameterization
- **Star schema design** — fact/dimension separation, surrogate keys, measures over calculated columns

The skill does NOT call any APIs or run any code itself. It is purely a prompt-augmentation layer that shapes Claude's output quality for this domain.

## Architecture

```
~/.claude/skills/fabric_powerbi_workflow/
└── SKILL.md          # Single file — trigger rules + conventions
```

**Data flow:**
1. User types a message mentioning Fabric/Power BI/DAX/etc.
2. Claude Code's skill matcher detects trigger keywords.
3. SKILL.md content is injected into Claude's system context.
4. Claude generates code/advice following the encoded conventions.

**Dependencies:** None. This is a static skill file — no runtime dependencies, no API calls.

## Key Conventions Enforced

| Area | Convention | Why |
|------|-----------|-----|
| Lakehouse tables | Delta Lake format | Fabric default; enables time-travel, ACID |
| Ingestion | `COPY INTO` / pipelines | Scalable, auditable vs. manual upload |
| DAX | `VAR/RETURN` style | Readable, debuggable, avoids repeated sub-expressions |
| DAX | Measures > calculated columns | Compressed storage, flexible aggregation |
| Power Query M | Early `Table.TransformColumnTypes` | Enables query folding downstream |
| Notebooks | Markdown cells between code | Reproducibility for team handoff |
| Paths (Windows) | Raw strings `r"C:\..."` | Avoids escape-char bugs |

## Limitations

- **No runtime validation** — the skill can't verify that generated DAX actually compiles against your model. You still need to paste into Power BI Desktop or DAX Studio.
- **No schema awareness** — it doesn't know your actual table/column names. You must provide them or Claude will use generic placeholders.
- **Windows-centric** — path conventions assume Windows. Linux/macOS Fabric developers need to mentally translate.
- **Static knowledge** — if Microsoft changes Fabric APIs (e.g., new REST endpoints), the skill won't auto-update. You'd edit SKILL.md manually.
- **No MCP integration** — doesn't connect to a live Fabric workspace. For that, you'd need a custom MCP server wrapping the Fabric REST API.

## Relevance to AI-Product Builders

| Use Case | How This Helps |
|----------|---------------|
| **Agent factories** | Template for domain-specific skills — same pattern works for Snowflake, BigQuery, dbt, etc. |
| **Lead-gen / marketing** | Teams building Power BI dashboards for campaign analytics get correct DAX on first try. |
| **Ad creatives** | Performance-marketing teams using Fabric for ad-spend analysis get proper medallion pipelines. |
| **Voice AI** | Voice-driven BI assistants can use this skill pattern to generate spoken DAX explanations. |

## Source

[wardawgmalvicious/claude-config](https://github.com/wardawgmalvicious/claude-config) — Personal Claude Code config with skills, subagents, hooks, and rules for Microsoft Fabric and Power BI workflows on Windows. Cherry-pickable, no semver.
