import asyncio
from backend.db import connect_db, disconnect_db, execute

async def seed():
    await connect_db()
    await execute("DELETE FROM order_items")
    await execute("DELETE FROM orders")
    await execute("DELETE FROM products")
    products = [
        ("T-shirt", 1999, "https://via.placeholder.com/150", "A cool T-shirt"),
        ("Jeans", 4999, "https://via.placeholder.com/150", "Stylish jeans"),
        ("Sneakers", 7999, "https://via.placeholder.com/150", "Comfortable sneakers"),
    ]
    for name, price_cents, image_url, description in products:
        await execute(
            "INSERT INTO products (name, price_cents, image_url, description) VALUES ($1, $2, $3, $4)",
            name, price_cents, image_url, description
        )
    await disconnect_db()

if __name__ == "__main__":
    asyncio.run(seed())
