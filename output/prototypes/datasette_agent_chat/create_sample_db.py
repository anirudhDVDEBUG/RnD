"""Create a sample SQLite database for demonstrating datasette-agent."""
import sqlite3
import os

DB_PATH = os.environ.get("DEMO_DB", "demo.db")


def create_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    products = [
        ("Wireless Mouse", "Electronics", 29.99, 150, "2026-01-15"),
        ("Mechanical Keyboard", "Electronics", 89.99, 75, "2026-01-20"),
        ("USB-C Hub", "Electronics", 45.00, 200, "2026-02-01"),
        ("Standing Desk", "Furniture", 499.99, 30, "2026-02-10"),
        ("Monitor Arm", "Furniture", 79.99, 90, "2026-02-15"),
        ("Webcam HD", "Electronics", 59.99, 120, "2026-03-01"),
        ("Desk Lamp", "Furniture", 34.99, 180, "2026-03-05"),
        ("Laptop Stand", "Furniture", 42.00, 110, "2026-03-10"),
        ("Noise-Cancel Headphones", "Electronics", 199.99, 60, "2026-03-15"),
        ("Ergonomic Chair", "Furniture", 649.99, 25, "2026-04-01"),
        ("Portable Charger", "Electronics", 24.99, 300, "2026-04-10"),
        ("Cable Organizer", "Accessories", 12.99, 500, "2026-04-15"),
        ("Mousepad XL", "Accessories", 19.99, 250, "2026-04-20"),
        ("Screen Cleaner Kit", "Accessories", 9.99, 400, "2026-05-01"),
        ("Bluetooth Speaker", "Electronics", 69.99, 85, "2026-05-10"),
    ]
    c.executemany(
        "INSERT INTO products (name, category, price, stock, created_at) VALUES (?,?,?,?,?)",
        products,
    )

    c.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            customer_email TEXT NOT NULL,
            ordered_at TEXT NOT NULL
        )
    """)

    orders = [
        (1, 2, 59.98, "alice@example.com", "2026-05-01"),
        (3, 1, 45.00, "bob@example.com", "2026-05-02"),
        (2, 1, 89.99, "alice@example.com", "2026-05-03"),
        (5, 3, 239.97, "carol@example.com", "2026-05-04"),
        (1, 1, 29.99, "dave@example.com", "2026-05-05"),
        (9, 1, 199.99, "carol@example.com", "2026-05-06"),
        (4, 1, 499.99, "eve@example.com", "2026-05-07"),
        (11, 5, 124.95, "alice@example.com", "2026-05-08"),
        (15, 2, 139.98, "bob@example.com", "2026-05-09"),
        (10, 1, 649.99, "frank@example.com", "2026-05-10"),
        (6, 2, 119.98, "dave@example.com", "2026-05-11"),
        (12, 10, 129.90, "grace@example.com", "2026-05-12"),
        (7, 3, 104.97, "carol@example.com", "2026-05-13"),
        (8, 2, 84.00, "alice@example.com", "2026-05-14"),
        (14, 4, 39.96, "bob@example.com", "2026-05-15"),
    ]
    c.executemany(
        "INSERT INTO orders (product_id, quantity, total, customer_email, ordered_at) VALUES (?,?,?,?,?)",
        orders,
    )

    conn.commit()
    conn.close()
    print(f"Created sample database: {DB_PATH}")
    print(f"  - products: 15 rows")
    print(f"  - orders:   15 rows")


if __name__ == "__main__":
    create_db()
