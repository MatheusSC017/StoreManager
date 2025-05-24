from pydantic import BaseModel, Field
from datetime import date as dt_date
from typing import Optional


class ProductCreate(BaseModel):
    description: str = Field(example="Chocolate Bar")
    value: float = Field(example=12.5)
    barcode: str = Field(example="567671948894")
    section: str = Field(example="Section B")
    stock: int = Field(example=250)
    expiration_date: Optional[dt_date] = Field(example="2025-07-24")


class ProductOut(BaseModel):
    id: int = Field(example=1)
    description: str = Field(example="Chocolate Bar")
    value: float = Field(example=12.5)
    barcode: str = Field(example="567671948894")
    section: str = Field(example="Section B")
    stock: int = Field(example=250)
    expiration_date: Optional[dt_date] = Field(example="2025-07-24")

    class Config:
        from_attributes = True
