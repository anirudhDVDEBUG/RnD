"""
Demo: Fabric & Power BI Workflow Skill — generates example artifacts
showing the conventions this skill teaches Claude Code.

No external dependencies. No API keys. Pure stdlib.
"""

import json
import textwrap
from datetime import date


def generate_dax_measures():
    """Generate example DAX measures following skill conventions."""
    measures = {
        "Revenue YoY Growth %": textwrap.dedent("""\
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
                )"""),
        "Running Total Revenue": textwrap.dedent("""\
            Running Total Revenue =
            VAR MaxDate =
                MAX( DimDate[Date] )
            RETURN
                CALCULATE(
                    SUM( FactSales[Revenue] ),
                    DimDate[Date] <= MaxDate,
                    ALL( DimDate )
                )"""),
        "Avg Order Value": textwrap.dedent("""\
            Avg Order Value =
            VAR TotalRevenue =
                SUM( FactSales[Revenue] )
            VAR OrderCount =
                DISTINCTCOUNT( FactSales[OrderID] )
            RETURN
                DIVIDE( TotalRevenue, OrderCount )"""),
    }
    return measures


def generate_power_query_m():
    """Generate example Power Query M script following skill conventions."""
    return textwrap.dedent("""\
        let
            Source = Csv.Document(
                File.Contents("bronze/raw_customers.csv"),
                [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]
            ),
            PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
            SetTypes = Table.TransformColumnTypes(PromotedHeaders, {
                {"CustomerID", Int64.Type},
                {"Name", type text},
                {"Email", type text},
                {"SignupDate", type date},
                {"Revenue", Currency.Type}
            }),
            RemovedNulls = Table.SelectRows(SetTypes, each [CustomerID] <> null),
            FilteredByDate = Table.SelectRows(RemovedNulls,
                each [SignupDate] >= #date(2024, 1, 1)
            ),
            TrimmedText = Table.TransformColumns(FilteredByDate, {
                {"Name", Text.Trim, type text},
                {"Email", Text.Lower, type text}
            })
        in
            TrimmedText""")


def generate_pyspark_notebook():
    """Generate example PySpark notebook cells for a Fabric lakehouse."""
    cells = [
        {
            "type": "markdown",
            "content": "# Bronze → Silver: Customer Data Cleansing\n"
                       "Read raw CSV from bronze layer, clean, and write to silver as Delta.",
        },
        {
            "type": "code",
            "content": textwrap.dedent("""\
                # Read from bronze layer (Delta format in Fabric lakehouse)
                df_raw = spark.read.format("delta").load(
                    "Tables/bronze_customers"
                )
                print(f"Bronze row count: {df_raw.count()}")"""),
        },
        {
            "type": "markdown",
            "content": "## Data Quality: Remove nulls, trim strings, validate emails",
        },
        {
            "type": "code",
            "content": textwrap.dedent("""\
                from pyspark.sql.functions import col, trim, lower, regexp_extract

                df_clean = (
                    df_raw
                    .filter(col("customer_id").isNotNull())
                    .withColumn("name", trim(col("name")))
                    .withColumn("email", lower(trim(col("email"))))
                    .filter(
                        regexp_extract(col("email"), r"^[\\w.+-]+@[\\w-]+\\.[\\w.]+$", 0) != ""
                    )
                )
                print(f"Silver row count: {df_clean.count()}")"""),
        },
        {
            "type": "markdown",
            "content": "## Write to Silver layer as Delta with merge schema",
        },
        {
            "type": "code",
            "content": textwrap.dedent("""\
                (
                    df_clean.write
                    .format("delta")
                    .mode("overwrite")
                    .option("mergeSchema", "true")
                    .save("Tables/silver_customers")
                )
                print("Silver layer written successfully.")"""),
        },
    ]
    return cells


def generate_medallion_layout():
    """Generate a medallion architecture directory layout."""
    return {
        "lakehouse": {
            "Tables": {
                "bronze_customers": {"format": "delta", "source": "raw CSV via COPY INTO"},
                "bronze_orders": {"format": "delta", "source": "Fabric pipeline"},
                "silver_customers": {"format": "delta", "source": "notebook transform"},
                "silver_orders": {"format": "delta", "source": "notebook transform"},
                "gold_customer_360": {"format": "delta", "source": "aggregation notebook"},
                "gold_revenue_summary": {"format": "delta", "source": "aggregation notebook"},
            }
        }
    }


def generate_tsql_warehouse_query():
    """Generate example T-SQL for Fabric warehouse."""
    return textwrap.dedent("""\
        -- Fabric Warehouse: Gold layer aggregation
        -- Uses T-SQL (not PySpark) per skill conventions for warehouse queries
        CREATE VIEW gold.vw_monthly_revenue AS
        SELECT
            d.CalendarYear,
            d.MonthName,
            d.MonthNumber,
            SUM(f.Revenue) AS TotalRevenue,
            COUNT(DISTINCT f.CustomerKey) AS UniqueCustomers,
            SUM(f.Revenue) / NULLIF(COUNT(DISTINCT f.OrderKey), 0) AS AvgOrderValue
        FROM fact.Sales AS f
        INNER JOIN dim.Date AS d
            ON f.DateKey = d.DateKey
        GROUP BY
            d.CalendarYear,
            d.MonthName,
            d.MonthNumber;""")


def main():
    print("=" * 70)
    print("  FABRIC & POWER BI WORKFLOW SKILL — Demo Output")
    print(f"  Generated: {date.today().isoformat()}")
    print("=" * 70)

    # 1. DAX Measures
    print("\n" + "─" * 70)
    print("  1. DAX MEASURES (VAR/RETURN pattern, star-schema references)")
    print("─" * 70)
    measures = generate_dax_measures()
    for name, dax in measures.items():
        print(f"\n  ┌─ {name}")
        for line in dax.split("\n"):
            print(f"  │ {line}")
        print("  └─")

    # 2. Power Query M
    print("\n" + "─" * 70)
    print("  2. POWER QUERY M (let/in, early type setting, query folding)")
    print("─" * 70)
    pq = generate_power_query_m()
    for line in pq.split("\n"):
        print(f"    {line}")

    # 3. PySpark Notebook
    print("\n" + "─" * 70)
    print("  3. FABRIC NOTEBOOK — PySpark (bronze → silver, Delta format)")
    print("─" * 70)
    cells = generate_pyspark_notebook()
    for i, cell in enumerate(cells):
        marker = "MD" if cell["type"] == "markdown" else "PY"
        print(f"\n  [{marker}] Cell {i + 1}:")
        for line in cell["content"].split("\n"):
            print(f"    {line}")

    # 4. T-SQL Warehouse Query
    print("\n" + "─" * 70)
    print("  4. FABRIC WAREHOUSE — T-SQL (gold layer view)")
    print("─" * 70)
    tsql = generate_tsql_warehouse_query()
    for line in tsql.split("\n"):
        print(f"    {line}")

    # 5. Medallion Architecture Layout
    print("\n" + "─" * 70)
    print("  5. MEDALLION ARCHITECTURE — Lakehouse table layout")
    print("─" * 70)
    layout = generate_medallion_layout()
    tables = layout["lakehouse"]["Tables"]
    for table_name, meta in tables.items():
        layer = table_name.split("_")[0]
        print(f"    Tables/{table_name:<25} [{layer.upper()}]  ← {meta['source']}")

    # Summary
    print("\n" + "=" * 70)
    print("  SUMMARY: Skill encodes these conventions so Claude produces")
    print("  production-quality Fabric/PBI code without extra prompting.")
    print("=" * 70)
    print(f"\n  Artifacts generated: {len(measures)} DAX measures, 1 Power Query M script,")
    print(f"  {len(cells)} notebook cells, 1 T-SQL view, {len(tables)} medallion tables.")
    print()


if __name__ == "__main__":
    main()
