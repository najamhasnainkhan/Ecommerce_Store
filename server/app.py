from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Product(BaseModel):
    id: int
    name: str
    price: float
    image: str

class CartItem(BaseModel):
    id: int
    quantity: int

class Order(BaseModel):
    items: List[CartItem]

# In-memory products list
products = [
    {"id": 1, "name": "T-Shirt", "price": 19.99, "image": "https://via.placeholder.com/50"},
    {"id": 2, "name": "Mug", "price": 9.99, "image": "https://via.placeholder.com/50"},
    {"id": 3, "name": "Sticker", "price": 2.99, "image": "https://via.placeholder.com/50"}
]

@app.get("/api/products", response_model=List[Product])
def get_products():
    return products

@app.post("/api/orders")
def place_order(order: Order):
    # Simulate order processing
    if not order.items:
        raise HTTPException(status_code=400, detail="Order is empty")
    # Here, you could add logic to store order in DB
    return {"message": "Order placed successfully"}
