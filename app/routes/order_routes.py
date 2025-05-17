from fastapi import APIRouter, HTTPException, Query, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from app.model.models import Order
from database import get_session
from pydantic import BaseModel
import json
import uuid

router = APIRouter(prefix="/api/orders", tags=["Orders"])


class OrderCreate(BaseModel):
    status: str
    items: List[str]
    userId: int


class OrderUpdate(BaseModel):
    status: str

@router.post("")
async def create_order(order: OrderCreate, session: AsyncSession = Depends(get_session)):
    
    tracking = f"TRK-{uuid.uuid4().hex[:8].upper()}" 
    stmt = select(Order).where(Order.tracking == tracking)
    while (await session.exec(stmt)).first():
        tracking = f"TRK-{uuid.uuid4().hex[:8].upper()}"

    db_order = Order(
        status=order.status,
        items=json.dumps(order.items),
        tracking=tracking,
        userId=order.userId
    )
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)

    return {
        "message": "Order created successfully",
        "orderId": db_order.orderId,
        "tracking": db_order.tracking
    }
    

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
