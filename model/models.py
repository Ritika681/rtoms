from sqlmodel import SQLModel, Field
from typing import Optional

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    orderId: int = Field(index=True, unique=True)
    status: str
    items: str  # JSON string of list
    tracking: str
