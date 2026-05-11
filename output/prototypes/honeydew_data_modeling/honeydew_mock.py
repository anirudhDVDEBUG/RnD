"""
Mock Honeydew semantic layer client.

Simulates the Honeydew AI coding-agents plugin by providing:
  - Entity/attribute exploration
  - Metric definitions retrieval
  - Semantic SQL generation from natural-language metric requests

No real API key is needed — all data is synthetic.
"""

import json
from typing import Optional

# ---------------------------------------------------------------------------
# Mock semantic-layer catalogue
# ---------------------------------------------------------------------------

ENTITIES = {
    "orders": {
        "description": "All e-commerce orders placed on the platform",
        "attributes": {
            "order_id":      {"type": "string",    "description": "Unique order identifier"},
            "customer_id":   {"type": "string",    "description": "FK to customers entity"},
            "order_date":    {"type": "date",      "description": "Date the order was placed"},
            "status":        {"type": "string",    "description": "Order status (pending/shipped/delivered/returned)"},
            "total_amount":  {"type": "decimal",   "description": "Total order value in USD"},
            "discount":      {"type": "decimal",   "description": "Discount applied to the order"},
            "channel":       {"type": "string",    "description": "Acquisition channel (web/mobile/in-store)"},
        },
        "relationships": ["customers", "order_items"],
    },
    "customers": {
        "description": "Registered customer profiles",
        "attributes": {
            "customer_id":   {"type": "string",    "description": "Unique customer identifier"},
            "email":         {"type": "string",    "description": "Customer email address"},
            "signup_date":   {"type": "date",      "description": "Date customer registered"},
            "region":        {"type": "string",    "description": "Geographic region"},
            "lifetime_value":{"type": "decimal",   "description": "Calculated customer LTV"},
            "segment":       {"type": "string",    "description": "Marketing segment (new/active/churned)"},
        },
        "relationships": ["orders"],
    },
    "order_items": {
        "description": "Line items within each order",
        "attributes": {
            "item_id":       {"type": "string",    "description": "Unique line-item identifier"},
            "order_id":      {"type": "string",    "description": "FK to orders entity"},
            "product_name":  {"type": "string",    "description": "Name of the product"},
            "category":      {"type": "string",    "description": "Product category"},
            "quantity":      {"type": "integer",   "description": "Units purchased"},
            "unit_price":    {"type": "decimal",   "description": "Price per unit in USD"},
        },
        "relationships": ["orders"],
    },
}

METRICS = {
    "total_revenue": {
        "entity": "orders",
        "expression": "SUM(orders.total_amount)",
        "description": "Total revenue across all orders",
        "filters": [],
    },
    "average_order_value": {
        "entity": "orders",
        "expression": "AVG(orders.total_amount)",
        "description": "Average value per order",
        "filters": [],
    },
    "order_count": {
        "entity": "orders",
        "expression": "COUNT(DISTINCT orders.order_id)",
        "description": "Total number of unique orders",
        "filters": [],
    },
    "customer_count": {
        "entity": "customers",
        "expression": "COUNT(DISTINCT customers.customer_id)",
        "description": "Total number of unique customers",
        "filters": [],
    },
    "repeat_purchase_rate": {
        "entity": "orders",
        "expression": (
            "COUNT(DISTINCT CASE WHEN order_rank > 1 THEN orders.customer_id END) "
            "/ NULLIF(COUNT(DISTINCT orders.customer_id), 0)"
        ),
        "description": "Fraction of customers who placed more than one order",
        "filters": [],
    },
    "net_revenue": {
        "entity": "orders",
        "expression": "SUM(orders.total_amount - orders.discount)",
        "description": "Revenue after discounts",
        "filters": [],
    },
}


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class HoneydewClient:
    """Simulated Honeydew semantic-layer client."""

    def __init__(self, workspace: str = "demo_workspace",
                 domain: str = "demo.honeydew.live",
                 api_key: str = "mock-key"):
        self.workspace = workspace
        self.domain = domain
        self.api_key = api_key

    # -- exploration --------------------------------------------------------

    def list_entities(self) -> list[str]:
        return list(ENTITIES.keys())

    def describe_entity(self, name: str) -> dict:
        entity = ENTITIES.get(name)
        if not entity:
            raise KeyError(f"Entity '{name}' not found in workspace '{self.workspace}'")
        return {
            "entity": name,
            "description": entity["description"],
            "attributes": {
                k: v["type"] for k, v in entity["attributes"].items()
            },
            "relationships": entity["relationships"],
        }

    def get_attribute_details(self, entity_name: str, attribute: str) -> dict:
        entity = ENTITIES.get(entity_name)
        if not entity:
            raise KeyError(f"Entity '{entity_name}' not found")
        attr = entity["attributes"].get(attribute)
        if not attr:
            raise KeyError(f"Attribute '{attribute}' not found on entity '{entity_name}'")
        return {"entity": entity_name, "attribute": attribute, **attr}

    # -- metrics ------------------------------------------------------------

    def list_metrics(self) -> list[str]:
        return list(METRICS.keys())

    def get_metric(self, name: str) -> dict:
        metric = METRICS.get(name)
        if not metric:
            raise KeyError(f"Metric '{name}' not found")
        return {"metric": name, **metric}

    # -- SQL generation -----------------------------------------------------

    def generate_sql(self, metric_names: list[str],
                     group_by: Optional[list[str]] = None,
                     filters: Optional[dict] = None) -> str:
        """Generate a semantic SQL query from metric + dimension references."""
        selects = []
        tables = set()

        group_by = group_by or []
        filters = filters or {}

        for g in group_by:
            parts = g.split(".")
            if len(parts) == 2:
                tables.add(parts[0])
            selects.append(g)

        for m in metric_names:
            meta = METRICS.get(m)
            if not meta:
                raise KeyError(f"Unknown metric '{m}'")
            tables.add(meta["entity"])
            selects.append(f"{meta['expression']}  AS {m}")

        from_clause = " JOIN ".join(sorted(tables)) if tables else "dual"

        # build WHERE
        where_parts = []
        for col, val in filters.items():
            where_parts.append(f"{col} = '{val}'")

        sql = f"SELECT\n  " + ",\n  ".join(selects)
        sql += f"\nFROM {from_clause}"
        if where_parts:
            sql += "\nWHERE " + " AND ".join(where_parts)
        if group_by:
            sql += "\nGROUP BY " + ", ".join(group_by)

        return sql
