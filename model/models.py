from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users_table"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    orders: List["Order"] = Relationship(back_populates="user")

class Order(SQLModel, table=True):
    __tablename__ = "orders_table"
    id: Optional[int] = Field(default=None, primary_key=True)
    orderId: int = Field(index=True, unique=True)
    status: str
    items: str 
    tracking: str
    userId: Optional[int] = Field(default=None, foreign_key="users_table.id")
    user: Optional["User"] = Relationship(back_populates="orders")
