#!/usr/bin/env python3
"""
End-to-end demo of the Honeydew semantic-layer workflow.

Uses a mock client (no API key needed) to show:
  1. Listing entities in the semantic layer
  2. Exploring entity attributes and relationships
  3. Browsing pre-defined business metrics
  4. Generating semantically correct SQL from metric references
"""

import json
from honeydew_mock import HoneydewClient

DIVIDER = "=" * 64


def section(title: str):
    print(f"\n{DIVIDER}")
    print(f"  {title}")
    print(DIVIDER)


def main():
    client = HoneydewClient(
        workspace="ecommerce_analytics",
        domain="demo.honeydew.live",
        api_key="mock-key-for-demo",
    )

    # ----- 1. List entities ------------------------------------------------
    section("1. Entities in the Semantic Layer")
    entities = client.list_entities()
    for e in entities:
        desc = client.describe_entity(e)
        print(f"\n  [{e}]  {desc['description']}")
        print(f"    Attributes : {', '.join(desc['attributes'].keys())}")
        print(f"    Related to : {', '.join(desc['relationships'])}")

    # ----- 2. Deep-dive on one entity --------------------------------------
    section("2. Attribute Details — orders.total_amount")
    detail = client.get_attribute_details("orders", "total_amount")
    print(json.dumps(detail, indent=2))

    # ----- 3. Metrics catalogue --------------------------------------------
    section("3. Business Metrics Catalogue")
    for m in client.list_metrics():
        info = client.get_metric(m)
        print(f"\n  {m}")
        print(f"    Expression : {info['expression']}")
        print(f"    Description: {info['description']}")

    # ----- 4. SQL generation -----------------------------------------------
    section("4. Generated SQL — Revenue by Region")
    sql = client.generate_sql(
        metric_names=["total_revenue", "order_count"],
        group_by=["customers.region"],
    )
    print(f"\n{sql}")

    section("5. Generated SQL — Net Revenue, Web Channel Only")
    sql2 = client.generate_sql(
        metric_names=["net_revenue", "average_order_value"],
        group_by=["orders.channel"],
        filters={"orders.channel": "web"},
    )
    print(f"\n{sql2}")

    section("6. Generated SQL — Repeat Purchase Rate by Segment")
    sql3 = client.generate_sql(
        metric_names=["repeat_purchase_rate", "customer_count"],
        group_by=["customers.segment"],
    )
    print(f"\n{sql3}")

    print(f"\n{DIVIDER}")
    print("  Demo complete. All queries generated from the semantic layer.")
    print(f"{DIVIDER}\n")


if __name__ == "__main__":
    main()
