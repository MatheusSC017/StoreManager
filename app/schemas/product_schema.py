from pydantic import BaseModel, Field, ConfigDict
from datetime import date as dt_date
from typing import Optional, List


class ProductCreate(BaseModel):
    description: str = Field(json_schema_extra={"example": "Chocolate Bar"})
    value: float = Field(json_schema_extra={"example": 12.5})
    barcode: str = Field(json_schema_extra={"example": "567671948894"})
    section: str = Field(json_schema_extra={"example": "Section B"})
    stock: int = Field(json_schema_extra={"example": 250})
    expiration_date: Optional[dt_date] = Field(json_schema_extra={"example": "2025-07-24"})


class ProductImageOut(BaseModel):
    id: int
    filename: str

    model_config = ConfigDict(from_attributes=True)


class ProductOut(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 1})
    description: str = Field(..., json_schema_extra={"example": "Chocolate Bar"})
    value: float = Field(..., json_schema_extra={"example": 12.5})
    barcode: str = Field(..., json_schema_extra={"example": "567671948894"})
    section: str = Field(..., json_schema_extra={"example": "Section B"})
    stock: int = Field(..., json_schema_extra={"example": 250})
    expiration_date: Optional[dt_date] = Field(json_schema_extra={"example": "2025-07-24"})
    images: List[ProductImageOut] = []

    model_config = ConfigDict(from_attributes=True)
