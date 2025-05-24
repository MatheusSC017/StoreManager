from pydantic import BaseModel, Field
from datetime import date as dt_date
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "Pending"
    CLOSED = "Closed"


class ProductQuantity(BaseModel):
    product_id: int = Field(example=1)
    quantity: int = Field(example=10)


class OrderCreate(BaseModel):
    client_id: int = Field(example=1)
    date: dt_date = Field(example="2025-05-23")
    status: OrderStatus = Field(example="Pending")
    products: List[ProductQuantity] = Field(example=[{"product_id": 1, "quantity": 10}, ])


class OrderOut(BaseModel):
    id: int = Field(example=1)
    client_id: int = Field(example=1)
    date: dt_date = Field(example="2025-05-23")
    status: OrderStatus = Field(example="Pending")
    products: List[ProductQuantity] = Field(example=[{"product_id": 1, "quantity": 10}, ])

    class Config:
        from_attributes = True
