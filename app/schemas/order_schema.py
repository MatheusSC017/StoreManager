from pydantic import BaseModel
from datetime import date
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "Pending"
    CLOSED = "Closed"


class ProductQuantity(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    client_id: int
    date: date
    status: OrderStatus
    products: List[ProductQuantity]


class OrderOut(BaseModel):
    id: int
    client_id: int
    date: date
    status: OrderStatus
    products: List[ProductQuantity]

    class Config:
        from_attributes = True
