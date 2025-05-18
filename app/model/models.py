from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, ForwardRef
import datetime


Order = ForwardRef("orders_table")

class User(SQLModel, table=True):
    __tablename__ = "users_table"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phoneNumber: str

    orders: List["Order"] = Relationship(back_populates="user")


class Order(SQLModel, table=True):
    __tablename__ = "orders_table"
    orderId: Optional[int] = Field(default=None, primary_key=True)
    status: str
    items: str
    tracking: str = Field(unique=True)
    userId: int = Field(foreign_key="users_table.id")  
    user: Optional[User] = Relationship(back_populates="orders")
