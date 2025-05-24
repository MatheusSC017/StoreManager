from pydantic import BaseModel
from datetime import date
from typing import Optional


class ProductCreate(BaseModel):
    description: str
    value: float
    barcode: str
    section: str
    stock: int
    expiration_date: Optional[date] = None


class ProductOut(BaseModel):
    id: int
    description: str
    value: float
    barcode: str
    section: str
    stock: int
    expiration_date: Optional[date] = None

    class Config:
        from_attributes = True
