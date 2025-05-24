from pydantic import BaseModel, Field, ConfigDict
from datetime import date as dt_date
from typing import List
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "Pending"
    CLOSED = "Closed"


class ProductQuantity(BaseModel):
    product_id: int = Field(json_schema_extra={"example": 1})
    quantity: int = Field(json_schema_extra={"example": 10})


class OrderCreate(BaseModel):
    client_id: int = Field(json_schema_extra={"example": 1})
    date: dt_date = Field(json_schema_extra={"example": "2025-05-23"})
    status: OrderStatus = Field(json_schema_extra={"example": "Pending"})
    products: List[ProductQuantity] = Field(json_schema_extra={"example": [{"product_id": 1, "quantity": 10}, ]})


class OrderOut(BaseModel):
    id: int = Field(json_schema_extra={"example": 1})
    client_id: int = Field(json_schema_extra={"example": 1})
    date: dt_date = Field(json_schema_extra={"example": "2025-05-23"})
    status: OrderStatus = Field(json_schema_extra={"example": "Pending"})
    products: List[ProductQuantity] = Field(json_schema_extra={"example": [{"product_id": 1, "quantity": 10}, ]})

    model_config = ConfigDict(from_attributes=True)
