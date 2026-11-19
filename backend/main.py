from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from backend.db import connect_db, disconnect_db, fetch, execute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    id: int
    name: str
    price_cents: int
    image_url: str
    description: str

class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    items: List[OrderItem]

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

@app.get("/api/products", response_model=List[Product])
async def get_products():
    rows = await fetch("SELECT id, name, price_cents, image_url, description FROM products ORDER BY id")
    return [Product(
        id=row["id"], name=row["name"], price_cents=row["price_cents"], image_url=row["image_url"], description=row["description"]
    ) for row in rows]

@app.post("/api/orders")
async def create_order(order: Order):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")
    async with asyncio.Lock():
        res = await execute("INSERT INTO orders DEFAULT VALUES RETURNING id")
        order_id = None
        if res.startswith("INSERT 0 1"):
            # Need to get last inserted id
            last_row = await fetch("SELECT currval(pg_get_serial_sequence('orders','id')) AS id")
            order_id = last_row[0]["id"]
        else:
            raise HTTPException(status_code=500, detail="Failed to create order")
        for item in order.items:
            await execute(
                "INSERT INTO order_items (order_id, product_id, quantity) VALUES ($1, $2, $3)",
                order_id, item.product_id, item.quantity
            )
    return {"message": "Order placed successfully"}
