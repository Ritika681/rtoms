from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from model.models import Order
from database import get_session
from pydantic import BaseModel
import json

router = APIRouter(prefix="/api/orders", tags=["Orders"])


class OrderCreate(BaseModel):
    orderId: int
    status: str
    items: List[str]
    tracking: str
    userId: int


class OrderUpdate(BaseModel):
    status: str


@router.post("")
async def create_order(order: OrderCreate, session: AsyncSession = Depends(get_session)):
    stmt = select(Order).where(Order.orderId == order.orderId)
    result = await session.exec(stmt)
    existing = result.first()
    if existing:
        raise HTTPException(status_code=400, detail="Order already exists")

    db_order = Order(
        orderId=order.orderId,
        status=order.status,
        items=json.dumps(order.items),
        tracking=order.tracking,
        userId=order.userId
    )
    session.add(db_order)
    await session.commit()
    return {"message": "Order created successfully", "orderId": order.orderId}


@router.get("/{orderId}")
async def get_order(orderId: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Order).where(Order.orderId == orderId)
    result = await session.exec(stmt)
    order = result.first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {
        "orderId": order.orderId,
        "status": order.status,
        "items": json.loads(order.items),
        "tracking": order.tracking,
        "userId": order.userId
    }


@router.get("/{orderId}/status")
async def get_order_status(orderId: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Order.status).where(Order.orderId == orderId)
    result = await session.exec(stmt)
    status = result.scalar_one_or_none()
    if status is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"status": status}


@router.put("/{orderId}/status")
async def update_order_status(orderId: int, update: OrderUpdate, session: AsyncSession = Depends(get_session)):
    stmt = select(Order).where(Order.orderId == orderId)
    result = await session.exec(stmt)
    order = result.first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = update.status
    session.add(order)
    await session.commit()
    return {"message": "Order status updated successfully", "orderId": orderId}


@router.delete("/{orderId}")
async def cancel_order(orderId: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Order).where(Order.orderId == orderId)
    result = await session.exec(stmt)
    order = result.first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await session.delete(order)
    await session.commit()
    return {"message": "Order deleted successfully", "orderId": orderId}


@router.get("/{orderId}/tracking")
async def track_order(orderId: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Order.tracking).where(Order.orderId == orderId)
    result = await session.exec(stmt)
    tracking = result.scalar_one_or_none()
    if tracking is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"tracking": tracking}


@router.get("")
async def get_all_orders(
    page: int = Query(1, alias="pageNumber"),
    size: int = Query(10, alias="pageSize"),
    session: AsyncSession = Depends(get_session)
):
    offset = (page - 1) * size
    stmt = select(Order).offset(offset).limit(size)
    result = await session.exec(stmt)
    orders_list = result.all()

    orders = []
    for order in orders_list:
        orders.append({
            "orderId": order.orderId,
            "status": order.status,
            "items": json.loads(order.items),
            "tracking": order.tracking,
            "userId": order.userId
        })

    return {"page": page, "size": size, "orders": orders}
