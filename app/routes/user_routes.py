from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
from database import get_session
from app.model.models import User, Order
import json

class UserBase(SQLModel):
    name: str
    email: str
    phoneNumber: str

class UserCreate(UserBase):
    pass

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/signup")
async def signup_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    # Check if user already exists
    stmt = select(User).where(User.email == user.email)
    result = await session.exec(stmt)
    existing_user = result.first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User.from_orm(user)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return {"id": new_user.id, "name": new_user.name, "email": new_user.email, "phoneNumber": new_user.phoneNumber}

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