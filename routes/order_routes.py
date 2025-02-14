from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

# Simulated in-memory order storage
orders_db: Dict[int, Dict] = {
    1: {"orderId": 1, "status": "Processing", "items": ["item1", "item2"], "tracking": "In warehouse"},
    2: {"orderId": 2, "status": "Shipped", "items": ["item3"], "tracking": "Out for delivery"},
    3: {"orderId": 3, "status": "Delivered", "items": ["item4", "item5"], "tracking": "Delivered"}
}

# Define Pydantic model for updating order status
class OrderStatusUpdate(BaseModel):
    status: str

# Get all orders
@router.get("/api/orders/")
async def get_order():
    order = orders_db
    return order

# Get full order details
@router.get("/api/orders/{orderId}")
async def get_order(orderId: int):
    order = orders_db.get(orderId)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order