from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from database import get_session
from app.model.models import User, Order
import json

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("/{userId}/orders")
async def get_user_orders(userId: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Order).where(Order.userId == userId)
    result = await session.exec(stmt)
    orders = result.all()

    return [
        {
            "orderId": o.orderId,
            "status": o.status,
            "items": json.loads(o.items),
            "tracking": o.tracking,
            "userId": o.userId
        } for o in orders
    ]


@router.get("/{userId}/order-history")
async def get_user_order_history(userId: int, session: AsyncSession = Depends(get_session)):
    stmt = select(Order).where(Order.userId == userId)
    result = await session.exec(stmt)
    orders = result.all()

    # Simulate historical data return; extend as needed for actual history
    return [
        {
            "orderId": o.orderId,
            "status": o.status,
            "tracking": o.tracking,
            "userId": o.userId
        } for o in orders
    ]
