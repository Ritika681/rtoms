from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, ForwardRef
import datetime


Order = ForwardRef("Order")

class User(SQLModel, table=True):
    __tablename__ = "users_table"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phoneNumber: str

    orders: List["Order"] = Relationship(back_populates="user")


class Order(SQLModel, table=True):
    orderId: Optional[int] = Field(default=None, primary_key=True)
    status: str
    items: str
    tracking: str = Field(unique=True)
    userId: int = Field(foreign_key="users_table.id")  
    created_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow)
    user: Optional[User] = Relationship(back_populates="orders")
