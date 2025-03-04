from fastapi import APIRouter, HTTPException, Query
from database import orders_collection
from bson import ObjectId
from pydantic import BaseModel
from typing import List, Optional
import json

router = APIRouter()


# Order Pydantic model
class Order(BaseModel):
    orderId: int
    status: str
    items: List[str]
    tracking: str

class OrderUpdate(BaseModel):
    status: str

#  Create a new order
@router.post("/api/orders")
async def create_order(order: Order):
    existing_order = await orders_collection.find_one({"orderId": order.orderId})
    if existing_order:
        raise HTTPException(status_code=400, detail="Order already exists")

    new_order = order.dict()
    await orders_collection.insert_one(new_order)
    return {"message": "Order created successfully", "orderId": order.orderId}

#  Get full order details
@router.get("/api/orders/{orderId}")
async def get_order(orderId: int):
    order = await orders_collection.find_one({"orderId": orderId})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["_id"] = str(order["_id"])
    return order

#  Retrieve order status
@router.get("/api/orders/{orderId}/status")
async def get_order_status(orderId: int):
    order = await orders_collection.find_one({"orderId": orderId}, {"status": 1, "_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

#  Update order status
@router.put("/api/orders/{orderId}/status")
async def update_order_status(orderId: int, update_data: OrderUpdate):
    result = await orders_collection.update_one(
        {"orderId": orderId},
        {"$set": update_data.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order status updated successfully", "orderId": orderId}

#  Cancel an order
@router.delete("/api/orders/{orderId}")
async def cancel_order(orderId: int):
    result = await orders_collection.delete_one({"orderId": orderId})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully", "orderId": orderId}

#  Track live order status
@router.get("/api/orders/{orderId}/tracking")
async def track_order(orderId: int):
    order = await orders_collection.find_one({"orderId": orderId}, {"tracking": 1, "_id": 0})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

#  Get all orders (Admin use) - Pagination
@router.get("/api/orders")
async def get_all_orders(
    page: int = Query(1, alias="pageNumber"),
    size: int = Query(10, alias="pageSize")
):
    skip = (page - 1) * size
    orders_cursor = orders_collection.find().skip(skip).limit(size)
    
    orders = []
    async for order in orders_cursor:
        order["_id"] = str(order["_id"])
        orders.append(order)

    return {"page": page, "size": size, "orders": orders}
